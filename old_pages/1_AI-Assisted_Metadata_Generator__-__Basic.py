import streamlit as st 
from llm_calls import generate_image_title_description_streamlit_api, classify_images
import base64
import pandas as pd
import re
import json
import ast


#st.set_page_config(page_title="Automatic title generator for stock photos")
st.header("Simple SEO Tool for Stock Photos - Free AI")
st.write("Streamline metadata creation with our user-friendly AI tool. Ideal for beginners, enhance your stock images' SEO quickly and for free.")
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

uploaded_files = st.file_uploader("Upload an Image", type=("jpg", "png"), accept_multiple_files=True)

if uploaded_files is not None and st.button("Show images"):
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption='Uploaded Image')



prompt_context = """As the helpful Stock Photography Assistant, analyze the following image and generate search engine optimised titles and descriptions for stock photography."""
       
prompt_title = """Titles are accurate, relevant, descriptive and precise, around 60 characters long, and include 1-3 strong keywords.
                  Titles include descriptive language and strong verbs. "
                  Examples 1:'Happy family enjoying a picnic in the park' , Examples 2:'Stunning landscape photo of a mountain range'"""


prompt_description = """Descriptions accurately represents photo, are concice and to the point. Include variety of keywords, long-tail and short-tail keywords.
            Descriptions use strong verbs and descriptive language and are up to 500 characters long. 
            Examples 1:'Colorful sunset over the ocean with waves crashing against the shore.' , Examples 2:'Aerial view of a city skyline at night with a river in the foreground.'"""
prompt_topic = ""
prompt_person= ""
keywords=""
keywords_true = ""
output_keywords = ""   
Include = st.toggle("Include Keywords")
if Include:
    output_keywords = "Keywords:"
    keywords = st.text_area("MUST include keywords!")
    keywords_true = f"""Include a maximum of 50 keywords, and don’t include technical data.
                     Arrange keywords in order of importance,Include long-tail and short-tail keywords. Use keywords from the generated Title. Also use information from topics:{prompt_topic} and person:{prompt_person} if they are given 
                    If there are any keywords in the square brackets, you MUST USE them,keywords:[{keywords}]."""

topic= st.toggle("Include topic")

topic_main =""
if topic:
        
    prompt_topic = st.text_area(
        "Topic",
        value="Woman on a holiday in Slovenian mountain cuntry Kranjska Gora",
    )    
    topic_main =f"This Topic in square brackets will help you to contextualize and help you understand the scene from the image. Use this information to  generate more relevant titles and descriptions.Topic:[{prompt_topic}]"
    
    
person = st.toggle("Include person ethniciry")
if person:
    ethnicity = st.radio("Select ethnicity", ("Black",
                                                  "East Asian",
                                                  "Hispanic",
                                                  "White",
                                                  "Middle Eastern",
                                                  "Multiracial person",
                                                  "Multiracial Group",
                                                  "Native American",
                                                  "Pacific Islander",
                                                  "South Asian",
                                                  "Southeast Asian",))
    prompt_person = st.text_area(
        "Person",
        value=f"Use {ethnicity} to assign ethnicity of the person, when there is a person in the image."
    )    

audience = st.toggle("Include Prompt Audience")
prompt_audience = ""
if audience:
    prompt_audience = st.text_area(
        "Prompt Audience",
        value= "This photos are ment for travel bloggers"
    )




  
prompt_structure = f"""{prompt_context}\n{prompt_title}\n{prompt_description} {topic_main} {prompt_person} {keywords_true} {prompt_audience}"""
st.write(prompt_structure)            
# Initialize session state for dataframes
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


if uploaded_files and st.button("Generate") and openai_api_key:
    for uploaded_file in uploaded_files:
        uploaded_file_base64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
        with st.spinner('Wait for it... Generating titles and descriptions...'):
            try:
                output = generate_image_title_description_streamlit_api(uploaded_file_base64, prompt_structure, openai_api_key)
                
                              
                

                description = re.search(r"Description: (.+)", output).group(1)
                title = re.search(r"Title: (.+)", output).group(1) 
                keywords = re.search(r"Keywords: (.+)", output).group(1) 
            except AttributeError:
                keywords = ""
            
            st.session_state.df_qHero.loc[len(st.session_state.df_qHero)] = [uploaded_file.name, title, description, keywords]
            st.session_state.df_EPS.loc[len(st.session_state.df_EPS)] = [uploaded_file.name, "", description, "", "", title, keywords]
            st.session_state.df_Adobe.loc[len(st.session_state.df_Adobe)] = [uploaded_file.name, title, keywords, "", ""]
            st.session_state.df_Shutter.loc[len(st.session_state.df_Shutter)] = [uploaded_file.name, title, keywords, "", "", "", ""]

st.table(st.session_state.df_qHero)
st.write("-------------------------------------------------------------------")
st.text("Select which CSV you want to download")

qHero = st.checkbox('qHero')
EPS = st.checkbox('EPS')
Adobe = st.checkbox('Adobe')
Shutter = st.checkbox('Shutter')


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
        
if Adobe:
    CSV_file_name_Adobe = st.text_input("Name CSV file name", placeholder="You can leave empty")
    csv = st.session_state.df_Adobe.to_csv(index=False).encode('utf-8')
    if CSV_file_name_Adobe:
        st.download_button(
        "Press to Download - EPS",
        csv,
        CSV_file_name_Adobe + ".csv",
        "text/csv",
        key='download-csv-Adobe'   
        )
    else:
        st.download_button(
        "Press to Download - Adobe",
        csv,
        "Adobe_file.csv",
        "text/csv",
        key='download-csv-Adobe'   
        )  
        
if Shutter:
    CSV_file_name_Shutter = st.text_input("Name CSV file name", placeholder="You can leave empty")
    csv = st.session_state.df_Shutter.to_csv(index=False).encode('utf-8')
    if CSV_file_name_Shutter:
        st.download_button(
        "Press to Download - Shutter",
        csv,
        CSV_file_name_Shutter + ".csv",
        "text/csv",
        key='download-csv-Shutter'   
        )
    else:
        st.download_button(
        "Press to Download - Shutter",
        csv,
        "Shutter_file.csv",
        "text/csv",
        key='download-csv-Shutter'   
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
