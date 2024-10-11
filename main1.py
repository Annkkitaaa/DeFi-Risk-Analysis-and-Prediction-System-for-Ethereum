import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Add the current directory to Python's module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import custom modules
from data_collection.ethereum_data import EthereumDataCollector
from data_collection.defi_api import DefiDataCollector
from data_processing.processor import DataProcessor
from ml_model.risk_model import RiskModel
from visualization.dashboard import run_dashboard

# Set page config at the very beginning
st.set_page_config(page_title="DeFi Risk Analysis", page_icon="🔍", layout="wide")

def set_purple_theme():
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0e6ff;
        }
        .stButton>button {
            background-color: #8a2be2;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #e6d9ff;
        }
        .stSelectbox>div>div>select {
            background-color: #e6d9ff;
        }
        h1, h2, h3 {
            color: #4b0082;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    set_purple_theme()
    st.title("🔍 DeFi Risk Analysis and Prediction System")

    # Sidebar for navigation
    st.sidebar.header("Navigation")
    st.sidebar.markdown("""
        - [Data Collection](#data-collection)
        - [Risk Prediction](#risk-prediction)
        - [Interactive Dashboard](#interactive-dashboard)
    """)

    st.markdown("This app provides a comprehensive risk analysis of DeFi protocols using real-time Ethereum and DeFi data, combined with machine learning to predict risk levels.")

    try:
        # Section 1: Data Collection
        st.header("Data Collection")
        eth_collector = EthereumDataCollector('https://shape-mainnet.g.alchemy.com/v2/FxI_sgw7cJxy3yUMS1J2UN4U6K7exJX9')
        defi_collector = DefiDataCollector()

        latest_block = eth_collector.get_latest_block()
        if latest_block is None:
            st.error("Failed to fetch the latest Ethereum block.")
            return

        defi_data = defi_collector.get_defi_data()
        if defi_data is None:
            st.error("Failed to fetch DeFi data.")
            return

        st.success(f"✅ Latest Ethereum Block Number: {latest_block['number']}")

        # Section 2: Data Processing
        st.header("Data Processing")
        df = DataProcessor.process_defi_data(defi_data)
        df = DataProcessor.calculate_risk_score(df)
        st.success("✅ Data processed successfully")

        # Section 3: Risk Prediction
        st.header("Risk Prediction")
        risk_model = RiskModel()
        X = df[['market_cap', 'total_volume', 'volatility']]
        y = df['risk_label']
        accuracy = risk_model.train(X, y)
        st.success(f"✅ Model Accuracy: **{accuracy:.2f}**")

        st.subheader("Predict Risk Label")
        col1, col2, col3 = st.columns(3)
        with col1:
            market_cap = st.number_input("Market Cap (USD)", min_value=0.0, format="%.2f")
        with col2:
            total_volume = st.number_input("Total Volume (USD)", min_value=0.0, format="%.2f")
        with col3:
            volatility = st.number_input("Volatility (0-1)", min_value=0.0, max_value=1.0, format="%.2f")

        if st.button("Predict Risk"):
            input_data = [[market_cap, total_volume, volatility]]
            prediction = risk_model.predict(input_data)
            st.success(f"Predicted Risk Label: **{prediction[0]}**")

        # Section 4: Interactive Dashboard
        st.header("Interactive Dashboard")
        run_dashboard(df)

    except Exception as e:
        st.error(f"Error during execution: {e}")

if __name__ == "__main__":
    main()