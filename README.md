## Problem — Who is affected, and what specifically breaks down for them today?
## AI Capability — Which lab capability addresses the failure point, and why does it fit?
## Workflow — What goes in, what does the AI do, what comes out, and who acts on the output? Include screenshots of output
## Failure Case — One specific failure, with a reference to the lab output that showed it is possible.
## Oversight and Tradeoff — Where does human review sit, and what does the one change cost 

# AI Waste Sorting Assistant (San Jose)

## Team Members
- Diego Resendiz
- Alexa Gonzalez
- Rory Wilson


## Problem

This project focuses on tenants living in multi-unit apartment buildings in San Jose who are trying to dispose of household waste correctly but are unsure which items belong in recycling, compost, or landfill. The failure point is not a lack of information, but that existing waste-sorting rules are difficult to interpret at the moment of disposal. For example, items like greasy pizza boxes, plastic-lined cups, or biodegradable plastics create confusion, leading to incorrect sorting. This results in contamination of recycling streams and inefficiencies in waste management. This problem aligns with UN SDG 11: Sustainable Cities and Communities.


## AI Capability

This system uses two AI capabilities demonstrated in the labs:

- **Structured Data Extraction (Lab 2):** Converts user text input into structured categories (recycling, compost, landfill). This helps users quickly understand how to sort multiple items at once.
- **Image Recognition (Lab 3):** Analyzes uploaded images of waste or bins, identifies objects, and determines urgency and recommended actions.

These capabilities directly address the failure point by transforming confusing or unclear waste information into simple, actionable outputs. The system was adapted from the Gemini lab notebooks and modified for waste-sorting scenarios.


## Workflow

**Input:**
- User types a description of waste items  
  Example: “I have leftover food, plastic bottles, and cardboard boxes”
- OR uploads an image of waste or bins

**AI Processing:**
- Extracts individual items from text input
- Classifies each item into categories (recycling, compost, landfill)
- For images, identifies objects and evaluates waste conditions (e.g., overflow, contamination)

**Output:**
- Structured list of items with disposal categories
- Clear instructions for each item
- Image-based analysis including urgency and recommended action

**Real-World Action:**
- Tenant correctly sorts waste into appropriate bins
- Tenant reports issues such as overflowing or contaminated bins
- Improves waste management and reduces environmental harm

**Screenshots:**




## Failure Case

**Prompt:**
"I have a clean-looking Styrofoam takeout container, a coffee cup, and a shiny chip bag."

**Observed Output:**
The AI classified some items as recyclable based on appearance or material assumptions.

**Failure:**
This is a failure because these items are typically not recyclable: Styrofoam is not accepted in most recycling programs, coffee cups have plastic lining, and chip bags are multi-layer materials. The AI produced confident but incorrect classifications.

**Real-World Consequence:**
If a tenant follows this output, they may incorrectly place non-recyclable items into recycling bins, increasing contamination and reducing the effectiveness of waste processing systems.


## Oversight and Tradeoff

**Oversight Decision:**
Human review is required when the AI has medium or low confidence, or when items involve ambiguous materials such as biodegradable plastics or mixed materials. This is necessary because the lab results show that the AI can produce incorrect classifications in edge cases.

**The One Change:**
The system will include an “unsure / needs human review” category instead of forcing every item into a classification.

**Tradeoff:**
This reduces automation and may slow down the user experience, but it improves accuracy and prevents harmful misclassification, making the system more reliable.
