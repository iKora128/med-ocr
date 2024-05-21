from PIL import Image, ImageEnhance
import base64
from openai import OpenAI 
import json
import pandas as pd
import io
import streamlit as st

# Set the API key and model name
MODEL = "gpt-4o"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_ROLE_CONTENT = """
Please output only JSON without any extra output.
This is a health checkup result. Please analyze it and output it in JSON format.
Additionally, provide a property for reference values, and insert null if there is no value.
Ensure to cover all data.
Please start to 
{
  "results": [
    {
"""


def image_processing(image: Image, contrast_factor: float = 2.0) -> Image:
    """Convert image to grayscale, enhance contrast, and sharpen."""
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(contrast_factor)
    sharpener = ImageEnhance.Sharpness(enhanced_image)
    processed_image = sharpener.enhance(2.0)
    return processed_image

def encode_image(image: Image) -> str:
    """Encode PIL Image to base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def create_message(system_role: str, base64_image: str):
    """Create message for OpenAI API."""
    message = [
        {
            'role': 'system',
            'content': system_role
        },
        {
            'role': 'user',
            'content': [
                {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}
            }
            ]
        }
    ]
    return message

def img_to_json(image: Image):
    """Generate description for the image using GPT-4."""
    image_base64 = encode_image(image)
    messages = create_message(SYSTEM_ROLE_CONTENT, image_base64)
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content

def json_to_csv(json_data: str, output_path: str) -> pd.DataFrame:
    """Convert JSON string to CSV file."""
    try:
        data = json.loads(json_data)
        dataframe = pd.json_normalize(data['results'], sep='_')
        print(dataframe)
        dataframe.to_csv(output_path, index=False)
        print(f"CSV file saved as {output_path}")

        return dataframe
    
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def img_to_csv(image: Image, csv_output_path: str):
    """Main function to process image and print CSV content."""
    csv_content = img_to_json(image)
    print(csv_content)
    dataframe = json_to_csv(csv_content, csv_output_path)
    
    return dataframe

if __name__ == "__main__":
    img_path = "./images/採血結果_demo.jpg"
    output_path = "/Users/nagashimadaichi/Work/AI_experience/OCR/checkup_results.csv"
    img = Image.open(img_path)
    img_to_csv(img_path, output_path)

    