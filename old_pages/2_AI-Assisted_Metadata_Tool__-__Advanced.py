#streamlit run Hello.py
import streamlit as st 
from llm_calls import generate_image_title_description_streamlit_api 
import base64
import pandas as pd
import re

st.header("Pro-Level AI SEO: Free Stock Photo Tool")
st.write("Empower your stock photography with advanced AI SEO tools. Customize metadata for impactful online presence, all at no cost.")



st.sidebar.header("SEO Title and description")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="file_qa_api_key", type="password")
    #"[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


st.title("📝 iStock Titles and Descriptions Automatization Assistant")

st.markdown(
    """
    ### Advanced usage:
    ##### (For users who want to get a better/more specific results.)
    - Upload batch up to 50 images. Images should be in the same theme but it is not mandaroty.
    - Copy-Paste the prompt in the text area below.
    - OPTIONALY you can Upload your own prompt in .txt format.
    - (If you want to include keywords you have to do this in the prompt, like in the example below)
    - (If you do NOT want keywords you have to remove the keywords part from the prompt)
    - Download the CSV file.
    """
)



uploaded_files = st.file_uploader("Upload Images", type=("jpg", "png"), accept_multiple_files=True)


if uploaded_files is not None and st.button("Show images"):
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption='Uploaded Image')

upload = st.toggle("Upload text file with prompt")
if upload:
    uploaded_prompt = st.file_uploader("Upload prompt", type=("txt"))
    if uploaded_prompt is not None:
        prompt = uploaded_prompt.read().decode()
        
        st.write(prompt)
else: 
    prompt = st.text_area("Prompt", height=250 ,value="""As the iStock Keyword and Title Assistant, your role is to provide  SEO-friendly titles and extended descriptions for each image provided.""")

prompt = ""
prompt_out = """OUTPUT in the following FORMAT: 
    Title: "This is the title."
    Description: "This is a description."
    Keywords:  """



prompt = prompt +  prompt_out
# Initialize session state for dataframes
if 'df_EPS' not in st.session_state:
    st.session_state.df_EPS = pd.DataFrame(
        columns=["file name", "created date", "description", "country", "brief code", "title", "keywords"],
    )

if 'df_qHero' not in st.session_state:
    st.session_state.df_qHero = pd.DataFrame(
        columns=["file name", "title", "description", "keywords"],
    )


if uploaded_files and st.button("Generate") and openai_api_key:
    for uploaded_file in uploaded_files:
        uploaded_file_base64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
        with st.spinner('Wait for it... Generating titles and descriptions...'):
            try:
                output = generate_image_title_description_streamlit_api(uploaded_file_base64, prompt, openai_api_key)
                #st.write(output)
                description = re.search(r'Description: "?([^"]+)"?', output, re.IGNORECASE).group(1)
                title = re.search(r'Title: "?([^"]+)"?', output, re.IGNORECASE).group(1) 
                keywords = re.search(r"Keywords: (.+)", output, re.IGNORECASE).group(1) 
            except AttributeError:
                keywords = ""
                description = "Change prompt formatin to: \nDescription: \nTitle: \nKeywords:"
                title = "Change prompt formatin to: \nDescription: \nTitle: \nKeywords:"

            
            st.session_state.df_qHero.loc[len(st.session_state.df_qHero)] = [uploaded_file.name, title, description, keywords]
            st.session_state.df_EPS.loc[len(st.session_state.df_EPS)] = [uploaded_file.name, "", description, "", "", title, keywords]


st.table(st.session_state.df_qHero)
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


















