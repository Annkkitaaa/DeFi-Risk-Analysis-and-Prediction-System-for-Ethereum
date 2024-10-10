import pandas as pd

class DataProcessor:
    @staticmethod
    def process_defi_data(raw_data):
        df = pd.DataFrame(raw_data)
        df = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']]
        df['volatility'] = df['current_price'].pct_change().fillna(0)
        return df

    @staticmethod
    def calculate_risk_score(df):
        df['risk_score'] = (df['volatility'] * 0.4 + (df['total_volume'] / df['market_cap']) * 0.6) * 100
        df['risk_label'] = pd.cut(df['risk_score'], bins=[-float('inf'), 33, 66, float('inf')], labels=['Low', 'Medium', 'High'])
        return df