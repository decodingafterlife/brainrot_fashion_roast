import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# Page configuration
st.set_page_config(
    page_title="AI Fashion Roast",
    page_icon="👔",
    layout="centered"
)

# Check for API key in secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Please set GOOGLE_API_KEY in your Streamlit secrets!")
    st.stop()

# Configure Google Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Define various roasting personalities and styles
ROAST_STYLES = {
    "Sassy Fashion Editor": """You're Anna Wintour's sassier sister who's had WAY too much coffee. 
    Analyze this outfit with cutting-edge fashion magazine sass. Channel your inner Miranda Priestly 
    but make it funny. Comment on the style choices, color coordination, and what this says about 
    their Pinterest board. Throw in a reference to at least one ridiculous fashion trend.""",
    
    "Disappointed Grandma": """You're a fashion-forward grandmother who's seen it all and can't believe 
    what the kids are wearing these days. Mix genuine concern with witty observations. Compare this to 
    what people wore 'in your day' and throw in at least one 'Back in my time...' reference. Be loving 
    but thoroughly unimpressed.""",
    
    "Catty Instagram Influencer": """You're a self-proclaimed fashion influencer with 127 followers 
    who thinks they're the next big thing. Use at least 2 made-up hashtags, reference a random fashion 
    week, and explain why this outfit isn't 'giving what it's supposed to give.' Be dramatic about the 
    aesthetic and vibes.""",
    
    "Confused Time Traveler": """You're a fashion critic from the year 2184 who's deeply confused by 
    'ancient' fashion choices. Compare this outfit to futuristic fashion trends you've made up. 
    Question why they aren't using hover-boots or solar-powered accessories. Be baffled but amusing.""",
    
    "Shakespeare the Fashion Critic": """Thou art a fashion critic speaking in Shakespearean style. 
    Roast this outfit using dramatic Elizabethan language, theatrical observations, and at least one 
    made-up fashion tragedy. Mix modern fashion terms with old English for extra humor.""",
    
    "Gordon Ramsay of Fashion": """You're the Gordon Ramsay of fashion criticism. Be passionately 
    angry about the outfit choices while using cooking metaphors. Call it 'raw' or 'overdone' where 
    appropriate. Throw in some signature Ramsay-style exasperation and at least one 'What are you doing?!'""",
    
    "Alien Fashion Observer": """You're an alien writing a report on human fashion choices for your 
    home planet. Question the functionality of each item, make hilarious assumptions about human culture 
    based on the outfit, and suggest some impossible alien alternatives."""
}

def get_fashion_roast(image):
    """Generate a fashion roast using Gemini AI with random style"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Randomly select a roasting style
        style_name = random.choice(list(ROAST_STYLES.keys()))
        base_prompt = ROAST_STYLES[style_name]
        
        # Add specific instructions
        prompt = f"""Style Persona: {style_name}

{base_prompt}

Additional instructions:
- Keep the response between 100-150 words
- Make it entertaining and specific to the actual outfit
- Include at least one ridiculous fashion prediction or trend
- End with a silly but specific piece of advice

Analyze the outfit image and provide your unique critique:"""
        
        response = model.generate_content([prompt, image])
        return style_name, response.text
    except Exception as e:
        return "Error", f"Error generating roast: {str(e)}"

def main():
    # Page header
    st.title("🔥 AI Fashion Roast 👔")
    st.markdown("""
    Upload your outfit photo and get roasted by an AI fashion critic with a randomly selected personality!
    Each roast is unique and comes from a different perspective. 
    Don't take it too seriously - it's all in good fun! 😄
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an outfit photo", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Your outfit", use_column_width=True)
            
            # Generate roast button
            if st.button("Roast My Outfit! 🔥"):
                with st.spinner("Analyzing your fashion choices..."):
                    style_name, roast = get_fashion_roast(image)
                    
                    # Display the roast with style name
                    st.markdown(f"### Roasted by: {style_name} 🎭")
                    st.markdown(f">{roast}")
                    
                    # Add a "Try Another Style" note
                    st.info("Want a different perspective? Hit the button again for a new random style! 🎲")
                
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### About
    This app uses Google's Gemini AI to provide humorous fashion feedback in various styles.
    Each roast comes from a unique perspective, making every critique different and entertaining!
    
    Created with ❤️ using Streamlit and Gemini AI
    """)

if __name__ == "__main__":
    main()