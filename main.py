

import google.generativeai as genai
import PIL.Image

# # Configure Google Gemini API
GOOGLE_API_KEY = 'AIzaSyCkOelRO8Rjcpo38yECFIJCVaHdK0OUYg4'  # Replace with your API key
genai.configure(api_key=GOOGLE_API_KEY)

def roast_fashion(image_path):
    # Load the image
    image = PIL.Image.open(image_path)
    
    # Load Gemini Pro Vision model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create the prompt
    prompt = """You are a fashion critic with a witty sense of humor. 
    Roast this outfit in a funny way. Focus on the style choices, 
    color combinations, and overall look. Keep it under 100 words and make it entertaining."""
    
    # Generate the roast
    response = model.generate_content([prompt, image])
    return response.text

# Test the function
image_path = "image1.jpg"  # Replace with your image path
roast = roast_fashion(image_path)
print(roast)

# models = genai.list_models()
# for model in models:
#     print(f"\nModel Name: {model.name}")
#     print(f"Display Name: {model.display_name}")
#     print(f"Description: {model.description}")
#     print(f"Generation Methods: {model.supported_generation_methods}")
#     print(f"Input Types: ", end="")
    
#     # Print supported input types
#     if hasattr(model, 'input_content_types'):
#         print(model.input_content_types)
#     else:
#         print("Text only")
        
#     print("="*50)