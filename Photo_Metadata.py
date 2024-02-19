#source .venv/bin/activate
#python -m streamlit run Photo_Metadata.py
#http://localhost:8501/?analytics=on
# ----------------------Importing libraries----------------------
#rom ast import Not
#from curses import KEY_MAX
from matplotlib import container
from requests import session
import streamlit as st
import pandas as pd
import base64
import re
import io
import zipfile  
import time
from metadata import generate_image_metadata
import streamlit_analytics
import os 
import streamlit as st



# ----------------------Page config--------------------------------------

st.set_page_config(page_title="Generate Metadata for stock images and videos",page_icon="random",layout="wide",initial_sidebar_state="expanded")
st.write("")
st.sidebar.header("PHOTO - Title and Description Generator")

# ----------------------Analytics section--------------------------------
try:
    analytic_pass = os.environ.get('ANALYTIC_PASS')
except FileNotFoundError as e: 
    analytic_pass = st.secrets["ANALYTIC_PASS"]
streamlit_analytics.start_tracking()


if "counter" not in st.session_state:
    st.session_state.counter = 0
    
if 'api_key_prompt_shown' not in st.session_state:
    st.session_state.api_key_prompt_shown = False
    
if "API_Key" not in st.session_state:
    st.session_state.API_Key = None
    
def increment():
    st.session_state.counter += 1
# ----------------------Sidebar section--------------------------------
no_free = 5

try:
    st.session_state.Free_API_Key = st.secrets["API_KEY"]
except FileNotFoundError as e:
    st.session_state.Free_API_Key = os.environ.get('OPENAI_API')
            



st.image("PicturePerfectKeywords.jpg", width=100)
st.header("Generate titles, descriptions and keywords for stock photos")
tabMetadata, tabFree , tabPlaygoround = st.tabs(["Generate Image Metadata", "Try for FREE" , "Playground"])

with tabMetadata:
    with st.container(border = True):
        st.markdown("#### Start by entering your OpenAI API key and uploading images")
        
        colAPI, colUpload = st.columns([1, 5])
    with colAPI:
        st.text_input("1.Enter your OpenAI API key", type="password", key="API_Key")
        st.caption(
                "No OpenAI API key? Get yours [here!](https://openai.com/blog/api-no-waitlist/)")
    with colUpload:
        uploaded_files = st.file_uploader("2.Upload Images",  type=["jpeg", "png","jpg"], accept_multiple_files=True, key="basic_gen")
    col_show, col_show_len, col_empty_1 = st.columns([3, 3, 7])
    with col_show:
        show_button = st.button("Show Uploaded Images", key="basic_gen_01", help="Click to show uploaded images")
    with col_show_len:
        st.write(f"Number of uploaded images: {len(uploaded_files)}")
        if uploaded_files:
            st.write(f"Number of uploaded images: {len(uploaded_files)}")
    if uploaded_files is not None and show_button:
        for uploaded_file in uploaded_files:
            st.image(uploaded_file, caption=f"Uploaded {uploaded_file.name}", use_column_width=True)
            

    total_price = 0
    total_time = 0
    proc_time = 0
    
    if 'df_EPS' not in st.session_state:
        st.session_state.df_EPS = pd.DataFrame(
            columns=["file name", "created date", "description", "country", "brief code", "title", "keywords"],
    )

    if 'df_qHero' not in st.session_state:
        st.session_state.df_qHero = pd.DataFrame(
            columns=["file name", "title", "description", "keywords"],
        )
    
    if 'df_Adobe' not in st.session_state:
        st.session_state.df_Adobe = pd.DataFrame(
            columns=["Filename", "Title", "Keywords" , "Category", "Releases"],
        )
    if 'df_Shutter' not in st.session_state:
        st.session_state.df_Shutter = pd.DataFrame(
            columns=["Filename", "Description" , "Keywords" , "Categories" , "Illustration", "Mature Content" ,  "Editorial"],
        )
    with st.container(border = True):
        st.markdown("#### Generated Titles, Descriptions and Keywords")
        button = ""
        if not uploaded_files and not st.session_state.API_Key:
            a_button = st.button("If you want to generate Titles,.. --> Upload Images and Enter API key", key="basic_gen_02")
            if a_button:
                st.write("Upload Images and Enter API key")
        elif not uploaded_files:
            b_button = st.button("If you want to generate Titles,... --> Upload Images", key="basic_gen_03")
            if b_button:
                st.write("Upload Images")
        elif not st.session_state.API_Key:
            c_button = st.button("If you want to generate Titles,... --> Enter API key", key="basic_gen_04")
            if c_button:
                st.write("Enter API key")
        else:
            button = st.button("Generate Photo Titles, Descriptions", key="basic_gen_05")

        prompt = ""

        keywords = ""
        keywords_true = ""
        keywords_output = ""
        keywords_button = ""
        prompt_auto = f"""
                        Analyze the following image and generate search engine optimized titles and descriptions for stock photography.\r
                        Titles are accurate, relevant, descriptive and precise, around 60 characters long, and include 1-3 strong keywords.\r
                        Titles include descriptive language and strong verbs.\r
                        Examples 1:'Happy family enjoying a picnic in the park' , Examples 2:'Stunning landscape photo of a mountain range'\r
                        Descriptions accurately represent photo, are concise and to the point. Include a variety of keywords, long-tail and short-tail keywords.\r
                        Descriptions use strong verbs and descriptive language and are up to 200 characters long.\r
                        Examples 1:'Colorful sunset over the ocean with waves crashing against the shore.' , Examples 2:'Aerial view of a city skyline at night with a river in the foreground.'
                        \r
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
                        As the helpful Digital Asset Metadata Manager, analyze the following image and generate search engine optimized titles and descriptions for stock photography.\r
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
    
    with st.container(border = True):
        if uploaded_files and button and st.session_state.API_Key:
            for uploaded_file in uploaded_files:
                with st.spinner('Wait for it... Generating titles and descriptions...'):
                    start_time = time.time()
                    title_auto_beta, description, keywords, price = generate_image_metadata(uploaded_file, prompt_auto, st.session_state.API_Key)
                    st.session_state.counter += 1
                
                    end_time = time.time()
                    proc_time = end_time - start_time
                    total_time = total_time + proc_time
                    total_price = total_price + price
                    st.write(f"{title_auto_beta[0:40]} - Was Title Generated for file: {uploaded_file.name}  |  Title Generated in {proc_time:.2f} seconds  |  Price: ${price}")
                    st.session_state.df_qHero.loc[len(st.session_state.df_qHero)] = [uploaded_file.name, title_auto_beta, description, keywords]
                    st.session_state.df_EPS.loc[len(st.session_state.df_EPS)] = [uploaded_file.name, "", description, "", "", title_auto_beta, keywords]
                    st.session_state.df_Adobe.loc[len(st.session_state.df_Adobe)] = [uploaded_file.name, title_auto_beta, keywords, "", ""]
                    st.session_state.df_Shutter.loc[len(st.session_state.df_Shutter)] = [uploaded_file.name, title_auto_beta, keywords, "", "", "", ""]
        
            
       
    
    streamlit_analytics.stop_tracking(unsafe_password = analytic_pass)
    
    with st.container(border = True):
        st.markdown("#### Results")
        st.table(st.session_state.df_qHero)
        st.write(f"Total price: ${total_price:.5f}  |  Total time: {total_time:.2f} seconds")
    st.write("-------------------------------------------------------------------")
    if uploaded_files and button and st.session_state.API_Key:
        with st.container(border = True):
            st.markdown("#### Download the results in CSV file/s")
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
                        csv_qHero = st.session_state.df_qHero.to_csv(index=False).encode('utf-8')
                        filename_qHero = CSV_file_name_qHero + ".csv" if CSV_file_name_qHero else "qHero_file.csv"
                        add_csv_to_zip(zip_file, csv_qHero, filename_qHero)

                    if EPS:
                        csv_EPS = st.session_state.df_EPS.to_csv(index=False).encode('utf-8')
                        filename_EPS = CSV_file_name_EPS + ".csv" if CSV_file_name_EPS else "EPS_file.csv"
                        add_csv_to_zip(zip_file, csv_EPS, filename_EPS)

                    if Adobe:
                        csv_Adobe = st.session_state.df_Adobe.to_csv(index=False).encode('utf-8')
                        filename_Adobe = CSV_file_name_Adobe + ".csv" if CSV_file_name_Adobe else "Adobe_file.csv"
                        add_csv_to_zip(zip_file, csv_Adobe, filename_Adobe)

                    if Shutter:
                        csv_Shutter = st.session_state.df_Shutter.to_csv(index=False).encode('utf-8')
                        filename_Shutter = CSV_file_name_Shutter + ".csv" if CSV_file_name_Shutter else "Shutter_file.csv"
                        add_csv_to_zip(zip_file, csv_Shutter, filename_Shutter)

                # Reset buffer's position to the beginning
                zip_buffer.seek(0)

                # Download button for the ZIP file
                st.download_button(
                    label="Download Selected CSV files as ZIP",
                    data=zip_buffer,
                    file_name="all_csv_files.zip",
                    mime="application/zip"
                )

with tabFree:
    st.write("this is for free")
    

    if uploaded_files and button and st.session_state.API_Key:
        for uploaded_file in uploaded_files:
            with st.spinner('Wait for it... Generating titles and descriptions...'):
                start_time = time.time()
                title_auto_beta, description, keywords, price = generate_image_metadata(uploaded_file, prompt_auto, st.session_state.API_Key)
                st.session_state.counter += 1
               
                end_time = time.time()
                proc_time = end_time - start_time
                total_time = total_time + proc_time
                total_price = total_price + price
                st.write(f"{title_auto_beta} - Was Title Generated for file: {uploaded_file.name}  |  Title Generated in {proc_time:.2f} seconds  |  Price: ${price}")
                st.session_state.df_qHero.loc[len(st.session_state.df_qHero)] = [uploaded_file.name, title_auto_beta, description, keywords]
                st.session_state.df_EPS.loc[len(st.session_state.df_EPS)] = [uploaded_file.name, "", description, "", "", title_auto_beta, keywords]
                st.session_state.df_Adobe.loc[len(st.session_state.df_Adobe)] = [uploaded_file.name, title_auto_beta, keywords, "", ""]
                st.session_state.df_Shutter.loc[len(st.session_state.df_Shutter)] = [uploaded_file.name, title_auto_beta, keywords, "", "", "", ""]
    
        
       







with tabPlaygoround:
    st.markdown("""#### Basic introduction to promt engineering
                 - Here is a basic introdiction how to write efficient promt for GPT-4 Vision.
                 - Play with different options and see how the model responds.
                 - Copy-paste the generated prompt to the Metadata tab and see how the model performs.
                """)
    col_title_lenght, col_middle, col_description_lenght = st.columns(3)
    title_lenght = 40 
    description_lenght = 100
    with col_title_lenght:
        title_lenght = st.select_slider("Title lenght", options=["Short", "Medium", "Long"], key="advanced-slider_1")
        if title_lenght == "Short":
            title_lenght = 40
        elif title_lenght == "Medium":  
            title_lenght = 100
        else:
            title_lenght = 250
                
    with col_description_lenght:    
        description_lenght = st.select_slider("Description lenght", options=["Short", "Medium", "Long"], key="advanced-slider_2")
        if description_lenght == "Short":
            description_lenght = 100
        elif description_lenght == "Medium":
            description_lenght = 250
        else:
            description_lenght = 500

    prompt_context = """
    As the helpful Stock Photography Assistant, analyze the following image and generate search engine optimised titles and descriptions for stock photography."""
                
    prompt_title = f"""
    Titles are accurate, relevant, descriptive and precise, around {title_lenght} characters long, and include 1-3 strong keywords. 
    Titles include descriptive language and strong verbs. 
    Examples 1:'Happy family enjoying a picnic in the park' , Examples 2:'Stunning landscape photo of a mountain range'"""

    prompt_description = f"""
    Descriptions accurately represents photo, are concice and to the point. Include variety of keywords, long-tail and short-tail keywords. 
    Descriptions use strong verbs and descriptive language and are up to {description_lenght} characters long. Use most elevant words to generate description.
    Examples 1:'Colorful sunset over the ocean with waves crashing against the shore.' , Examples 2:'Aerial view of a city skyline at night with a river in the foreground.'"""
    
    prompt_topic = ""
    prompt_person = ""
    keywords = ""
    keywords_true = ""
    keywords_output = ""
    keywords_button = ""
                
    col3, colage, colnum = st.columns(3)
    with col3:
        prompt_ethnicity = ""
        ethnicities = ["Black", "East Asian", "Hispanic", "White", "Middle Eastern", 
                       "Multiracial person", "Multiracial Group", "Native American", 
                       "Pacific Islander", "South Asian", "Southeast Asian"]
        # Using multiselect for multiple selections
        selected_ethnicities = st.multiselect("Select ethnicity", ethnicities)
        if selected_ethnicities:
            # Creating a prompt using the selected ethnicities
            prompt_ethnicity = f"""Use keyword in square bracket {selected_ethnicities} to assign ethnicity of the person, when there is a person in the image or group. Also use this as a keyword."""
    
    with colage:
        prompt_age = ""
        age = ["Baby","Child","Teenager","Young Adult", "Adult", "Adult only","Mature adult" "Senior Adult", "Multigenerational"]
        selected_age = st.multiselect("Select Age", age)
        joined_age = ', '.join(selected_age)
        if selected_age:
            prompt_age = f"""USE {joined_age} to assign age of the person, when there is a person in the image, and also use {joined_age} as a keyword."""
            
    with colnum:
        prompt_person = ""
        number_people = ["No person","One person","Two People","Group of people", "Diverse group"]
        selected_num = st.multiselect("Select Number of People", number_people)
        joined_num = ', '.join(selected_num)
        if selected_num:
            prompt_person = f"""USE {joined_num} to assign number of people, when there is a person or a group in the image, and also use {joined_num} as a keyword."""
            
    colaudi, coltopic = st.columns(2)
    with colaudi:
        prompt_audience = ""
        prompt_audie = st.text_area(
            "Prompt Audience",
            placeholder="This photos are meant for travel bloggers",
            value="",
        )
        if prompt_audie:
            prompt_audience = f"""This is the audience to whome this pictures are important,{prompt_audie}"""

    with coltopic:
        topic_main = ""
        prompt_topic = st.text_area(
            "Topic",
            placeholder="Woman on a holiday in Slovenian mountain cuntry Kranjska Gora",
        )    
        if prompt_topic:
            topic_main =f"""Topic of the photo is {prompt_topic}, use this to generate titles,descriptions and keywords."""
                                
    if st.checkbox("Include Keywords in a List", key="advanced-checkbox_keywords"):
        keywords_output = """Keywords: "there are keywords" """
        keywords_button = " And Keywords"
        keywords = st.text_area("Optionaly include keywords", key="advanced-keywords_01")
        keywords_true = f"""
        Generate a maximum of 50 keywords, and don’t include technical data.
        Arrange keywords in order of importance. First more relevan are simple one-word keywords that are in the title and description.
        If there are any keywords in the square brackets, you MUST USE them, to generate keywords list:[{keywords}].
        Do NOT use from square brackets for help to generate titles and descriptions.""" 
    
    prompt_output = f"""
    OUTPUT in the following FORMAT:
    Title: "This is the title."
    Description: "This is a description."
    {keywords_output}"""
            
    prompt_structure = f"""{prompt_context}\n{prompt_title}\n{prompt_description}{topic_main}{prompt_person}{prompt_ethnicity}{prompt_age}{keywords_true}{prompt_audience}\n{prompt_output}"""
    prompt_play = f"""{prompt_context}\n{prompt_title}\n{prompt_description}{topic_main}{prompt_person}{prompt_ethnicity}{prompt_age}{keywords_true}{prompt_audience}"""
    st.text_area("Generated Prompt - To update Press CTRL+ENTER !", height=550, value=f"""{prompt_play}""")

