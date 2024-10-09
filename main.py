import logging
from data_collection import web_scraper, ethereum_data_fetcher, data_storage
from data_analysis import data_processing, statistical_analysis, visualization
from machine_learning import risk_prediction_model, sentiment_analysis, time_series_forecasting
from risk_scoring import risk_algorithm, smart_contract_analyzer
from blockchain import blockchain_integration
from ui import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting DeFi Risk Analysis and Prediction System")
    
    # Initialize components
    # Data collection
    scraper = web_scraper.WebScraper()
    eth_fetcher = ethereum_data_fetcher.EthereumDataFetcher()
    db = data_storage.Database()
    
    # Data analysis
    processor = data_processing.DataProcessor()
    analyzer = statistical_analysis.StatisticalAnalyzer()
    visualizer = visualization.Visualizer()
    
    # Machine learning
    risk_model = risk_prediction_model.RiskPredictionModel()
    sentiment_analyzer = sentiment_analysis.SentimentAnalyzer()
    forecaster = time_series_forecasting.TimeSeriesForecaster()
    
    # Risk scoring
    risk_scorer = risk_algorithm.RiskScorer()
    contract_analyzer = smart_contract_analyzer.SmartContractAnalyzer()
    
    # Blockchain integration
    blockchain = blockchain_integration.BlockchainIntegration()
    
    # Start the UI
    app.run()

if __name__ == "__main__":
    main()