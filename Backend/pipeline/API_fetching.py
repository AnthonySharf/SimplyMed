import requests

def fetch_drug_adverse_effects(drug_name):
    # OpenFDA API endpoint for drug events. For adverse events, it's important to get a large sample of side effects (limit=500) and symptoms to back up the claims from the product labeling with evidence.
    url = f"https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{drug_name}&limit=500"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful. 
        data = response.json()
        reaction_counts = {}

        # Extracting relevant information from the response, including the drug name, adverse event, and report date. This is also capable of handling scenarios in which a particular value is empty or null, replacing it with N/A or a blank
        if 'results' in data:
            for result in data['results']:
                reactions = result.get('patient', {}).get('reaction', [])
                for reaction in reactions:
                    term = reaction.get('reactionmeddrapt', None)
                    if term:
                        reaction_counts[term] = reaction_counts.get(term, 0) + 1

            return dict(sorted(reaction_counts.items(), key=lambda x: x[1], reverse=True))
                
        else:
            return {"message": "No data found for the specified drug."}
    
    # Display an erro message if the request fails
    except requests.exceptions.RequestException as e:
        return {"error": str(e)} 
    

def fetch_drug_profile(drug_name):
    # OpenFDA API endpoint for drug profile. 
    url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}+OR+openfda.brand_name:{drug_name}&limit=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful. 
        data = response.json()
        profile_formatted = []

        # Extracting relevant information from the response. This is also capable of handling scenarios in which a particular value is empty or null, replacing it with N/A or a blank
        if 'results' in data:
            for result in data['results']:
                openfda_info = result.get('openfda', {})
                if 'HUMAN PRESCRIPTION DRUG' in openfda_info.get('product_type', []):
                    indications_and_usage = result.get('indications_and_usage', [])
                    description = result.get('description', [])
                    general_precaution = result.get('precautions', [])
                    adverse_reactions = result.get('adverse_reactions', [])
                    profile_formatted = str("Usage: " + str(indications_and_usage) + "Description: " + str(description) + ", " + "General Precautions: " + str(general_precaution) + ", " + "Adverse Reactions: " + str(adverse_reactions))
                else:
                    purpose = result.get('purpose', [])
                    active_ingredients = result.get('active_ingredient', [])
                    warnings = result.get('warnings', [])
                    stop_use = result.get('stop_use', [])
                    profile_formatted = str("Purpose: " + str(purpose) + ", " + "Active Ingredients: " + str(active_ingredients) + ", " + "Warnings: " + str(warnings) + ", " + "Stop Use: " + str(stop_use))

            return profile_formatted
    
        else:
            return {"message": "No data found for the specified drug."}
    
    # Display an error message if the request fails
    except requests.exceptions.RequestException as e:
        return {"error": str(e)} 