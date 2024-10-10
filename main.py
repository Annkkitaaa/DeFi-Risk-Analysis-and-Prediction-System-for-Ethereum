import sys
import os
import streamlit as st

# Add the current directory to Python's module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import custom modules
from data_collection.ethereum_data import EthereumDataCollector
from data_collection.defi_api import DefiDataCollector
from data_processing.processor import DataProcessor
from ml_model.risk_model import RiskModel
from visualization.dashboard import run_dashboard

def main():
    # Set the title and sidebar
    st.set_page_config(page_title="DeFi Risk Analysis", page_icon="🔍")
    st.title("DeFi Risk Analysis and Prediction System")
    
    # Sidebar for navigation
    st.sidebar.header("Navigation")
    st.sidebar.text("Explore the functionalities:")
    st.sidebar.markdown("[Data Collection](#collecting-ethereum-and-defi-data)")
    st.sidebar.markdown("[Risk Prediction](#predict-risk-label)")
    st.sidebar.markdown("[Dashboard](#generating-interactive-dashboard)")

    try:
        # Data Collection
        st.write("### Collecting Ethereum and DeFi Data")
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

        st.success(f"Latest Ethereum Block Number: {latest_block['number']}")

        # Data Processing
        st.write("### Processing Data")
        df = DataProcessor.process_defi_data(defi_data)
        df = DataProcessor.calculate_risk_score(df)

        # Machine Learning Model
        st.write("### Training Machine Learning Model for Risk Prediction")
        risk_model = RiskModel()
        X = df[['market_cap', 'total_volume', 'volatility']]
        y = df['risk_label']
        accuracy = risk_model.train(X, y)

        st.success(f"## Model Accuracy: {accuracy:.2f}")

        # User Input for Prediction
        st.write("### Predict Risk Label")
        st.info("Use the sliders below to input values for risk prediction:")
        market_cap = st.number_input("Enter Market Cap:", min_value=0.0, format="%.2f")
        total_volume = st.number_input("Enter Total Volume:", min_value=0.0, format="%.2f")
        volatility = st.number_input("Enter Volatility:", min_value=0.0, format="%.2f")

        if st.button("Predict Risk"):
            # Prepare input data for prediction
            input_data = [[market_cap, total_volume, volatility]]
            prediction = risk_model.predict(input_data)

            st.success(f"### Predicted Risk Label: {prediction[0]}")

        # Streamlit Dashboard
        st.write("### Generating Interactive Dashboard")
        run_dashboard(df)

    except Exception as e:
        st.error(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
