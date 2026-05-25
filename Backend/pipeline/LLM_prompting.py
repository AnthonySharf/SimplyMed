import openai
from openai import OpenAI
import json

client = OpenAI()



def adverse_events_prompt_LLM(LLM_input):
    prompt = f"""
You are a medical data cleaning assistant. You will receive a dictionary of adverse drug events with their frequencies, and a list of red flag symptoms.

Your tasks:
1. Remove any remaining non-symptoms (drug errors, administrative events, device issues, Infusion related reactions, or anything that is not a physiological reaction in the human body). Also remove symptoms that are too vague to be meaningful to a non-expert user, such as "Malaise", "Feeling abnormal", "General physical health deterioration", "Asthenia", "drug hypersensitivity", "pain" or any symptom that doesn't describe a specific, identifiable experience.
2. Group symptoms into parent/child relationships. A parent is a broad symptom (e.g. "Pain"). Children are specific variants (e.g. "Abdominal pain", "Back pain"). Keep both, but nest children under their parent. Example of correct parent/child grouping: "Pain" is the parent. "Abdominal pain", "Back pain", "Chest pain", "Pain in extremity" are all children of "Pain" because they are specific types of pain. The parent "Pain" keeps its own frequency. Children keep their own frequencies nested underneath. Never list a child symptom as a standalone top-level entry if its parent is also present.
3. Keep all red flag symptoms regardless of frequency. Red flag symptoms are provided as a dict with their actual frequencies — use those exact frequency values in the output. In the output, prefix red flag symptom names with "⚠️ " so they are visually distinct from regular symptoms.
4. Remove duplicate or redundant symptoms where two entries describe the same condition. Keep the one with the higher frequency and remove the other. Examples: "Haemoglobin decreased" and "Anaemia" describe the same condition — keep whichever has higher frequency. "Renal failure" and "Renal failure acute" — keep the more specific one if it has meaningful frequency, otherwise keep the higher frequency one.
5. If present, remove the "pain" symptom and its frequency as it is too vague to be meaningful to a non-expert user, and keep the more specific variants of pain (abdominal pain, back pain, chest pain, etc.) with their frequencies.

Input:
Top 10 adverse events: {LLM_input["top_ten_adverse_events"]}
Red flag symptoms (include these with their exact frequencies): {LLM_input["red_flag_symptoms"]}

Return ONLY a JSON object in this exact structure, no explanation, no markdown:
{{
  "symptom_name": {{
    "frequency": <integer>
  }}
  
List regular symptoms first, then red flag symptoms at the end.

Important: frequency values must always be a single integer or float, never a tuple or list.

"""
    return prompt

def call_LLM_adverse_events(LLM_input_adverse_events):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": adverse_events_prompt_LLM(LLM_input_adverse_events)}
    ]
)
    LLM_output_adverse_events = json.loads(response.choices[0].message.content)
    return LLM_output_adverse_events

def drug_profile_prompt_LLM(profile_formatted):
    prompt = f"""
You are a medical information simplifier. You will receive raw drug label information including warnings, active ingredients, and usage instructions. You will also receive the purpose or usage of the drug, which you will summarize what the drug is used for in the 'purpose' field.

Your task:
Rewrite this information in plain English that a non-medical person can easily understand. Be concise and clear. Do not use clinical jargon. Do not add any information that is not in the original text.

Input:
{profile_formatted}

Return ONLY a JSON object in this exact structure, no explanation, no markdown:
{{
  "purpose": "<simplified string>",
  "active_ingredients": "<simplified string>",
  "warnings": "<simplified string>",
  "usage": "<simplified string>"
}}
"""
    return prompt

def call_LLM_drug_profile(profile_formatted):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": drug_profile_prompt_LLM(profile_formatted)}
    ]
)
    LLM_output_drug_profile = json.loads(response.choices[0].message.content)
    return LLM_output_drug_profile