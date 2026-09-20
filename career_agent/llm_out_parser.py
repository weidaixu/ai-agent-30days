import json



def parse_llm_json(result_text):
    cleaned_text = result_text.replace("```json", "").replace("```", "").strip()
    profile_data = json.loads(cleaned_text)
    return profile_data