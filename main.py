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

def main():
    # Set the theme to be responsive to system preferences
    st.set_page_config(
        page_title="DeFi Risk Analysis",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for both light and dark modes
    st.markdown("""
    <style>
    /* Light mode styles */
    .stApp {
        background-color: #f3e5f5;
        color: #333333;
    }
    
    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #2d1e2f;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #9c27b0;
            color: white;
        }
        .stProgress .st-bo {
            background-color: #9c27b0;
        }
        /* Ensure text is visible in dark mode */
        p, h1, h2, h3, h4, h5, h6, li, .stMarkdown {
            color: #ffffff !important;
        }
    }
    
    /* Styles for both modes */
    .stButton>button {
        background-color: #9c27b0;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #9c27b0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔮 DeFi Risk Analysis and Prediction System")

    # Sidebar for navigation
    st.sidebar.header("Navigation")
    st.sidebar.text("Explore the functionalities:")
    st.sidebar.markdown("[Data Collection](#collecting-ethereum-and-defi-data)")
    st.sidebar.markdown("[Risk Prediction](#predict-risk-label)")
    st.sidebar.markdown("[Dashboard](#interactive-dashboard)")

    # Introduction
    st.write("""
    ## 📊 Welcome to the DeFi Risk Analysis Dashboard
    
    This application analyzes and predicts risk in DeFi (Decentralized Finance) protocols. 
    We collect data from Ethereum blockchain and DeFi APIs, process it, and use machine 
    learning to predict risk levels.
    """)

    try:
        # Data Collection
        st.header("🔗 Collecting Ethereum and DeFi Data")
        st.write("""
        We collect data from two main sources:
        1. Ethereum blockchain using Alchemy API
        2. DeFi protocols using CoinGecko API
        
        This data forms the foundation of our analysis.
        """)

        eth_collector = EthereumDataCollector('https://shape-mainnet.g.alchemy.com/v2/FxI_sgw7cJxy3yUMS1J2UN4U6K7exJX9')
        defi_collector = DefiDataCollector()

        with st.spinner("Fetching latest Ethereum block..."):
            latest_block = eth_collector.get_latest_block()
        if latest_block is None:
            st.error("Failed to fetch the latest Ethereum block.")
            return

        with st.spinner("Fetching DeFi data..."):
            defi_data = defi_collector.get_defi_data()
        if defi_data is None:
            st.error("Failed to fetch DeFi data.")
            return

        st.success(f"Latest Ethereum Block Number: {latest_block['number']}")

        # Data Processing
        st.header("🔬 Processing Data")
        st.write("""
        We process the collected data to calculate risk scores. The risk score is determined by:
        
        1. Volatility (40% weight): Measures price fluctuations
        2. Volume to Market Cap ratio (60% weight): Indicates liquidity and trading activity
        
        Risk Score Formula:
        ```
        Risk Score = (Volatility * 0.4 + (Total Volume / Market Cap) * 0.6) * 100
        ```
        
        Risk Labels:
        - Low: 0-33
        - Medium: 34-66
        - High: 67-100
        """)

        with st.spinner("Processing data..."):
            df = DataProcessor.process_defi_data(defi_data)
            df = DataProcessor.calculate_risk_score(df)

        # Machine Learning Model
        st.header("🤖 Training Machine Learning Model")
        st.write("""
        We use a Random Forest Classifier to predict risk labels based on:
        - Market Cap
        - Total Volume
        - Volatility

        The model is trained on 80% of the data and tested on the remaining 20%.
        """)

        risk_model = RiskModel()
        X = df[['market_cap', 'total_volume', 'volatility']]
        y = df['risk_label']
        
        with st.spinner("Training model..."):
            accuracy = risk_model.train(X, y)

        st.success(f"Model Accuracy: {accuracy:.2f}")

        # User Input for Prediction
        st.header("🔮 Predict Risk Label")
        st.info("Use the sliders below to input values for risk prediction:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            market_cap = st.number_input("Market Cap ($):", min_value=0.0, format="%.2f")
        with col2:
            total_volume = st.number_input("Total Volume ($):", min_value=0.0, format="%.2f")
        with col3:
            volatility = st.number_input("Volatility (0-1):", min_value=0.0, max_value=1.0, format="%.2f")

        if st.button("Predict Risk"):
            input_data = [[market_cap, total_volume, volatility]]
            prediction = risk_model.predict(input_data)
            st.success(f"Predicted Risk Label: {prediction[0]}")

        # Streamlit Dashboard
        st.header("📊 Interactive Dashboard")
        st.write("""
        Explore the visualizations below to gain insights into the DeFi market and risk distribution.
        """)
        
        run_dashboard(df)

    except Exception as e:
        st.error(f"Error during execution: {e}")

if __name__ == "__main__":
    main()