import re
import base64
from llm_calls import generate_image_title_description_streamlit_api_low, analyze_video
#import cv2


def generate_image_metadata(uploaded_file, prompt_basic, API_Key):
    """
    Processes an uploaded file to generate metadata including title, description, and keywords
    using a specific API. The function encodes the file in base64, sends it to the API, and parses
    the response.

    Args:
    - uploaded_file: The uploaded file object to be processed.
    - prompt_basic: The basic prompt text for the API call.
    - API_Key: The API key for authentication with the API.

    Returns:
    A tuple containing the title, description, keywords, and the price as returned by the API.
    If the API call fails or parsing fails, returns a message indicating what information was not found.
    """

    # Encode the uploaded file in base64
    uploaded_file_base64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
    
    # Initialize return values
    title_basic_beta = "No title found - Contact support"
    description = "No description found - Contact support."
    keywords = ""
    price = 0.0  # Default price, assuming API returns price as a float

    try:
        # Assuming generate_image_title_description_streamlit_api_low is a predefined function
        output_basic, price = generate_image_title_description_streamlit_api_low(uploaded_file_base64, prompt_basic, API_Key)
        #print(output_basic)
        
        # Regex search for description
        description_match = re.search(r'Description: "?([^"]+)"?', output_basic, re.IGNORECASE)
        if description_match:
            description = description_match.group(1)
        
        # Regex search for title
        title_match = re.search(r'Title: "?([^"]+)"?', output_basic, re.IGNORECASE)
        if title_match:
            title_basic_beta = title_match.group(1)
        
        # Regex search for keywords
        keywords_match = re.search(r"Keywords: (.+)", output_basic, re.IGNORECASE)
        if keywords_match:
            keywords = keywords_match.group(1)
    
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred: {e}")

    return title_basic_beta, description, keywords, price


def generate_video_metadata(uploaded_file, prompt_basic, API_Key):
    """
    Processes an uploaded video file to generate metadata including title, description, and keywords
    using a specific API. The function encodes the video file in base64, sends it to the API, and parses
    the response.

    Args:
    - uploaded_file: The uploaded video file object to be processed.
    - prompt_basic: The basic prompt text for the API call.
    - API_Key: The API key for authentication with the API.

    Returns:
    A tuple containing the title, description, keywords, and the price as returned by the API.
    If the API call fails or parsing fails, returns a message indicating what information was not found.
    """

    
    
    # Initialize return values
    title_basic_beta = "No title found - Contact support"
    description = "No description found - Contact support."
    keywords = ""
    

    try:
        # Assuming generate_image_title_description_streamlit_api_low is a predefined function
        output_basic = analyze_video(uploaded_file, API_Key, prompt_basic)
        print(output_basic)
        
        # Regex search for description
        description_match = re.search(r'Description: "?([^"]+)"?', output_basic, re.IGNORECASE)
        if description_match:
            description = description_match.group(1)
        
        # Regex search for title
        title_match = re.search(r'Title: "?([^"]+)"?', output_basic, re.IGNORECASE)
        if title_match:
            title_basic_beta = title_match.group(1)
        
        # Regex search for keywords
        keywords_match = re.search(r"Keywords: (.+)", output_basic, re.IGNORECASE)
        if keywords_match:
            keywords = keywords_match.group(1)
    
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred: {e}")

    return title_basic_beta, description, keywords
