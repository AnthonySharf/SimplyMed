from fastapi import FastAPI

from pipeline.API_fetching import fetch_drug_adverse_effects
from pipeline.API_fetching import fetch_drug_profile
from pipeline.data_cleaning import DataCleaning

from database import get_drug
from database import save_drug

from pipeline.LLM_prompting import call_LLM_adverse_events
from pipeline.LLM_prompting import call_LLM_drug_profile

from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a simple GET endpoint for the drug-profile name
# The reason why the OpenFDA URL isn't used here is because the API fetching logic occurs in its own file (fetch_data.py) 
# Combined the previous two API endpoints into one to reduce the number of API calls and improve efficiency.
    
@app.get("/drug-info/{drug}")
def read_drug_name(drug: str):
    drug_name = drug.lower()
    drug_info = get_drug(drug_name) # Reduces the number of API calls
    if drug_info:
        return drug_info # If the drug already exists in the database, return the drug information from the database
    else: 

        # SPECIFICALLY FOR ADVERSE EVENTS AND RED FLAGGED SYMPTOMS
        adverse_effects = fetch_drug_adverse_effects(drug_name) 
        cleaned_symptoms = DataCleaning.remove_non_symptoms(adverse_effects)
        top_ten = DataCleaning.pick_top_ten_adverse_events(cleaned_symptoms)
        red_flag_symptoms = DataCleaning.flag_red_flag_language(cleaned_symptoms)
        LLM_input_adverse_events = DataCleaning.pass_to_LLM(top_ten, red_flag_symptoms)
        LLM_adverse_events_red_flagged = call_LLM_adverse_events(LLM_input_adverse_events)
        Final_LLM_adverse_events_red_flagged = DataCleaning.frequency_to_percentage(LLM_adverse_events_red_flagged) # Convert frequencies to percentages for the final output to the frontend

        # SPECIFICALLY FOR DRUG PROFILE INFORMATION
        drug_profile = fetch_drug_profile(drug_name)
        LLM_drug_profile = call_LLM_drug_profile(drug_profile)

        # SPECIFICALLY FOR SAVING THE DRUG INFORMATION TO THE DATABASE
        save_drug(drug_name, Final_LLM_adverse_events_red_flagged, LLM_drug_profile) # Save the drug information to the database

        # SPECIFICALLY FOR RETURNING THE DRUG INFORMATION TO THE FRONTEND
        return {"drug_name": drug, "adverse_events": Final_LLM_adverse_events_red_flagged, "drug_profile": LLM_drug_profile}
    

