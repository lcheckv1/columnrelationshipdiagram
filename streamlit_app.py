
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from io import StringIO
import xml.etree.ElementTree as et

"""
# Tableau Analyzer

Please select a .twb file to upload, then select data columns, worksheets, or dashboards on the left.
A table will appear telling you where selected columns appear as a data dependency within each worksheet or dashboard.

"""


uploaded_file=st.file_uploader("Upload a .twb.", disabled=False, label_visibility="visible")
counter=0
if uploaded_file is not None and counter==0:
    counter+=1
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    root=et.fromstring(string_data)
    #flow for worksheets

    datname=''
    calc=''
    caption=''
    columnData=pd.DataFrame(columns=['column','calculation','caption'])
    for a in root:
        for b in a:
            for c in b:
                if c.tag=='column':
                    try:
                        caption=c.attrib['caption']
                    except:
                        caption=''
                    datname=c.attrib['name']
                    for d in c:
                        if d.tag=='calculation':
                            try:
                                calc=d.attrib['formula']
                            except:
                                calc=''
                if datname!='':
                    #datarow=pd.DataFrame(data={'column': [datname], 'calcluation': [calc]})
                    new_index = len(columnData)
                    columnData.loc[new_index] = {'column': datname, 'calculation': calc,'caption':caption}
                    datname=''
                    calc=''
    
    


    df=columnData
    df2=columnData
  
    calctranslate=pd.DataFrame(columns=['oldcalc','calculation_new'])

    relationshipdf=pd.DataFrame(columns=['parentcaption','childcaption'])
    #print(df)
  
    columnname=df[['column','caption']]
    #columnname=columnname[columnname['column'].apply(lambda x: x.startswith('[Calculation_'))]         
    columnname=columnname.rename(columns={"column": "col", "caption": "cap"})

    hierarchydata=pd.DataFrame(columns=['parentName','parentCaption','childName','childCaption'])
    
    for index,row in df.iterrows():
        childcalc=(row['calculation'])
        childCaption=row['caption']
        childName=row['column']
        #basically a self-join, to determine if any/all column fields exist in the calculation
        for index,row in columnname.iterrows():
            parentName=row['col']
            parentCaption=row['cap']
            if parentName in childcalc:
                row=[parentName,parentCaption,childName,childCaption]
                hierarchydata.loc[len(calctranslate)] = row

    hierarchydata=hierarchydata.drop_duplicates()
    st.write(hierarchydata)
