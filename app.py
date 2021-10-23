import streamlit as st
import pandas as pd
import altair as alt
st.markdown('# Hackaton project')

df=pd.read_csv('https://raw.githubusercontent.com/napoles-uach/Nanostring/main/Kidney_Sample_Annotations.csv')

st.write(df.head())

segment=st.sidebar.radio('SegmentLabel',['Geometric Segment', 'Pankle','Neg'])
st.markdown('SegmentLabel: '+segment)

slidename=st.sidebar.text_input('SlideName')
st.markdown('SlideName: '+slidename)

df1=df[['ROICoordinateX','ROICoordinateY','SlideName','pathology']]

df1=df1[df1['SlideName']=='normal3']

c = alt.Chart(df1).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology')

st.altair_chart(c, use_container_width=True)