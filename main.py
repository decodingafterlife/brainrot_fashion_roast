

import google.generativeai as genai
import PIL.Image

# # Configure Google Gemini API
GOOGLE_API_KEY = '****'  # Replace with your API key
genai.configure(api_key=GOOGLE_API_KEY)

def roast_fashion(image_path):
    # Load the image
    image = PIL.Image.open(image_path)
    
    # Load model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create the prompt
    prompt = """You are a fashion critic with a witty sense of humor. 
    Roast this outfit in a funny way. Focus on the style choices, 
    color combinations, and overall look. Keep it under 100 words and make it entertaining."""
    
    # Generate the roast
    response = model.generate_content([prompt, image])
    return response.text


image_path = "image1.jpg"  
roast = roast_fashion(image_path)
print(roast)
