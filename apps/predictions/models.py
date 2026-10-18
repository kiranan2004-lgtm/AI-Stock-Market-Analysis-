from django.db import models

class PredictionRun(models.Model):
    """Execution run and evaluation of an econometric or deep-learning model."""
    MODEL_CHOICES = [
        ('linear', 'Linear Regression Baseline'),
        ('random_forest', 'Random Forest Regressor'),
        ('arima', 'ARIMA Time-Series'),
        ('lstm', 'LSTM Deep Neural Network'),
        ('hybrid', 'Hybrid LSTM-ARIMA Ensemble'),
    ]

    stock = models.ForeignKey('market.Stock', on_delete=models.CASCADE, related_name='prediction_runs')
    model_type = models.CharField(max_length=50, choices=MODEL_CHOICES)
    horizon_days = models.IntegerField(default=30)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    predicted_price = models.DecimalField(max_digits=12, decimal_places=2)
    expected_return_pct = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Validation metrics on held-out test dataset
    mae = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    rmse = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    directional_accuracy = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # Numerical series
    predictions_json = models.JSONField(default=list, help_text="Future forecast values")
    test_actual_json = models.JSONField(default=list, blank=True, help_text="Actual prices in test set")
    test_pred_json = models.JSONField(default=list, blank=True, help_text="Predicted prices in test set")
    weights_json = models.JSONField(default=dict, blank=True, help_text="Hybrid model weights or hyperparameters")
    
    training_data_points = models.IntegerField(default=0)
    trained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trained_at']

    def __str__(self):
        return f"{self.stock.symbol} [{self.model_type}] - {self.trained_at.strftime('%Y-%m-%d %H:%M')}"
