#streamlit run Hello.py
import streamlit as st 
from llm_calls import generate_image_title_description_streamlit_api
import base64

st.header("Experiment with AI: Free SEO Playground")
st.write("Discover SEO potential for your stock images in our AI playground. Experiment with titles and descriptions freely and enhance appeal.")


st.sidebar.header("Prompt Playground")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="file_qa_api_key", type="password")
    #"[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


st.title("📝 Prompt Playground")

uploaded_file = st.file_uploader("Upload an article", type=("jpg", "png"))


if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image')

st.write("# Co-Star promt framework")


prompt_context = st.text_area(
    "Prompt Context",
    value="""As the helpful Stock Photography Assistant, analyze the following image and generate search engine optimised titles and descriptions for stock photography.""",
    height=100
    
)    

prompt_title = st.text_area(
    "Title",
    value="Titles are accurate, relevant, descriptive and precise, around 60 characters long, and include 1-3 strong keywords."
          "Titles include descriptive language and strong verbs"
          "Examples: 1.'Happy family enjoying a picnic in the park' , 2.'Stunning landscape photo of a mountain range'",
    height=200
) 

prompt_description = st.text_area(
    "Description",
    value="Descriptions accurately represents photo, are concice and to the point. Include variety of keywords, long-tail and short-tail keywords."
          "Descriptions use strong verbs and descriptive language and are up to 500 characters long "
          "Examples: 1.'Colorful sunset over the ocean with waves crashing against the shore.' , 2.'Aerial view of a city skyline at night with a river in the foreground.'",
    height=200
)


topic= st.toggle("Include topic")
prompt_topic = ""
if topic:
    prompt_topic = st.text_area(
        "Topic",
        value="This topic will help you to contextualize and help you understand the scene from the image. Use this information to  generate more relevant titles and descriptions."
    )    

person = st.toggle("Include person ethniciry")
prompt_person= ""
if person:
    prompt_person = st.text_area(
        "Person",
        placeholder="Use this information to assign ethnicity of the person when there is a person in the image."
    )    

audience = st.toggle("Include Prompt Audience")
prompt_audience = ""
if audience:
    prompt_audience = st.text_area(
        "Prompt Audience",
        placeholder="This photos are ment for travel bloggers"
    )




if prompt_context and prompt_objective and  prompt_responce:
    prompt_structure = f"""{prompt_context} {prompt_title} {prompt_description} {prompt_topic} {prompt_person} {prompt_audience}"""

st.markdown(
    """
    #### You can aditionaly change the structure of the prompt below. 
    
       
    """
)
st.text_area(
    "Prompt assembled with CO-Star framework",
    value=prompt_structure,
    height=300,
    key="prompt_structure",
    help="The structure of the prompt. You can change this if you want to customize the prompt.",
)

st.markdown(
    """
     
    ###### When you are happy with the prompt structure, you can download it and use it in your project.
       
    """
)

st.download_button(
    label="Download Prompt",
    data=prompt_structure,
    file_name="prompt.txt",
    mime="text/plain",
)


st.write("# OUTPUT")

if uploaded_file and prompt_structure and st.button("Generate") and openai_api_key:
    with st.spinner('Wait for it...'):

    # Convert uploaded_file to base64
        uploaded_file_base64 = base64.b64encode(uploaded_file.read()).decode('utf-8')

        output = generate_image_title_description_streamlit_api(uploaded_file_base64, prompt_structure, openai_api_key)
    st.success('Done!')
    
    
    st.write(output)




