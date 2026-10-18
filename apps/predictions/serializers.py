from rest_framework import serializers
from apps.market.serializers import StockSerializer
from .models import PredictionRun

class PredictionRunSerializer(serializers.ModelSerializer):
    stock_details = StockSerializer(source='stock', read_only=True)
    model_name = serializers.CharField(source='get_model_type_display', read_only=True)

    class Meta:
        model = PredictionRun
        fields = [
            'id', 'stock', 'stock_details', 'model_type', 'model_name',
            'horizon_days', 'current_price', 'predicted_price', 'expected_return_pct',
            'mae', 'rmse', 'directional_accuracy', 'predictions_json',
            'test_actual_json', 'test_pred_json', 'weights_json',
            'training_data_points', 'trained_at'
        ]
