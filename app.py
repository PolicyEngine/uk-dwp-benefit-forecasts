import streamlit as st
import pandas as pd
from charts import create_benefit_chart

st.title("Benefit caseload and spending data")

st.markdown(
    "This interactive dashboard shows the forecasted caseloads and spending for different benefits by the Department for Work and Pensions' annual data releases, which can be found [here](https://www.gov.uk/government/collections/benefit-expenditure-tables)."
)

# Load the data
df = pd.read_csv("data/benefits.csv")

# Create a list of benefits
benefits = df.Benefit.unique()
benefit = st.selectbox(
    "Select a benefit",
    benefits,
    index=list(benefits).index("Universal Credit"),
)

spending = create_benefit_chart(df, benefit, spending=True)
st.plotly_chart(spending)

caseloads = create_benefit_chart(df, benefit, spending=False)
st.plotly_chart(caseloads)

# Allow download of the data

st.download_button(
    label="Download data as CSV",
    data=df.to_csv(index=False),
    file_name="benefits.csv",
    mime="text/csv",
)
