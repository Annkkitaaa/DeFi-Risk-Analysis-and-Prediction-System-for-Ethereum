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
    st.title("DeFi Risk Analysis and Prediction System")

    try:
        # Data Collection
        st.write("### Collecting Ethereum and DeFi Data...")
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

        st.write(f"Latest Ethereum Block Number: {latest_block['number']}")

        # Data Processing
        st.write("### Processing Data...")
        df = DataProcessor.process_defi_data(defi_data)
        df = DataProcessor.calculate_risk_score(df)

        # Machine Learning Model
        st.write("### Training Machine Learning Model for Risk Prediction...")
        risk_model = RiskModel()
        X = df[['market_cap', 'total_volume', 'volatility']]
        y = df['risk_label']
        accuracy = risk_model.train(X, y)

        st.write(f"## Model Accuracy: {accuracy:.2f}")

        # User Input for Prediction
        st.write("### Predict Risk Label")
        market_cap = st.number_input("Enter Market Cap:", min_value=0.0)
        total_volume = st.number_input("Enter Total Volume:", min_value=0.0)
        volatility = st.number_input("Enter Volatility:", min_value=0.0)

        if st.button("Predict Risk"):
            # Prepare input data for prediction
            input_data = [[market_cap, total_volume, volatility]]
            prediction = risk_model.predict(input_data)

            st.write(f"### Predicted Risk Label: {prediction[0]}")

        # Streamlit Dashboard
        st.write("### Generating Interactive Dashboard...")
        run_dashboard(df)

    except Exception as e:
        st.error(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
