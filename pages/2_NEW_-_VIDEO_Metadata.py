#from itertools import count
from requests import session
import streamlit as st 
from llm_calls import generate_image_title_description_streamlit_api, classify_images, analyze_video
from metadata import generate_video_metadata
import base64
import pandas as pd
#import re
#import json
#import ast
import time
import streamlit_analytics
import os 
import zipfile
import io



st.set_page_config(page_icon="random",layout="wide",initial_sidebar_state="expanded")

st.image("PicturePerfectKeywords.jpg", width=100)
st.header("Generate titles, descriptions and keywords for stock Videos")
st.sidebar.header("NEW - VIDEO  Title and Description Generator")

#analytic_pass = os.environ.get('ANALYTIC_PASS')
analytic_pass = st.secrets["ANALYTIC_PASS"]
streamlit_analytics.start_tracking()

if "video_counter" not in st.session_state:
    st.session_state.video_counter = 0

def video_increment():
    st.session_state.video_counter += 1


no_calls = 3

key_choice = st.sidebar.radio(
    "",
    (
         "Your Key",
        "Free Key (capped)",
    ),
    horizontal=True,
)

if key_choice == "Your Key":

    API_Key = st.sidebar.text_input(
        "First, enter your OpenAI API key", type="password", key="API_Key"
    )

elif key_choice == "Free Key (capped)":

    if  key_choice == "Free Key (capped)":
        try:
            
            API_Key = st.secrets["API_KEY"]
        except FileNotFoundError as e:
            API_Key = os.environ.get('OPENAI_API')
        
        st.sidebar.caption(f"""## {st.session_state.video_counter}/{no_calls} - OpenAI API calls used""")
        
    else:
        API_Key = os.environ.get('OPENAI_API')


image_arrow = st.sidebar.image(
        "Gifs/arrow_small_new.gif",
)

if key_choice == "Free Key (capped)":

    image_arrow.empty()

else:

    st.write("")

    st.sidebar.caption(
        "No OpenAI API key? Get yours [here!](https://openai.com/blog/api-no-waitlist/)"
    )
    pass

if st.session_state.video_counter == no_calls :
    st.write("You have used 3 API calls. Please enter your own API key or use the free key.")
    API_Key = st.sidebar.text_input(
        "First, enter your OpenAI API key", type="password", key="Used_API_Key")

tabMetadata, tabPlaygoround = st.tabs(["Generate Video Metadata", "Playground"])

prompt = f"""
As the helpful Digital Asset Metadata Manager, analyze frames from uploaded video  and Generate a compelling title and description that I can upload along with the video on istocks.\r
                    Titles are accurate, relevant, descriptive and precise, around 60 characters long, and include 1-3 strong keywords.\r
                    Titles include descriptive language and strong verbs.\r
                    Examples 1:'Happy family enjoying a picnic in the park' , Examples 2:'Stunning landscape photo of a mountain range'\r
                    Descriptions accurately represent photo, are concise and to the point. Include a variety of keywords, long-tail and short-tail keywords.\r
                    Descriptions use strong verbs and descriptive language and are up to 200 characters long.\r
                    Examples 1:'Colorful sunset over the ocean with waves crashing against the shore.' , Examples 2:'Aerial view of a city skyline at night with a river in the foreground.'\r
            """         

with tabMetadata:
    uploaded_file = st.file_uploader("Upload a Video", type=("mp4", "avi", "mov"))

    if uploaded_file is not None and st.button("Show Uploaded Video"):
            video_bytes = uploaded_file.read()
            st.video(video_bytes)
            

    total_price = 0
    total_time = 0
    proc_time = 0

    if not uploaded_file and not API_Key:
        button = st.button("Upload Video and Enter API key", key="basic_gen_02")
    elif not uploaded_file:
        button = st.button("Upload Video", key="basic_gen_03")
    elif not API_Key:
        button = st.button("Enter API key", key="basic_gen_04")
    else:
        button = st.button("Generate Video Titles, Descriptions", key="basic_gen_05", on_click=video_increment)
        
        
        # Initialize session state for dataframes
    if 'df_EPS_vid' not in st.session_state:
        st.session_state.df_EPS_vid = pd.DataFrame(
            columns=["file name", "created date", "description", "country", "brief code", "title", "keywords"],
        )

    if 'df_qHero_vid' not in st.session_state:
        st.session_state.df_qHero_vid = pd.DataFrame(
            columns=["file name", "title", "description", "keywords"],
        )

    if 'df_Adobe_vid' not in st.session_state:
        st.session_state.df_Adobe_vid = pd.DataFrame(
            columns=["Filename", "Title", "Keywords", "Category", "Releases"],
        )
    if 'df_Shutter_vid' not in st.session_state:
        st.session_state.df_Shutter_vid = pd.DataFrame(
            columns=["Filename", "Description", "Keywords", "Categories", "Illustration", "Mature Content", "Editorial"],
        )

    prompt = ""

    keywords = ""
    keywords_true = ""
    keywords_output = ""
    keywords_button = ""
    prompt = f"""
                    As the helpful Digital Asset Metadata Manager, analyze frames from uploaded video  and Generate a compelling title and description that I can upload along with the video on istocks.\r
                    Titles are accurate, relevant, descriptive and precise, around 60 characters long, and include 1-3 strong keywords.\r
                    Titles include descriptive language and strong verbs.\r
                    Examples 1:'Happy family enjoying a picnic in the park' , Examples 2:'Stunning landscape photo of a mountain range'\r
                    Descriptions accurately represent photo, are concise and to the point. Include a variety of keywords, long-tail and short-tail keywords.\r
                    Descriptions use strong verbs and descriptive language and are up to 200 characters long.\r
                    Examples 1:'Colorful sunset over the ocean with waves crashing against the shore.' , Examples 2:'Aerial view of a city skyline at night with a river in the foreground.'\r
                    """
    # Offer the option to upload a text file containing a prompt
    if st.checkbox("Use your own promt", key="basic-checkbox_prompt_01"):
        if st.checkbox("Include Keywords", key="basic-checkbox_keywords_01"):
            keywords_output = """Keywords: "keyword1,keyword2,..." """
            keywords_button = " And Keywords"
            keywords = st.text_area("Optionally include keywords")
            keywords_true = f"""
            Analyze the following image and generate a maximum of 50 keywords, IF YOU CAN and don’t include technical data.\r
            Arrange keywords in order of importance. First more relevant are simple one-word keywords that are in the title and description.\r
            If there are any keywords in the square brackets [{keywords}], you MUST USE them.\r
            Do NOT use keywords from square brackets for help to generate titles and descriptions."""
        with st.container(border = True):
            col_text, colCheckbox = st.columns([2, 1])
            with col_text:
                upload = st.checkbox("Upload text file with prompt")
                if upload:
                    uploaded_prompt = st.file_uploader("Upload prompt", type=("txt"))
                    # If a file is uploaded, use its content as the prompt
                    if uploaded_prompt is not None:
                        uploaded_prompt = uploaded_prompt.read().decode()
                        prompt = st.text_area("Prompt - To update Press CTRL+ENTER !", height=250, value=f"""{uploaded_prompt}""")

                else:
                    # If no file is uploaded, display a text area for manual input of the prompt
                    prompt = st.text_area("Prompt - To update Press CTRL+ENTER !", height=350, value=f"""
                    As the helpful Digital Asset Metadata Manager, analyze frames from uploaded video  and Generate a compelling title and description that I can upload along with the video on istocks.\r
                    Titles are accurate, relevant, descriptive and precise, around 60 characters long, and include 1-3 strong keywords.\r
                    Titles include descriptive language and strong verbs.\r
                    Examples 1:'Happy family enjoying a picnic in the park' , Examples 2:'Stunning landscape photo of a mountain range'\r
                    Descriptions accurately represent photo, are concise and to the point. Include a variety of keywords, long-tail and short-tail keywords.\r
                    Descriptions use strong verbs and descriptive language and are up to 200 characters long.\r
                    Examples 1:'Colorful sunset over the ocean with waves crashing against the shore.' , Examples 2:'Aerial view of a city skyline at night with a river in the foreground.'\r
                    """)
                

            prompt_out = f"""
            OUTPUT in the following FORMAT:\r
            Title: "This is the title."\r
            Description: "This is a description."\r
            {keywords_output}"""

            prompt_auto = prompt + keywords_true + prompt_out
            
            with colCheckbox:
                st.markdown("#### Check prompt going into GPT-4 Vision")
                st.write(str(prompt_auto))



    if uploaded_file and button and API_Key:
        with st.spinner('Wait for it... Generating Video titles and descriptions...'):
            # Reset the buffer to the beginning to ensure it can be read from the start
            uploaded_file.seek(0)
            start_time = time.time()
            title_video_beta, video_description, keywords = generate_video_metadata(uploaded_file, prompt, API_Key)
            
            end_time = time.time()
            proc_time= end_time - start_time
            # To display the uploaded video after analysis, you might need to reset and read again
            uploaded_file.seek(0)
            st.write(f"{title_video_beta} - Was Title Generated for file: {uploaded_file.name}  |  Title Generated in {proc_time:.2f} seconds")
            st.session_state.df_qHero_vid.loc[len(st.session_state.df_qHero_vid)] = [uploaded_file.name, title_video_beta, video_description, keywords]
            st.session_state.df_EPS_vid.loc[len(st.session_state.df_EPS_vid)] = [uploaded_file.name, "", video_description, "", "", title_video_beta, keywords]
            st.session_state.df_Adobe_vid.loc[len(st.session_state.df_Adobe_vid)] = [uploaded_file.name, title_video_beta, keywords, "", ""]
            st.session_state.df_Shutter_vid.loc[len(st.session_state.df_Shutter_vid)] = [uploaded_file.name, title_video_beta, keywords, "", "", "", ""]
            
    streamlit_analytics.stop_tracking(unsafe_password = analytic_pass)
    
    st.table(st.session_state.df_qHero_vid)
    st.write("-------------------------------------------------------------------")
    st.text("Select which CSV you want to download")
    colqHero, colEPS, colAdobe, colShutter = st.columns(4)
    with colqHero:
        qHero = st.checkbox('qHero')
        CSV_file_name_qHero = st.text_input("Name CSV file name", placeholder="You can leave empty", key="basic_qHero")
    with colEPS:
        EPS = st.checkbox('EPS')
        CSV_file_name_EPS = st.text_input("Name CSV file name", placeholder="You can leave empty", key="basic_EPS")
    with colAdobe:
        Adobe = st.checkbox('Adobe')
        CSV_file_name_Adobe = st.text_input("Name CSV file name", placeholder="You can leave empty", key="basic_Adobe")
    with colShutter:
        Shutter = st.checkbox('Shutter')
        CSV_file_name_Shutter = st.text_input("Name CSV file name", placeholder="You can leave empty", key="basic_Shutter")

    # Function to add a CSV to the ZIP
    def add_csv_to_zip(zipfile, csv_content, filename):
        zipfile.writestr(filename, csv_content)

    # Check if any condition is true and create a ZIP file
    if qHero or EPS or Adobe or Shutter:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            if qHero:
                csv_qHero = st.session_state.df_qHero_vid.to_csv(index=False).encode('utf-8')
                filename_qHero = CSV_file_name_qHero + ".csv" if CSV_file_name_qHero else "qHero_file.csv"
                add_csv_to_zip(zip_file, csv_qHero, filename_qHero)

            if EPS:
                csv_EPS = st.session_state.df_EPS_vid.to_csv(index=False).encode('utf-8')
                filename_EPS = CSV_file_name_EPS + ".csv" if CSV_file_name_EPS else "EPS_file.csv"
                add_csv_to_zip(zip_file, csv_EPS, filename_EPS)

            if Adobe:
                csv_Adobe = st.session_state.df_Adobe_vid.to_csv(index=False).encode('utf-8')
                filename_Adobe = CSV_file_name_Adobe + ".csv" if CSV_file_name_Adobe else "Adobe_file.csv"
                add_csv_to_zip(zip_file, csv_Adobe, filename_Adobe)

            if Shutter:
                csv_Shutter = st.session_state.df_Shutter_vid.to_csv(index=False).encode('utf-8')
                filename_Shutter = CSV_file_name_Shutter + ".csv" if CSV_file_name_Shutter else "Shutter_file.csv"
                add_csv_to_zip(zip_file, csv_Shutter, filename_Shutter)

        # Reset buffer's position to the beginning
        zip_buffer.seek(0)

        # Download button for the ZIP file
        st.download_button(
            label="Download All CSVs as ZIP",
            data=zip_buffer,
            file_name="all_csv_files.zip",
            mime="application/zip"
        )

   
   
   
   
with tabPlaygoround:
    st.write("Coming soon...")
    
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


