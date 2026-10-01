import os
import random
from openai import OpenAI
import requests
from PIL import Image, ImageDraw, ImageFont

# Initialize OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Content angles rotating between depreciation/flexibility and tracking
PROMPTS = [
    "Write a short, punchy LinkedIn post about the 'depreciating asset trap' of buying office furniture and IT hardware upfront. Emphasize why flexible EaaS tenures and mid-term swaps protect cash flow.",
    "Write a short, punchy LinkedIn post about tracking depreciating assets across multi-floor managed workspaces using UHF RFID and mobile QR codes for instant maintenance reporting."
]

def generate_post_content():
    prompt = random.choice(PROMPTS)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an elite B2B LinkedIn growth agent for Modulease EaaS. Write in short sentences, maximum white space, bold hooks in the first 2 lines, zero fluff, ending with an engagement question."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def create_branded_image(hook_text):
    # Create a 1200x627 LinkedIn-optimized image with your dark slate brand color (#0f172a)
    img = Image.new("RGB", (1200, 627), color="#0f172a")
    draw = ImageDraw.Draw(img)
    
    # Draw an amber accent bar on the left edge
    draw.rectangle([0, 0, 20, 627], fill="#f59e0b")
    
    # Paste Logo if available
    if os.path.exists("logo.png"):
        logo = Image.open("logo.png").convert("RGBA")
        logo.thumbnail((120, 120))
        img.paste(logo, (80, 80), logo)

    # Add text formatting (Using default or basic system font mapping)
    try:
        font_large = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    except:
        font_large = ImageFont.load_default()

    # Wrap text roughly onto the canvas
    draw.text((80, 240), "MODULEASE EaaS", fill="#3b82f6", font=font_large)
    
    # Save output image
    image_path = "post_graphic.png"
    img.save(image_path)
    return image_path

def post_to_linkedin(text, image_path):
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.environ.get("LINKEDIN_AUTHOR_URN")  # e.g., urn:li:organization:1234567 or urn:li:person:abcdef
    
    # LinkedIn API integration code for sharing text + image content goes here
    print("Agent simulation: Post generated successfully and ready for LinkedIn API dispatch!")
    print(f"Caption:\n{text}")

if __name__ == "__main__":
    caption = generate_post_content()
    graphic = create_branded_image(caption.split('\n')[0])
    post_to_linkedin(caption, graphic)
