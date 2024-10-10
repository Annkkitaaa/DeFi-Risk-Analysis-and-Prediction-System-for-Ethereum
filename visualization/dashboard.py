import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run_dashboard(df):
    st.title("DeFi Risk Analysis Dashboard")

    st.write("## DeFi Protocol Data")
    st.dataframe(df)

    st.write("## Risk Distribution")
    fig, ax = plt.subplots()
    df['risk_label'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

    st.write("## Top 10 Protocols by Market Cap")
    top_10 = df.nlargest(10, 'market_cap')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_10['name'], top_10['market_cap'])
    ax.set_xticklabels(top_10['name'], rotation=45, ha='right')
    ax.set_ylabel('Market Cap (USD)')
    st.pyplot(fig)

    st.write("## Risk Score vs Market Cap")
    fig, ax = plt.subplots()
    ax.scatter(df['market_cap'], df['risk_score'])
    ax.set_xlabel('Market Cap (USD)')
    ax.set_ylabel('Risk Score')
    st.pyplot(fig)