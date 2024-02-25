#source .venv/bin/activate
#python -m streamlit run Photo_Metadata.py
#http://localhost:8501/?analytics=on
# ----------------------Importing libraries----------------------
#rom ast import Not
#from curses import KEY_MAX
from matplotlib import container
from pyparsing import col
from requests import session
import streamlit as st
import pandas as pd
import base64
import re
import io
import zipfile  
import time
from metadata import generate_video_metadata
import streamlit_analytics
import os 
import streamlit as st



# ----------------------Page config--------------------------------------

st.set_page_config(page_title="Generate Metadata for stock images and videos",page_icon="random",layout="wide",initial_sidebar_state="expanded")
st.write("")
st.sidebar.header("VIDEO - Title and Description Generator")

# ----------------------Analytics section--------------------------------
try:
    analytic_pass = os.environ.get('ANALYTIC_PASS')
except FileNotFoundError as e: 
    analytic_pass = st.secrets["ANALYTIC_PASS"]
streamlit_analytics.start_tracking()


if "counter" not in st.session_state:
    st.session_state.counter = 0
no_free = 5

    

# ----------------------Sidebar section--------------------------------


try:
    st.session_state.Free_API_Key = st.secrets["API_KEY"]
except FileNotFoundError as e:
    st.session_state.Free_API_Key = os.environ.get('OPENAI_API')
            



st.image("PicturePerfectKeywords.jpg", width=100)
st.header("Videos Metadata Generator")
st.markdown("#### Generate titles, descriptions and keywords for stock Videos")
tabMetadata, tabPlaygoround = st.tabs(["Generate Image Metadata", "Try for FREE in Playground"])


#--------------------------------------------------Upload Images and Enter API key--------------------------------------------------
with tabMetadata:
    with st.container(border = True):
        st.markdown("#### Start by entering your OpenAI API key and uploading Videos")
        
        colAPI, colUpload = st.columns([1, 5])
    with colAPI:
        st.text_input("1.Enter your OpenAI API key", type="password", key="API_Key")
        st.caption(
                "No OpenAI API key? Get yours [here!](https://openai.com/blog/api-no-waitlist/)")
    with colUpload:
        uploaded_files = st.file_uploader("2.Upload Video",  type=["mp4", "avi", "mov"], accept_multiple_files=True, key="basic_gen")
    col_show, col_show_len, col_empty_1 = st.columns([3, 3, 7])
    with col_show:
        show_button = st.button("Show Uploaded Images", key="basic_gen_01", help="Click to show uploaded images")
    with col_show_len:
        st.write(f"Number of uploaded images: {len(uploaded_files)}")

    if uploaded_files is not None and show_button:
        for uploaded_file in uploaded_files:
            video_bytes = uploaded_file.read()
            st.video(video_bytes)
            

    total_price = 0
    total_time = 0
    proc_time = 0
    
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
            columns=["Filename", "Title", "Keywords" , "Category", "Releases"],
        )
    if 'df_Shutter_vid' not in st.session_state:
        st.session_state.df_Shutter_vid = pd.DataFrame(
            columns=["Filename", "Description" , "Keywords" , "Categories" , "Illustration", "Mature Content" ,  "Editorial"],
        )
        
#--------------------------------------------------Generate Titles, Descriptions and Keywords--------------------------------------------------
    with st.container(border = True):
        st.markdown("#### Generated Titles, Descriptions and Keywords")
        button = ""
        if not uploaded_files and not st.session_state.API_Key:
            a_button = st.button("If you want to generate Titles,.. --> Upload Videos and Enter API key", key="basic_gen_02")
            if a_button:
                st.write("Upload Images and Enter API key")
        elif not uploaded_files:
            b_button = st.button("If you want to generate Titles,... --> Upload Videos", key="basic_gen_03")
            if b_button:
                st.write("Upload Videos")
        elif not st.session_state.API_Key:
            c_button = st.button("If you want to generate Titles,... --> Enter API key", key="basic_gen_04")
            if c_button:
                st.write("Enter API key")
        else:
            button = st.button("Generate Video Titles, Descriptions", key="basic_gen_05" )

        prompt = ""

        keywords = ""
        keywords_true = ""
        keywords_output = ""
        keywords_button = ""
        prompt_auto = f"""
                        These are frames of an uploaded video\r
                        As the helpful Digital Asset Metadata Manager, analyze the following frames.\r
                        Generate  title and description from this frames.\r
                        Folow below guidelines.\r
                        Titles are accurate, relevant, descriptive and precise, around 60 characters long, and include 1-3 strong keywords.\r
                        Titles include descriptive language and strong adjectives and positive emotions.\r
                        Example of title 1:'Happy family enjoying a picnic in the park' , Example of title 2:'Stunning landscape photo of a mountain range'\r
                        Descriptions accurately represent photo, are concise and to the point. Include a variety of keywords, long-tail and short-tail keywords.\r
                        Descriptions use strong verbs and descriptive language and are up to 200 characters long.\r
                        Example of description 1:'Colorful sunset over the ocean with waves crashing against the shore.' , Example of description 2:'Aerial view of a city skyline at night with a river in the foreground.'\r
                        \n
                        OUTPUT in the following FORMAT:\r
                        Title: "This is the title."\r
                        Description: "This is a description."\r
                        """
        
        # Offer the option to upload a text file containing a prompt
        if st.checkbox("Use your own prompt for more granular control", key="basic-checkbox_prompt_01"):
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
                        These are frames of a video\r
                        As the helpful Digital Asset Metadata Manager, analyze the following frames.\r
                        Generate  title and description from this frames.\r
                        Folow below guidelines.\r
                        Titles are accurate, relevant, descriptive and precise, around 60 characters long, and include 1-3 strong keywords.\r
                        Titles include descriptive language and strong adjectives and positive emotions.\r
                        Example of title 1:'Happy family enjoying a picnic in the park' , Example of title 2:'Stunning landscape photo of a mountain range'\r
                        Descriptions accurately represent photo, are concise and to the point. Include a variety of keywords, long-tail and short-tail keywords.\r
                        Descriptions use strong verbs and descriptive language and are up to 200 characters long.\r
                        Example of description 1:'Colorful sunset over the ocean with waves crashing against the shore.' , Example of description 2:'Aerial view of a city skyline at night with a river in the foreground.'\r
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
    
    with st.container(border = True):
        if uploaded_files and button and st.session_state.API_Key and len(uploaded_files) > 0:
            for uploaded_file in uploaded_files:
                with st.spinner('Wait for it... Generating titles and descriptions...'):
                    uploaded_file.seek(0)
                    start_time = time.time()
                    title_video_beta, video_description, keywords, output = generate_video_metadata(uploaded_file, prompt, st.session_state.API_Key)
                    
                    end_time = time.time()
                    proc_time= end_time - start_time
                    # To display the uploaded video after analysis, you might need to reset and read again
                    uploaded_file.seek(0)
                    st.write(f"{title_video_beta} - Was Title Generated for file: {uploaded_file.name}  |  Title Generated in {proc_time:.2f} seconds")
                    st.write("-----------------------------------------------------------------------------------------------------------------")
                    st.write("Orginal OUTPUT from the model")
                    st.write(output)
                    st.session_state.df_qHero_vid.loc[len(st.session_state.df_qHero_vid)] = [uploaded_file.name, title_video_beta, video_description, keywords]
                    st.session_state.df_EPS_vid.loc[len(st.session_state.df_EPS_vid)] = [uploaded_file.name, "", video_description, "", "", title_video_beta, keywords]
                    st.session_state.df_Adobe_vid.loc[len(st.session_state.df_Adobe_vid)] = [uploaded_file.name, title_video_beta, keywords, "", ""]
                    st.session_state.df_Shutter_vid.loc[len(st.session_state.df_Shutter_vid)] = [uploaded_file.name, title_video_beta, keywords, "", "", "", ""]

            
        
        
            
       

    
    
    with st.container(border=True):
        st.markdown("#### Results")
        st.table(st.session_state.df_qHero_vid)
        st.write(f"Total price: ${total_price:.5f}  |  Total time: {total_time:.2f} seconds")

    if  len(st.session_state.df_qHero_vid) > 0:
        with st.container(border=True):
            st.markdown("#### Download the results in CSV file/s")
            st.text("Select which CSV you want to download")
            colqHero, colEPS, colAdobe, colShutter = st.columns(4)
            with colqHero:
                qHero = st.checkbox('qHero')
                CSV_file_name_qHero = st.text_input("Name CSV file name", placeholder="You can leave empty", key="basic_qHero")
                if qHero:
                    csv_qHero = st.session_state.df_qHero_vid.to_csv(index=False).encode('utf-8')
                    filename_qHero = CSV_file_name_qHero + ".csv" if CSV_file_name_qHero else "qHero_file.csv"
                    st.download_button(
                    label="Download qHero CSV",
                    data=csv_qHero,
                    file_name=filename_qHero
            )
            with colEPS:
                EPS = st.checkbox('EPS')
                CSV_file_name_EPS = st.text_input("Name CSV file name", placeholder="You can leave empty", key="basic_EPS")
                if EPS:
                    csv_EPS = st.session_state.df_EPS_vid.to_csv(index=False).encode('utf-8')
                    filename_EPS = CSV_file_name_qHero + ".csv" if CSV_file_name_qHero else "EPS_file.csv"
                    st.download_button(
                    label="Download EPS CSV",
                    data=csv_EPS,
                    file_name=filename_EPS
                    )
            with colAdobe:
                Adobe = st.checkbox('Adobe')
                CSV_file_name_Adobe = st.text_input("Name CSV file name", placeholder="You can leave empty", key="basic_Adobe")
                if Adobe:
                    csv_Adobe = st.session_state.df_Adobe_vid.to_csv(index=False).encode('utf-8')
                    filename_Adobe = CSV_file_name_Adobe + ".csv" if CSV_file_name_Adobe else "Adobe_file.csv"
                    st.download_button(
                    label="Download Adobe CSV",
                    data=csv_Adobe,
                    file_name=filename_Adobe
                    )
            with colShutter:
                Shutter = st.checkbox('Shutter')
                CSV_file_name_Shutter = st.text_input("Name CSV file name", placeholder="You can leave empty", key="basic_Shutter")
                if Shutter:
                    csv_Shutter = st.session_state.df_Shutter_vid.to_csv(index=False).encode('utf-8')
                    filename_Shutter = CSV_file_name_Shutter + ".csv" if CSV_file_name_Shutter else "Shutter_file.csv"
                    st.download_button(
                    label="Download Shutter CSV",
                    data=csv_Shutter,
                    file_name=filename_Shutter
                    )

    
streamlit_analytics.stop_tracking(unsafe_password = analytic_pass)

             
