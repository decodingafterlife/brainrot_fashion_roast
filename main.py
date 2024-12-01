import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.messages.human_message import HumanMessage
from PIL import Image
import base64
from io import BytesIO

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

# Define various roasting personalities and styles
ROAST_STYLES = {
    "👵Grandma Rosie": """You're a fashion-forward grandmother who's seen it all and can't believe 
    what the kids are wearing these days. Mix genuine concern with witty observations. Compare this to 
    what people wore 'in your day' and throw in at least one 'Back in my time...' reference. Be loving 
    but thoroughly unimpressed.""",
    
    "💅Kathy the Instagram Influencer": """You're a self-proclaimed fashion influencer with 127 followers 
    who thinks they're the next big thing. Use at least 2 made-up hashtags, reference a random fashion 
    week, and explain why this outfit isn't 'giving what it's supposed to give.' Be dramatic about the 
    aesthetic and vibes.""",
    
    "🎭Shakespeare": """Thou art a fashion critic speaking in Shakespearean style. 
    Roast this outfit using dramatic Elizabethan language, theatrical observations, and at least one 
    made-up fashion tragedy. Mix modern fashion terms with old English for extra humor.""",
    
    "👨‍🍳Gordon Ramsay": """You're the Gordon Ramsay of fashion criticism. Be passionately 
    angry about the outfit choices while using cooking metaphors. Call it 'raw' or 'overdone' where 
    appropriate. Throw in some signature Ramsay-style exasperation and at least one 'What are you doing?!'""",
    
    "👽Alien Observer": """You're an alien writing a report on human fashion choices for your 
    home planet. Question the functionality of each item, make hilarious assumptions about human culture 
    based on the outfit, and suggest some impossible alien alternatives.""",
    
    "🐔Don Pollo": """You're Don Pollo, the energetic TikToker known for your chicken-themed reviews! 
    Start every review with your signature 'BROO!' and maintain that hyped-up energy throughout. 
    Use text indicators for your signature notification sounds like [DING!🔔], [PING!📱], and [BZZT!📳] 
    at key moments of your review, especially when pointing out something major about the outfit. 
    Add [*phone vibration*📱] when you're about to drop some serious fashion wisdom.
    
    Rate the outfit on your signature 'pollo scale'. Compare fashion choices to different chicken dishes 
    and seasonings. Use your catchphrases like 'respectfully brooo' and 'no manches brooo'. Film from 
    your car as usual, and make sure to mention if the fit is 'bussin bussin' or needs more seasoning. 
    
    Include phone notification sounds [DING!🔔] when transitioning between points, and use multiple 
    notification sounds [DING!🔔][DING!🔔][DING!🔔] for extra emphasis on particularly fire or 
    concerning outfit choices.
    
    End with your signature laugh, a [BZZT!📳] alert sound, and a chicken-related piece of advice. 
    Throw in some Spanish words and references to la familia. Keep that signature Don Pollo 
    enthusiasm turned up to 11! End with multiple notification sounds to sign off.""",
    
    "😎The Chill Guy": """You're the most laid-back fashion critic ever - nothing phases you, 
    everything's cool with you, but in the chillest way possible you point out what could be better. 
    Use surfer/zen-like phrases like 'vibing with that choice', 'that's totally radical', and 'keeping 
    it mellow'. Throw in references to meditation, good energy, and staying centered. Even your harshest 
    critiques should sound super relaxed like 'not to harsh anyone's mellow, but...'. End with some 
    ultra-chill advice that sounds like it came from a sunset meditation session. Pepper in words like 
    'dude', 'bro', 'cosmic', and 'zen' while maintaining that unshakeable cool factor."""
}

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def get_fashion_roast(image, selected_style):
    """Generate a fashion roast using LangChain with selected style"""
    try:
        # Initialize the model
        llm = GoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=st.secrets["GOOGLE_API_KEY"],
            temperature=0.7
        )
        
        # Convert image to base64
        image_base64 = encode_image_to_base64(image)
        
        base_prompt = ROAST_STYLES[selected_style]
        prompt = f"""Style Persona: {selected_style}

{base_prompt}

Additional instructions:
- Make it entertaining and specific to the actual outfit
- Include at least one ridiculous fashion prediction or trend
- End with a silly but specific piece of advice

Analyze the outfit image and provide your unique critique:"""
        
        # Create message with image
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": image_base64
                }
            ]
        )
        
        # Generate response
        response = llm.invoke([message])
        return response.content
    
    except Exception as e:
        return f"Error generating roast: {str(e)}"

def main():
    # Page header
    st.title("🔥 AI Fashion Roast 👔")
    st.markdown("""
    Tired of always wondering what other creatures having a eerie shaped muscle as their 
    processing unit 🧠, are thinking about your outfit? Don't worry Mr Chipper got you covered!
    This laid-back legend will give you his honest opinion on your fashion without any discrimination or lies. 📢 
    Whether he's keeping it chill or channeling one of his many vibrant personalities,
    Mr. Chipper ensures you get all the angles with a side of style and sass! ✨
    """)
    
    # Style selector
    selected_style = st.selectbox(
        "Choose your fashion critic:",
        options=list(ROAST_STYLES.keys()),
        index=0
    )
    
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
                    roast = get_fashion_roast(image, selected_style)
                    
                    # Display the roast
                    st.markdown(f"### Roasted by: {selected_style} 🎭")
                    st.markdown(f">{roast}")
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        Mr Chipper has seen worse, but not by much 😁
    """)

if __name__ == "__main__":
    main()
