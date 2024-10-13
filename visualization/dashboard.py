import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    # Replace this with your actual data loading logic
    df = pd.read_csv('your_data_file.csv')
    df['market_cap'] = pd.to_numeric(df['market_cap'], errors='coerce')
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce')
    return df

def format_value(value):
    if value >= 1e9:
        return f'${value/1e9:.1f}B'
    elif value >= 1e6:
        return f'${value/1e6:.1f}M'
    else:
        return f'${value:.0f}'

def run_dashboard():
    st.title("DeFi Protocol Data Dashboard")

    df = load_data()

    if df.empty:
        st.error("No data available. Please check your data source.")
        return

    st.write("## Data Overview")
    st.dataframe(df)

    st.write("## Dashboard Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Risk Distribution")
        risk_distribution = df['risk_label'].value_counts()
        fig = px.pie(values=risk_distribution.values, names=risk_distribution.index, title="Risk Distribution")
        st.plotly_chart(fig)

    with col2:
        st.write("### Top 10 Protocols by Market Cap")
        top_10 = df.nlargest(10, 'market_cap')
        fig = go.Figure(data=[go.Bar(x=top_10['name'], y=top_10['market_cap'])])
        fig.update_layout(
            title="Top 10 Protocols by Market Cap",
            xaxis_title="Protocol Name",
            yaxis_title="Market Cap (USD)",
            xaxis_tickangle=-45
        )
        fig.update_traces(text=[format_value(x) for x in top_10['market_cap']], textposition='outside')
        st.plotly_chart(fig)

    st.write("### Risk Score vs Market Cap")
    fig = px.scatter(df, x='market_cap', y='risk_score', hover_data=['name'])
    fig.update_layout(
        title="Risk Score vs Market Cap",
        xaxis_title="Market Cap (USD)",
        yaxis_title="Risk Score"
    )
    st.plotly_chart(fig)