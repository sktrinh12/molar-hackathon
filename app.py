import streamlit as st
import pandas as pd
st.markdown('# Hackaton project')

df=pd.read_csv('https://raw.githubusercontent.com/napoles-uach/Nanostring/main/Kidney_Sample_Annotations.csv')

st.write(df.head())

