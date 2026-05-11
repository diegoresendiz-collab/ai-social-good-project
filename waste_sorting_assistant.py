# ============================================================
# Section 3A: Lab 2 — Structured Data Extraction
# Adapted from the San Jose 311 waste disposal routing context
# Modified to reflect Maria's scenario: Spanish-language input,
# hazardous waste items, and multilingual resident support.
# ============================================================

!pip install -q google-generativeai
import google.generativeai as genai
from google.colab import userdata
import json
import time

genai.configure(api_key=userdata.get('GEMINI_API_KEY'))

# --- Schema: the form Gemini must fill in exactly ---
# Modified from Lab 2 to fit the waste disposal use case.
# Key change: item_types replaces waste_type to match disposal context.
# Urgency guide updated: HIGH = hazardous materials (batteries, paint, chemicals).
schema_prompt = """
Extract information from this recycling and waste disposal request.
Return ONLY valid JSON with exactly these five fields:
{
  "location": string (the street address or area described),
  "item_types": string (the types of items the resident needs to dispose of),
  "urgency": "LOW" or "MEDIUM" or "HIGH",
  "department": string (which San Jose city department should respond: e.g. "Environmental Services", "Recology San Jose", "Household Hazardous Waste Program", "Public Works"),
  "resident_language": string (language the resident wrote in, e.g. "English", "Spanish", "Vietnamese")
}
Urgency guide: LOW = common recyclables, MEDIUM = large or multiple items, HIGH = hazardous materials like batteries, paint, or chemicals.
No explanation. No markdown. JSON only.
"""

def extract_structured(message):
    m = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=schema_prompt
    )
    response = m.generate_content(message)
    time.sleep(12)  # stays under free-tier rate limit
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(raw)

# --- Test messages representing Maria's scenario ---
# Message 1: English baseline (TV, batteries, paint)
# Message 2: Spanish input — Maria's actual use case
# Message 3: Mixed ambiguous items (edge of system capability)
test_messages = [
    {
        "label": "English — Hazardous household items",
        "message": "I have an old TV, some car batteries, and leftover paint cans I need to get rid of. I live at 456 Elm St in San Jose. Not sure where to take them or if it costs anything."
    },
    {
        "label": "Spanish — Maria's scenario (paint, batteries, cleaning products)",
        "message": "Tengo pintura vieja, baterías de carro y algunos productos de limpieza que ya no uso. Vivo en la calle Berryessa. ¿Dónde los puedo llevar?"
    },
    {
        "label": "Ambiguous mixed items (mattress + propane tanks)",
        "message": "Not sure what to do with my old mattress, a broken microwave, and some empty propane tanks. I'm in the Alum Rock area. Can the city pick these up?"
    }
]

for item in test_messages:
    print(f"=== {item['label']} ===")
    print(f"Input: {item['message']}")
    result = extract_structured(item["message"])
    print("Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()

###############################################

# ============================================================
# Section 3B: Lab 3 — Image Recognition
# Adapted to support Maria's scenario: a resident photographs
# an item of unknown disposal category and the system returns
# a plain-language recycling recommendation.
# ============================================================

!pip install -q google-generativeai Pillow
import google.generativeai as genai
from google.colab import userdata, files
from IPython.display import display
from PIL import Image as PILImage
import time

genai.configure(api_key=userdata.get('GEMINI_API_KEY'))

# --- Custom recycling analysis prompt ---
# Modified from Lab 3's civic analysis prompt.
# Original asked: problem, impact, urgency, department.
# This version asks: item ID, material, bin assignment, special instructions.
# This directly maps to the failure point: ambiguous items that don't fit standard categories.
recycling_prompt = """
Analyze this image for recycling purposes. Return a response with exactly these four parts:

1. ITEM: What the item is
2. MATERIAL: What material it is made of
3. BIN: Which bin it belongs in — Recycling, Compost, Landfill, or Special Disposal
4. INSTRUCTIONS: Any special disposal instructions, including whether it qualifies as household hazardous waste or e-waste

Be specific. If the item could go in more than one category, explain why and recommend the safest option.
If you cannot confidently identify the item, say so clearly rather than guessing.
"""

model = genai.GenerativeModel(model_name="gemini-2.5-flash")

print("Upload a photo of an item you want to classify for recycling.")
print("Examples: a paint can, a battery, a pizza box, an old phone, a plastic bag.\n")

uploaded = files.upload()

for filename, data in uploaded.items():
    # Save and display the uploaded image
    with open(filename, "wb") as f:
        f.write(data)

    img = PILImage.open(filename)
    display(img)
    time.sleep(3)

    # Send image + prompt to Gemini
    response = model.generate_content([recycling_prompt, img])
    time.sleep(12)

    print(f"\n--- Recycling Analysis: {filename} ---")
    print(response.text)
    print()

###############################################

# ============================================================
# Section 4: Edge Case Elicitation
# Target: A user outside the assumed majority — a resident who
# writes in Mixtec (an indigenous Mexican language spoken in
# parts of East San Jose) rather than Spanish or English.
# The system was designed with Spanish and English in mind.
# This tests whether the language detection field fails,
# and whether the disposal guidance remains accurate or breaks down.
# ============================================================

import google.generativeai as genai
from google.colab import userdata
import json
import time

genai.configure(api_key=userdata.get('GEMINI_API_KEY'))

schema_prompt = """
Extract information from this recycling and waste disposal request.
Return ONLY valid JSON with exactly these five fields:
{
  "location": string (the street address or area described),
  "item_types": string (the types of items the resident needs to dispose of),
  "urgency": "LOW" or "MEDIUM" or "HIGH",
  "department": string (which San Jose city department should respond: e.g. "Environmental Services", "Recology San Jose", "Household Hazardous Waste Program", "Public Works"),
  "resident_language": string (language the resident wrote in, e.g. "English", "Spanish", "Vietnamese")
}
Urgency guide: LOW = common recyclables, MEDIUM = large or multiple items, HIGH = hazardous materials like batteries, paint, or chemicals.
No explanation. No markdown. JSON only.
"""

def extract_structured(message):
    m = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=schema_prompt
    )
    response = m.generate_content(message)
    time.sleep(12)
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(raw)

# --- Edge case prompt ---
# Mixtec is a real indigenous language spoken by a significant community
# in East San Jose. It is not Spanish. The system was not designed for it.
# This message is a rough transliteration of "I have old paint and batteries
# near Alum Rock. Where do I take them?" in Mixtec-influenced phrasing.
# The goal: does the system misidentify the language as Spanish?
# Does it still route correctly, or does it fail silently?

edge_case_message = "Ndi kuu nuu pintura vieja xaan batteries kuachi. Na'a Alum Rock. ¿Ndi kuu sa'a ra?"

print("=== Edge Case: Mixtec-influenced message ===")
print(f"Input: {edge_case_message}\n")

result = extract_structured(edge_case_message)
print("Output:")
print(json.dumps(result, indent=2, ensure_ascii=False))
