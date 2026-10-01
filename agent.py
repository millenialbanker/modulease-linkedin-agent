import os
import random
import json
from google import genai
import requests
from PIL import Image, ImageDraw, ImageFont

# Initialize Gemini Client using the GEMINI_API_KEY environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

PROMPTS = [
    "Write a short, punchy LinkedIn post about the 'depreciating asset trap' of buying office furniture and IT hardware upfront. Emphasize why flexible EaaS tenures and mid-term swaps protect cash flow.",
    "Write a short, punchy LinkedIn post about tracking depreciating assets across multi-floor managed workspaces using UHF RFID and mobile QR codes for instant maintenance reporting."
]

def generate_post_content():
    prompt = random.choice(PROMPTS)
    system_instruction = (
        "You are an elite B2B LinkedIn growth agent for Modulease EaaS. "
        "Write in short sentences, maximum white space, bold hooks in the first 2 lines, "
        "zero fluff, ending with an engagement question."
    )
    
    # Updated to use gemini-3.8-flash as requested by the API error
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        ),
    )
    return response.text

def create_branded_image(hook_text):
    # Create a 1200x627 LinkedIn-optimized graphic with your brand colors
    img = Image.new("RGB", (1200, 627), color="#0f172a") # Dark Slate background
    draw = ImageDraw.Draw(img)
    
    # Draw an amber accent bar on the left edge (#f59e0b)
    draw.rectangle([0, 0, 20, 627], fill="#f59e0b")
    
    # Paste Logo if available in the repository root directory
    if os.path.exists("logo.png"):
        logo = Image.open("logo.png").convert("RGBA")
        logo.thumbnail((120, 120))
        img.paste(logo, (80, 80), logo)

    try:
        font_large = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    except:
        font_large = ImageFont.load_default()

    # Brand title watermark text in Electric Blue (#3b82f6)
    draw.text((80, 240), "MODULEASE EaaS", fill="#3b82f6", font=font_large)
    
    image_path = "post_graphic.png"
    img.save(image_path)
    return image_path

def post_to_linkedin(text, image_path):
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.environ.get("LINKEDIN_AUTHOR_URN") # urn:li:organization:145241250
    
    url = "https://api.linkedin.com/rest/posts"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202601"
    }
    
    payload = {
        "author": author_urn,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "searchable": True,
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByCreator": False
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code in [200, 201]:
        print("Success! Post published live to LinkedIn company page.")
    else:
        print(f"Failed to post. Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    print("Generating post content via Gemini...")
    caption = generate_post_content()
    
    print("Creating branded graphic image...")
    graphic = create_branded_image(caption.split('\n')[0])
    
    print("Dispatching live post to LinkedIn...")
    post_to_linkedin(caption, graphic)
