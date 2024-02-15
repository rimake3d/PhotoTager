import streamlit as st 
from llm_calls import output_final
import base64
import pandas as pd
import re
import json


st.set_page_config(page_title="SEO Title,description and keywords", page_icon="📈")
st.sidebar.header("SEO Title and description")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="file_qa_api_key", type="password")

st.title("📝 iStock Titles and Descriptions Automatization Assistant")

st.markdown(
    """
    ### Basic usage:
    - Upload batch up to 50 images. Images should be in the same theme but it is not mandatory. 
    - Optionally you can select if you want to include keywords, if you do you should provide keywords in the text area below. 
    (You will get better results if you include keywords in the prompt)
    - Download the CSV file.
    """
)

keywords=""
keywords_true = ""
output_keywords = ""   
Include = st.toggle("Include Keywords")
if Include:
    output_keywords = "Keywords:"
    keywords = st.text_area("MUST include keywords!")
    keywords_true = f"""You MUST USE keywords in square brackets based on these keywords [{keywords}]."""

uploaded_files = st.file_uploader("Upload an Image", type=("jpg", "png"), accept_multiple_files=True)

if uploaded_files is not None and st.button("Show images"):
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption='Uploaded Image')
        
        
        
# Initialize session state for dataframes
if 'df_Display' not in st.session_state:
    st.session_state.df_Display = pd.DataFrame(
        columns=["file name", "title", "description", "keywords", "Category"],
    )

if 'df_EPS' not in st.session_state:
    st.session_state.df_EPS = pd.DataFrame(
        columns=["file name", "created date", "description", "country", "brief code", "title", "keywords"],
    )

if 'df_qHero' not in st.session_state:
    st.session_state.df_qHero = pd.DataFrame(
        columns=["file name", "title", "description", "keywords"],
    )

if uploaded_files and st.button("Classification") and openai_api_key:
    for uploaded_file in uploaded_files:
        uploaded_file_base64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
        with st.spinner('Wait for it... Generating titles and descriptions...'):
            
                            
            try:
                output = output_final(uploaded_file_base64, openai_api_key)
                st.write(output[0])
                    
                description = re.search(r'Description: "?([^"]+)"?', output[0], re.IGNORECASE).group(1)
                
                title = re.search(r'Title: "?([^"]+)"?', output[0], re.IGNORECASE).group(1)
                
                keywords = re.search(r"Keywords: (.+)", output[0], re.IGNORECASE).group(1) 
                
                category = output[1]
            except AttributeError:
                keywords = ""
                title = ""
                description = ""
                   
            st.session_state.df_Display.loc[len(st.session_state.df_Display)] = [uploaded_file.name, title, description, keywords, category]
            st.session_state.df_qHero.loc[len(st.session_state.df_qHero)] = [uploaded_file.name, title, description, keywords]
            st.session_state.df_EPS.loc[len(st.session_state.df_EPS)] = [uploaded_file.name, "", description, "", "", title, keywords]
                    
              
st.table(st.session_state.df_Display)
st.write("-------------------------------------------------------------------")
st.text("Select which CSV you want to download")

qHero = st.checkbox('qHero')
EPS = st.checkbox('EPS')

if qHero:
    CSV_file_name_qHero = st.text_input("Name CSV file name", placeholder="You can leave empty")
    csv = st.session_state.df_qHero.to_csv(index=False).encode('utf-8')
    if CSV_file_name_qHero:
        st.download_button(
        "Press to Download - qHero",
        csv,
        CSV_file_name_qHero + ".csv",
        "text/csv",
        key='download-csv-qHero'   
        )
    else:
        st.download_button(
        "Press to Download - qHero",
        csv,
        "qHero_file.csv",
        "text/csv",
        key='download-csv-qHero'   
        )

if EPS:
    CSV_file_name_EPS = st.text_input("Name CSV file name", placeholder="You can leave empty")
    csv = st.session_state.df_EPS.to_csv(index=False).encode('utf-8')
    if CSV_file_name_EPS:
        st.download_button(
        "Press to Download - EPS",
        csv,
        CSV_file_name_EPS + ".csv",
        "text/csv",
        key='download-csv-EPS'   
        )
    else:
        st.download_button(
        "Press to Download - EPS",
        csv,
        "EPS_file.csv",
        "text/csv",
        key='download-csv-EPS'   
        )  

#if EPS:
#    CSV_file_name_EPS = st.text_input("Name CSV file for EPS", key="EPS")
#    if st.button("Download EPS CSV"):
#        csv = st.session_state.df_EPS.to_csv(index=False).encode('utf-8')
#        st.download_button(
#            "Press to Download - EPS",
#            csv,
#            CSV_file_name_EPS + ".csv" if CSV_file_name_EPS else "EPS_file.csv",
#            "text/csv",
#            key='download-csv-EPS'
#        )
