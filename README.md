# DeFi Risk Analysis and Prediction System for Ethereum
## Overview

The **DeFi Risk Analysis and Prediction System** is a web application designed to collect, process, and analyze data from decentralized finance (DeFi) protocols and the Ethereum blockchain. The application leverages machine learning techniques to assess the risk levels of various DeFi assets and provide predictions based on user inputs.

## Live Demo

You can try the application live here:  
**[Live Demo](https://defi-risk-analysis-and-prediction-system-for-ethereum.streamlit.app/#generating-interactive-dashboard)**

![image](https://github.com/user-attachments/assets/a092506e-20a5-4c06-8de7-82defca53504)

![image](https://github.com/user-attachments/assets/e5dee884-bb45-414f-9258-73b1431861f9)
![image](https://github.com/user-attachments/assets/c48107c0-58d1-4bba-89ab-3bcaa1feaa5c)





## Project Structure

```
defi_risk_analysis/
│
├── data_collection/
│   ├── __init__.py
│   ├── ethereum_data.py        # Module for collecting Ethereum blockchain data
│   └── defi_api.py            # Module for collecting DeFi protocol data
│
├── data_processing/
│   ├── __init__.py
│   └── processor.py           # Module for processing and analyzing the collected data
│
├── ml_model/
│   ├── __init__.py
│   └── risk_model.py          # Module for machine learning model to assess risk levels
│
├── visualization/
│   ├── __init__.py
│   └── dashboard.py           # Module for generating interactive visualizations
│
├── main.py                    # Main application file that integrates all components
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation
```

## Features

- **Data Collection**: Collects real-time data from the Ethereum blockchain and various DeFi protocols.
- **Data Processing**: Processes collected data to calculate risk scores and prepares it for modeling.
- **Machine Learning Model**: Trains a predictive model to classify risk levels of DeFi assets based on key metrics.
- **Interactive Dashboard**: Provides visualizations and allows users to input data for risk predictions.


## Usage

To run the application, execute the following command:

```bash
streamlit run main.py
```

Once the application is running, you can access it in your web browser at `http://localhost:8501`.





