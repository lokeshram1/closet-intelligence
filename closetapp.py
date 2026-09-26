import base64
import json
import streamlit as st  # Standard naming for Streamlit
from openai import OpenAI
from pydantic import BaseModel
from typing import List

# 1. Enforce the exact JSON structure using Pydantic
class RetailItem(BaseModel):
    item_description: str
    confidence: str

class OutfitRecommendation(BaseModel):
    outfit_number: int
    outfit_name: str
    retail_item_to_buy: str
    owned_items_to_pair: List[str]
    stylist_rationale: str

class ClosetComplementResponse(BaseModel):
    detected_retail_items: List[RetailItem]
    outfit_recommendations: List[OutfitRecommendation]

# Helper function to convert the uploaded file to a base64 string for OpenAI
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

def get_style_recommendations(uploaded_file, owned_wardrobe):
    client = OpenAI() # Automatically reads OPENAI_API_KEY from the terminal environment
    base64_image = encode_image(uploaded_file)
    
    system_prompt = f"""
    You are the AI engine for 'ClosetComplement,' an intelligent visual personal stylist application. 
    Analyze the retail rack image, compare it against the user's owned wardrobe, and generate three cohesive outfit recommendations.

    ### USER PROFILE (Owned Wardrobe)
    The user already owns these items in their closet at home:
    {owned_wardrobe}
    """

    user_instructions = (
        "Identify up to 5 prominent garments in the image. Create exactly THREE unique outfit combinations. "
        "Each outfit must combine at least one item from the retail image and at least one item from their owned wardrobe."
    )

    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_instructions},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        response_format=ClosetComplementResponse,
    )
    return response.choices.message.content

# --- STREAMLIT WEB INTERFACE ---
st.set_page_config(page_title="ClosetComplement AI", page_icon="👗", layout="centered")

st.title("👗 ClosetComplement AI Stylist")
st.write("Upload a picture of a clothing rack at a store, list what you own at home, and let AI build your outfits!")

# Section 1: User's Digital Closet
st.subheader("1. What's in your closet at home?")
user_closet = st.text_area(
    "List your favorite baseline items (one per line):",
    value="1. Bright pink blazer\n2. White knit sweater\n3. Blue denim jeans\n4. Black leather boots"
)

# Section 2: Store Photo Upload
st.subheader("2. Upload Store Rack Photo")
uploaded_image = st.file_uploader("Choose a photo of a clothing rack...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    st.image(uploaded_image, caption="Your Store Photo", use_container_width=True)

# Section 3: Trigger the AI Engine
if st.button("✨ Generate Outfit Recommendations", type="primary"):
    if uploaded_image is None:
        st.error("Please upload an image first!")
    else:
        with st.spinner("Analyzing style and matching colors..."):
            try:
                raw_json_string = get_style_recommendations(uploaded_image, user_closet)
                data = json.loads(raw_json_string)
                
                st.success("Analysis Complete!")
                st.subheader("🔍 Items Detected on the Rack")
                for item in data.get("detected_retail_items", []):
                    st.markdown(f"- **{item['item_description']}** *(Confidence: {item['confidence']})*")
                
                st.subheader("🛍️ Your Personalized Outfits")
                for outfit in data.get("outfit_recommendations", []):
                    with st.expander(f"Look {outfit['outfit_number']}: {outfit['outfit_name']}", expanded=True):
                        st.markdown(f"🛒 **What to buy:** {outfit['retail_item_to_buy']}")
                        st.markdown(f"🏡 **Pair it with your:** {', '.join(outfit['owned_items_to_pair'])}")
                        st.info(f"💡 *Stylist Note:* {outfit['stylist_rationale']}")
                        
            except Exception as e:
                st.error(f"An error occurred: {e}")
