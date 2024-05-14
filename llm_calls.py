#python -m streamlit run Hello.py
import requests
import re
from prompt_klas import gen_prompt, technology_innovation_spec, landscapes_nature_spec, urban_architecture_spec, people_lifestyle_spec, business_finance_spec, travel_world_cultures_spec, food_drink_spec, animals_wildlife_spec, health_wellness_spec, sports_recreation_spec, arts_entertainment_spec, fashion_beauty_spec
#import tiktoken
from tiktoken import encoding_for_model
import cv2 
import base64
from openai import OpenAI
#import os 
#import time
#import numpy as np
import tempfile

def count_tokens(prompt):
    encoding = encoding_for_model("gpt-4")
    num_tokens = len(encoding.encode(prompt))
    return num_tokens



def generate_image_title_description_streamlit_api_low(base64_image, prompt, openai_api_key):
  
    
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        
        "max_tokens": 300
    }

    image_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    input_prompt_tokens = count_tokens(prompt)
    #print(f"Prompt tokens: {input_prompt_tokens}")
    output_tokens = count_tokens(image_response.json()["choices"][0]["message"]["content"])
    #print(f"Output tokens: {output_tokens}")
    price = (input_prompt_tokens/1000)*0.01 + (output_tokens/1000)*0.03 + 0.00085
    #print(f"Price: ${price}")
    print(image_response.json()["choices"][0]["message"]["content"])
    return image_response.json()["choices"][0]["message"]["content"], price

  

def generate_image_title_description_streamlit_api(base64_image, prompt, openai_api_key):
    
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        
        "max_tokens": 300
    }

    image_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
   
    return image_response.json()["choices"][0]["message"]["content"]


def classify_images(base64_image, openai_api_key):
        
    
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """"Please analyze the attached image and determine its most appropriate category. It is crucial that you assign the image to exactly one of the following specified categories based on its content and characteristics. The categories are as follows:  
                                1. Landscapes and Nature, 
                                2. Urban and Architecture, 
                                3. People and Lifestyle, 
                                4. Business and Finance, 
                                5. Travel and World Cultures, 
                                6. Food and Drink, 
                                7. Animals and Wildlife, 
                                8. Health and Wellness, 
                                9. Sports and Recreation, 
                                10. Technology and Innovation, 
                                11. Arts and Entertainment, 
                                12. Fashion and Beauty.
                                Provide the category name and a brief justification for your choice based on the key elements observed in the image.
                                OUTPUT in the following FORMAT:
                                Category name: "This is a Category name."
                                Justification: "This is a Justification."
                                """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        
        "max_tokens": 300
    }

    image_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # Process the image response here
    classify = image_response.json()["choices"][0]["message"]["content"]
    #print(classify)
    category_search = re.search(r'Category name: "?([^".]+)"?', classify, re.IGNORECASE)
    
    if category_search:
        extracted_category = category_search.group(1).strip()
    else:
        # Handle the case where the category is not found in the response
        return None, "Category not found"
    #print(extracted_category)
    category_name = "Unknown Category"  # Default value for category_name

    if extracted_category == "Landscapes and Nature":
        
        category = landscapes_nature_spec()
        category_name = "Landscapes and Nature"
        
        print(category_name)
    elif extracted_category == "Urban and Architecture":
        category = urban_architecture_spec()
        category_name = "Urban and Architecture"
        print(category_name)
    elif extracted_category == "People and Lifestyle":
        category =  people_lifestyle_spec()
        category_name = "People and Lifestyle"
        print(category_name)
    elif extracted_category == "Business and Finance":  
        category = business_finance_spec()
        category_name = "Business and Finance"
        print(category_name)
    elif extracted_category == "Travel and World Cultures":
        category = travel_world_cultures_spec()
        category_name = "Travel and World Cultures"
        print(category_name)
    elif extracted_category == "Food and Drink":
        category = food_drink_spec()
        category_name = "Food and Drink"
        print(category_name)
    elif extracted_category == "Animals and Wildlife":
        category = animals_wildlife_spec()
        category_name = "Animals and Wildlife"
        print(category_name)
    elif extracted_category == "Health and Wellness":
        category = health_wellness_spec()
        category_name = "Health and Wellness" 
        print(category_name)   
    elif extracted_category == "Sports and Recreation":
        category = sports_recreation_spec()
        category_name = "Sports and Recreation"
        print(category_name)
    elif extracted_category == "Technology and Innovation":
        category = technology_innovation_spec()
        category_name = "Technology and Innovation"
        print(category_name)
    elif extracted_category == "Arts and Entertainment":
        category = arts_entertainment_spec()
        category_name = "Arts and Entertainment"
        print(category_name)
    elif extracted_category == "Fashion and Beauty":
        category = fashion_beauty_spec()
        category_name = "Fashion and Beauty"
        print(category_name)
    else:
        # Handle the case where the category is not found in the response
        return None, "Category not found"
    

    

    return category, category_name


def output_final(base64_image, openai_api_key):
    prompt_spec = classify_images(base64_image, openai_api_key)
    
    prompt = gen_prompt(prompt_spec[0][0].strip(), prompt_spec[0][1], prompt_spec[0][2], prompt_spec[0][3], prompt_spec[0][4], prompt_spec[0][5], prompt_spec[0][6], prompt_spec[0][7])
    

    return generate_image_title_description_streamlit_api(base64_image, prompt, openai_api_key), prompt_spec[1]


def analyze_video(uploaded_video_buffer, openai_api_key, prompt):
    # Write the uploaded video buffer to a temporary file
    print("This is a prompt in analyze_video" +prompt)
    print(openai_api_key)
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp4') as tmpfile:
        tmpfile.write(uploaded_video_buffer.read())
        tmpfile.flush
        video_path = tmpfile.name
        video = cv2.VideoCapture(video_path)
    print(video)
    base64Frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64_string = base64.b64encode(buffer).decode("utf-8")
        base64Frames.append(base64_string)
        

    video.release()
    print(len(base64Frames))
    # Assuming you have an OpenAI client setup
    client = OpenAI(api_key=openai_api_key)
    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                f"""{prompt}""",
                *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::200]),
            ],
        },
    ]
    params = {
        "model": "gpt-4-vision-preview",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 300,
    }
    result = client.chat.completions.create(**params)

    return result.choices[0].message.content