# main.py
from data_collection.ethereum_data import EthereumDataCollector
from data_collection.defi_api import DefiDataCollector
from data_processing.processor import DataProcessor
from ml_model.risk_model import RiskModel
from visualization.dashboard import run_dashboard
import streamlit as st

def main():
    # Data Collection
    eth_collector = EthereumDataCollector('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID')
    defi_collector = DefiDataCollector()

    latest_block = eth_collector.get_latest_block()
    defi_data = defi_collector.get_defi_data()

    # Data Processing
    df = DataProcessor.process_defi_data(defi_data)
    df = DataProcessor.calculate_risk_score(df)

    # Machine Learning Model
    risk_model = RiskModel()
    X = df[['market_cap', 'total_volume', 'volatility']]
    y = df['risk_label']
    accuracy = risk_model.train(X, y)

    # Streamlit Dashboard
    run_dashboard(df)

    st.write(f"## Model Accuracy: {accuracy:.2f}")
    st.write(f"Latest Ethereum Block: {latest_block['number']}")

if __name__ == "__main__":
    main()