class DataCleaning:
    # First function: automatically remove all non-symptoms from the list of adverse events
    def remove_non_symptoms(adverse_events):
        cleaned_adverse_events = adverse_events.copy() # Create a copy of the original dictionary to avoid modifying it directly
        non_symptoms = [
        "Drug ineffective", 
        "Off label use", 
        "Drug interaction", 
        "Wrong technique in drug usage process", 
        "Drug dose omission", 
        "Incorrect dose administered", 
        "Product quality issue", 
        "Drug administration error", 
        "Adverse event", 
        "No adverse event"
        ]
        for k in list(cleaned_adverse_events.keys()):
            if k in non_symptoms:
                del cleaned_adverse_events[k]
        return cleaned_adverse_events


    # Second function: flag all severe, red flag language in the adverse events with a hardcoded list of key words and their frequencies
    def flag_red_flag_language(cleaned_adverse_events):
        red_flag_symptoms = {}
        red_flag_language = [
        "Death",
        "Completed suicide",
        "Suicide attempt",
        "Suicidal ideation",
        "Anaphylactic reaction",
        "Cardiac arrest",
        "Respiratory arrest",
        "Septic shock",
        "Multi-organ failure",
        "Stevens-Johnson syndrome"
        ]
        for k in list(cleaned_adverse_events.keys()):
            if k in red_flag_language:
                red_flag_symptoms[k] = cleaned_adverse_events[k]
        return red_flag_symptoms

    # Third function: create a new dicitonary from the cleaned containing only the top 10 most common adverse events and their frequencies
    def pick_top_ten_adverse_events(cleaned_adverse_events):
        sorted_cleaned_adverse_events = {}
        for key in sorted(cleaned_adverse_events, key=cleaned_adverse_events.get, reverse=True): # Resort dict in case it became unsorted when removing non-symptoms
            sorted_cleaned_adverse_events[key] = cleaned_adverse_events[key]
        top_ten_adverse_events = dict(list(sorted_cleaned_adverse_events.items())[:10])
        return top_ten_adverse_events

    # Fourth function: Pass the final, cleaned dictionary to the LLM in LLM_prompting.py to remove 
    def pass_to_LLM(top_ten_adverse_events, red_flag_symptoms):
        LLM_input_adverse_events = {} # Input to the LLM should be a dict because LLMs accept json format
        LLM_input_adverse_events["top_ten_adverse_events"] = top_ten_adverse_events
        LLM_input_adverse_events["red_flag_symptoms"] = red_flag_symptoms
        return LLM_input_adverse_events
    
    def frequency_to_percentage(LLM_output_drug_profile):
        profile_copy = LLM_output_drug_profile.copy()
        for symptom in LLM_output_drug_profile:
            frequency = LLM_output_drug_profile[symptom]["frequency"]
            percentage = round((frequency / 500) * 100, 1) # Convert frequency to percentage based on the total number of adverse event reports (500)
            profile_copy[symptom]["frequency"] = percentage
        return profile_copy
        