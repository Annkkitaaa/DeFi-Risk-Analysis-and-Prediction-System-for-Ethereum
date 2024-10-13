import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run_dashboard(df):
    st.write("## DeFi Protocol Data")
    st.dataframe(df)

    st.write("## Dashboard Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### Risk Distribution")
        fig, ax = plt.subplots(figsize=(4, 4))
        df['risk_label'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title("Risk Distribution")
        st.pyplot(fig)

    with col2:
        st.write("### Top 5 Protocols by Market Cap")
        top_5 = df.nlargest(5, 'market_cap')
        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(top_5['name'], top_5['market_cap'])
        ax.set_xticklabels(top_5['name'], rotation=45, ha='right')
        ax.set_ylabel('Market Cap (USD)')
        
        def format_value(value):
            if value >= 1e9:
                return f'${value/1e9:.1f}B'
            elif value >= 1e6:
                return f'${value/1e6:.1f}M'
            else:
                return f'${value:.0f}'

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    format_value(height),
                    ha='center', va='bottom', rotation=0, fontsize=8)
        
        plt.tight_layout()
        st.pyplot(fig)

    with col3:
        st.write("### Risk Score vs Market Cap")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.scatter(df['market_cap'], df['risk_score'])
        ax.set_xlabel('Market Cap (USD)')
        ax.set_ylabel('Risk Score')
        plt.tight_layout()
        st.pyplot(fig)