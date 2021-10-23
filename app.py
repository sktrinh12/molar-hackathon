import streamlit as st
import pandas as pd
st.markdown('# Hackaton project')

df=pd.read_csv('https://raw.githubusercontent.com/napoles-uach/Nanostring/main/Kidney_Sample_Annotations.csv')

st.write(df.head())

segment=st.sidebar.radio('SegmentLabel',['Geometric Segment', 'Pankle','Neg'])
st.sidebar.markdown(segment)

slidename=st.sidebar.text_input('SlideName')