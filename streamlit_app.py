import streamlit as st
import google.generativeai as genai
from PIL import Image

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

def get_fashion_roast(image):
    """Generate a fashion roast using Gemini AI"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """You are a fashion critic with a witty sense of humor. 
        Roast this outfit in a funny way. Focus on the style choices, 
        color combinations, and overall look. Keep it entertaining."""
        
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error generating roast: {str(e)}"

def main():
    # Page header
    st.title("🔥 AI Fashion Roast 👔")
    st.markdown("""
    Tired of always wondering what other creatures, having a eerie shaped musle as their 
    processing unit are thinking about your outfit? Don't worry Mr Chipper got you covered,
    he'll give an honest opinion on your fashion without any discrimination or lies!
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an outfit photo", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Your outfit", use_column_width=True)
            
            # Generate roast button
            if st.button("Rate My Outfit! 🔥"):
                with st.spinner("Analyzing your fashion choices..."):
                    roast = get_fashion_roast(image)
                    
                # Display the roast
                st.markdown("### The Verdict 🎭")
                # st.markdown(f">{roast}")
                
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    If Mr Chipper says it's bad then it's bad, if he says it's good then it's worse!
    """)

if __name__ == "__main__":
    main()
