import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import altair as alt
from client import *
import pprint
st.markdown('# Hackaton project')

df1=pd.read_csv('https://raw.githubusercontent.com/napoles-uach/Nanostring/main/Kidney_Sample_Annotations.csv')
df2=pd.read_csv('https://raw.githubusercontent.com/napoles-uach/Nanostring/main/Kidney_Q3Norm_TargetCountMatrix.csv')

def header(content, font_colour, background_colour):
     st.markdown(f'<p style="background-color:{background_colour};color:{font_colour};font-size:24px;border-radius:2%;">{content}</p>', unsafe_allow_html=True)

def get_db(table_name):
    client = client_dct[table_name]
    event = client.query_database(
            types=table_name,
            limit=1000
        )
    return event

def get_eventstore(table_name):
    client = client_dct[table_name]
    event = client.view_entries()
    #print(event)
    # event = event['type', 'uuid', 'event', 'timestamp', 'alembic_version']
    return event

@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock":lambda _: None})
def init_Molar_connection():
    client_cfg = ClientConfig(
                        server_url=molar_server,
                        email=email,
                        password=password,
                        database_name=dbname1
    )

    user_client1 = Client(client_cfg)
    client_cfg = ClientConfig(
                        server_url=molar_server,
                        email=email,
                        password=password,
                        database_name=dbname2
    )
    user_client2 = Client(client_cfg)
    dct = {"kidney_sampant" : user_client1, "kidney_norm": user_client2}
    pprint.pprint(dct)
    return dct

client_dct = init_Molar_connection()

def rollback_es(client, event, id_val):
    """
    rollback table based on given the name of the table based on the id value
    """
    result = False
    rb_evt = client.rollback(before = event.at[id_val, 'timestamp'])
    return True

# st.write(df1.head())

segment=st.sidebar.radio('SegmentLabel',['Geometric Segment', 'PanCK','Neg'])
st.markdown('SegmentLabel: '+segment)

slidename=st.sidebar.text_input('SlideName')
st.markdown('SlideName: '+slidename)

List_ROI=['disease3', 'disease4', 'normal3', 'normal4', 'disease1B',
       'disease2B', 'normal2B']

# table dropdown
table_dropdown_ls = ["kidney_sampant", "kidney_norm"]
choice = st.sidebar.selectbox("Table Name", table_dropdown_ls)
data_file = st.sidebar.file_uploader("Upload Dataset (csv)", type=["csv"])

#######KIDNEY SAMPLE ANNOTATION########
header("Event store for kidney sample annotation table from Molar", "#e69138", "#444444")

es_sampant_show = get_eventstore("kidney_sampant")
st.dataframe(es_sampant_show)

#######KIDNAY Q3NORMALISED COUNT MATRIX########
header("Event store for kidney q3 normalised table from Molar", "#e69138", "#444444")
es_norm_show = get_eventstore("kidney_norm")
st.dataframe(es_norm_show)

# rollback number input
if choice == "kidney_norm":
    current_es = es_norm_show
else:
    current_es = es_sampant_show

# line break
st.sidebar.markdown("***")

if not es_norm_show.empty and not es_sampant_show.empty:
    es_id = st.sidebar.selectbox('Event Store Id:', current_es['id'])

# rollback button
if st.sidebar.button("Rollback"):
    client = client_dct[choice]
    if rollback_es(client, current_es, es_id):
        st.success(f"Rollback to {es_id} successful for {choice}")

# upload one csv file
def upload_file(df, table_name):
    client = client_dct[table_name]
    for i, r in df.iterrows():
        upload_row(client, table_name, r, True)


def upload_row(client, table_name, row, verbose=False):
    """
    upload one row at a time from a dataframe using the Molar Client API.
    Verbose will print out the json object using pprint
    """

    if table_name.endswith("sampant"):
        data={
                "SlideName": row['SlideName'],
                "ScanName": row['ScanName'],
                "ROILabel": row['ROILabel'],
                "SegmentLabel": row['SegmentLabel'],
                "SegmentDisplayName": row['SegmentDisplayName'],
                "SampleID": row['Sample_ID'],
                "AOISurfaceArea": row['AOISurfaceArea'],
                "AOINucleiCount": row['AOINucleiCount'],
                "ROICoordinateX": row['ROICoordinateX'],
                "ROICoordinateY": row['ROICoordinateY'],
                "RawReads": row['RawReads'],
                "TrimmedReads": row['TrimmedReads'],
                "StitchedReads": row['StitchedReads'],
                "AlignedReads": row['AlignedReads'],
                "DeduplicatedReads": row['DeduplicatedReads'],
                "SequencingSaturation": row['SequencingSaturation'],
                "UMIQ30": row['UMIQ30'],
                "RTSQ30": row['RTSQ30'],
                "DiseaseStatus": row['disease_status'],
                "Pathology": row['pathology'],
                "Region": row['region'],
                "LOQ": row['LOQ'],
                "NormalizationFactor": row['NormalizationFactor'],
                "ROILabel": row['ROILabel'],
            }
    else:
        data={
                "targetName": row['TargetName'],
                "ROILabel": row['ROILabel'],
                "segmentLabel": row['segmentLabel'],
                "segmentDisplayName" : row['segmentDisplayName'],
                "diseaseStatus" : row['diseaseStatus'],
                "geneExpr": row['geneExpr']
             }
    event = client.create_entry(
        type=table_name,
        data = data
    )
    if verbose:
        pprint.pprint(event)


def melt_df(df):
    """
    melt the dataframe and create new columns to fit the structure of the
    normalised data from kidney_norm table
    """

    dm = pd.melt(df, id_vars=['TargetName'], value_vars=df.columns[1:])
    dm.rename(columns = {'variable' : 'segmentDisplayName', 'value': 'geneExpr'}, inplace = True)
    dm['segmentLabel'] = dm['segmentDisplayName'].apply(lambda x: x.split('|')[2])
    dm['diseaseStatus'] = dm['segmentDisplayName'].apply(lambda x: 'DKD' if 'disease' in x.split('|')[0].split('_')[0] else 'normal')
    dm['ROILabel'] = dm['segmentDisplayName'].apply(lambda x: int(x.split('|')[1]))
    dm['SlideName'] = dm['segmentDisplayName'].apply(lambda x: x.split('|')[0].split('_')[0])
    dm['ScanName'] = dm['SlideName'].apply(lambda x: f'{x}_scan')
    return dm


st.markdown("***")
#######KIDNEY SAMPLE ANNOTATION########
header("Sample annotation data from Molar", "#3d85c6", "#444444")
df_sampant_show = get_db("kidney_sampant")
st.dataframe(df_sampant_show)

#######KIDNAY Q3NORMALISED COUNT MATRIX########
header("Q3 normalised data from Molar", "#3d85c6", "#444444")
df_norm_show = get_db("kidney_norm")
st.dataframe(df_norm_show)


if data_file is not None:
    file_details = {"filename":data_file.name, "filetype":data_file.type,
                    "filesize":data_file.size}
    st.write(file_details)
    read_df = pd.read_csv(data_file)
    if choice == "kidney_sampant":
        read_df['pathology'].fillna("", inplace=True)
    elif choice == "kidney_norm":
        read_df = melt_df(read_df)
    with st.spinner('Uploading data to Molar database...'):
        upload_file(read_df, choice)
    st.success(f"upload of {data_file} to {choice} sucessful!")

def plot_map(ii):
    st.write(List_ROI[ii])
    df_one=df1[['ROICoordinateX','ROICoordinateY','SlideName','pathology','disease_status']]

    df_one=df_one[df_one['SlideName']==List_ROI[ii]]

    c = alt.Chart(df_one).mark_circle().encode(
    x='ROICoordinateX', y='ROICoordinateY',color='pathology',size='disease_status')

    st.altair_chart(c, use_container_width=True)

def build_heatmap(slidename, df_sampant, df_norm):
    slidetype=df_sampant[df_sampant['SlideName']==slidename]
    # coord=slidetype[['ROICoordinateX','ROICoordinateY','region','AOINucleiCount','SegmentDisplayName']]
    coord=slidetype[['ROICoordinateX','ROICoordinateY','Region','AOINucleiCount','SegmentDisplayName']]
    groups=coord['SegmentDisplayName']
    groups_list=groups.to_list()
    df_norm = df_norm.pivot(index='targetName', columns='segmentDisplayName',
                            values='geneExpr')
    i=-1
    j=-1
    mat=np.zeros((int(len(groups_list)),int(len(groups_list))))
    for element1 in groups_list:
        j+=1
        i=-1
        for element2 in groups_list:
            i+=1
            vec1=np.array(df_norm[element1])
            vec2=np.array(df_norm[element2])
            v1=np.linalg.norm(vec1)
            v2=np.linalg.norm(vec2)
            mat[i][j]=np.dot(vec1,vec2)/(v1 * v2)
    mat_df = pd.DataFrame(mat, columns = groups_list,index = groups_list)
    fig = px.imshow(mat_df)
    fig.update_layout(
        title="Heatmap",
        coloraxis_colorbar=dict(
            title="Gene Expression Level"),
        xaxis_showticklabels=False,
        yaxis_showticklabels=False
    )

    return fig

st.sidebar.markdown("***")
st.sidebar.subheader("Heatmap")
choice_slidename = st.sidebar.selectbox("Slide Type", ["normal3", "disease3"])
if st.sidebar.button("Plot"):
    fig = build_heatmap(choice_slidename, df_sampant_show, df_norm_show)
    # fig = build_heatmap(choice_slidename, df1, df2)
    st.plotly_chart(fig, height=500)

# for i in range(6):
#     plot_map(i)

