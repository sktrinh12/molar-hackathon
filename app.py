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

List_ROI=['disease3', 'disease4', 'normal3', 'normal4', 'disease1B',
       'disease2B', 'normal2B']

df1=df[['ROICoordinateX','ROICoordinateY','SlideName','pathology','disease_status']]

df1=df1[df1['SlideName']==List_ROI[0]]

c = alt.Chart(df1).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology',size='disease_status')

st.altair_chart(c, use_container_width=True)

# ------
df1=df[['ROICoordinateX','ROICoordinateY','SlideName','pathology','disease_status']]
df1=df1[df1['SlideName']==List_ROI[1]]

c = alt.Chart(df1).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology',size='disease_status')

st.altair_chart(c, use_container_width=True)

# ------
df1=df[['ROICoordinateX','ROICoordinateY','SlideName','pathology','disease_status']]
df1=df1[df1['SlideName']==List_ROI[2]]

c = alt.Chart(df1).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology',size='disease_status')

st.altair_chart(c, use_container_width=True)

# ------
df1=df[['ROICoordinateX','ROICoordinateY','SlideName','pathology','disease_status']]
df1=df1[df1['SlideName']==List_ROI[3]]

c = alt.Chart(df1).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology',size='disease_status')

st.altair_chart(c, use_container_width=True)

# ------
df1=df[['ROICoordinateX','ROICoordinateY','SlideName','pathology','disease_status']]
df1=df1[df1['SlideName']==List_ROI[4]]

c = alt.Chart(df1).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology',size='disease_status',title='title')

st.altair_chart(c, use_container_width=True)
# ------
df1=df[['ROICoordinateX','ROICoordinateY','SlideName','pathology','disease_status']]
df1=df1[df1['SlideName']==List_ROI[5]]

c = alt.Chart(df1).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology',size='disease_status')

st.altair_chart(c, use_container_width=True)
# ------
df1=df[['ROICoordinateX','ROICoordinateY','SlideName','pathology','disease_status']]
df1=df1[df1['SlideName']==List_ROI[6]]

c = alt.Chart(df1).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology',size='disease_status')

st.altair_chart(c, use_container_width=True)