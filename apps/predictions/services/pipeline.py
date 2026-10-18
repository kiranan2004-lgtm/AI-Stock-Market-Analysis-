import os
import warnings
from typing import Dict, Any, Tuple, List
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Suppress verbose TensorFlow output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

try:
    from statsmodels.tsa.arima.model import ARIMA
    statsmodels_available = True
except Exception:
    statsmodels_available = False

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    tensorflow_available = True
except Exception:
    tensorflow_available = False


class TimeSeriesDataPipeline:
    """
    Chronological data preparation pipeline designed to strictly eliminate
    look-ahead bias and data leakage. Fits scalers solely on the training partition.
    """

    def __init__(self, sequence_length: int = 30, test_ratio: float = 0.2):
        self.sequence_length = sequence_length
        self.test_ratio = test_ratio
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def prepare_raw_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Splits prices into train and test sets chronologically, then fits scaler
        ONLY on train_prices.
        Returns: (train_prices, test_prices, scaled_train, scaled_test, all_prices)
        """
        close_col = 'Close' if 'Close' in df.columns else ('close' if 'close' in df.columns else None)
        if not close_col:
            raise ValueError("Price column ('Close' or 'close') not found in dataset.")

        clean_series = pd.to_numeric(df[close_col], errors='coerce').dropna()
        clean_series = clean_series[clean_series > 0]
        prices = clean_series.values.astype(float)

        if len(prices) < self.sequence_length + 20:
            raise ValueError(f"Insufficient valid data points ({len(prices)}) for sequence length {self.sequence_length}.")

        train_size = int(len(prices) * (1.0 - self.test_ratio))
        train_prices = prices[:train_size]
        test_prices = prices[train_size:]

        # Fit scaler ONLY on training data to avoid data leakage
        self.scaler.fit(train_prices.reshape(-1, 1))
        scaled_train = self.scaler.transform(train_prices.reshape(-1, 1)).flatten()
        scaled_test = self.scaler.transform(test_prices.reshape(-1, 1)).flatten()

        return train_prices, test_prices, scaled_train, scaled_test, prices

    def create_sequences(self, scaled_series: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create rolling (X, y) sequence pairs."""
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_series)):
            X.append(scaled_series[i - self.sequence_length:i])
            y.append(scaled_series[i])
        return np.array(X), np.array(y)

    def extract_tabular_features(self, prices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract lag and rolling features for classical ML models (Linear Regression, Random Forest).
        Features: Lag 1, Lag 2, Lag 3, Lag 5, Rolling 5 Mean, Rolling 10 Std.
        """
        series = pd.Series(prices)
        df_feat = pd.DataFrame({'price': series})
        df_feat['lag_1'] = series.shift(1)
        df_feat['lag_2'] = series.shift(2)
        df_feat['lag_3'] = series.shift(3)
        df_feat['lag_5'] = series.shift(5)
        df_feat['roll_mean_5'] = series.shift(1).rolling(5).mean()
        df_feat['roll_std_10'] = series.shift(1).rolling(10).std().fillna(0)

        df_feat = df_feat.dropna()
        X = df_feat[['lag_1', 'lag_2', 'lag_3', 'lag_5', 'roll_mean_5', 'roll_std_10']].values
        y = df_feat['price'].values
        return X, y


class ModelEvaluator:
    """Computes honest out-of-sample statistical metrics."""

    @staticmethod
    def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        if len(y_true) == 0 or len(y_pred) == 0:
            return {'mae': 0.0, 'rmse': 0.0, 'directional_accuracy': 0.0}

        n = min(len(y_true), len(y_pred))
        yt = y_true[:n]
        yp = y_pred[:n]

        mae = float(mean_absolute_error(yt, yp))
        rmse = float(np.sqrt(mean_squared_error(yt, yp)))

        # Directional Accuracy: did the model predict the correct sign of daily change?
        if n > 1:
            actual_directions = np.sign(yt[1:] - yt[:-1])
            pred_directions = np.sign(yp[1:] - yt[:-1])
            correct_directions = np.sum(actual_directions == pred_directions)
            dir_acc = float((correct_directions / (n - 1)) * 100)
        else:
            dir_acc = 50.0

        return {
            'mae': round(mae, 2),
            'rmse': round(rmse, 2),
            'directional_accuracy': round(dir_acc, 2)
        }
