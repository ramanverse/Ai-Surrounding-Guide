import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# We use the standard OpenAI client, but we point it at Groq's servers!
api_key = os.getenv("GROQ_API_KEY") or "missing_key_to_prevent_crash"
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

async def generate_scene_description(image_bytes: bytes, spatial_data: list, mime_type: str) -> str:
    # Vision models on this standard require the image to be encoded as a base64 string
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = f"""
    You are an assistive AI for a visually impaired user. 
    I am providing you with an image of their surroundings, along with sensor data from a fast but imperfect object detection model.
    
    Sensor Data:
    {spatial_data}
    
    Task: 
    1. Look at the image to verify the sensor data. Correct any obvious mistakes (e.g. if the sensor says 'refrigerator' but it is clearly a 'cupboard').
    2. Write a clear, concise, natural 1-2 sentence description of the scene. 
    3. State what the object is, where it is (left/center/right), and how close it is.
    4. Do not mention bounding boxes, coordinates, or the sensor data directly. Speak naturally.
    """
    
    try:
        # We call Meta's Llama 3.2 Vision model, processed by Groq's high-speed chips
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Groq API failed! Error: {str(e)}")
        # Our trusty Mock Offline Mode fallback
        if spatial_data and len(spatial_data) > 0:
            first = spatial_data[0]
            return f"[Offline Mode] I detect a {first['label']} in the {first['spatial_context']['direction']}, and it is {first['spatial_context']['proximity']}."
        return "[Offline Mode] The path appears clear."