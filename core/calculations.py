import numpy as np
import pandas as pd

def compute_fitness_targets(user_profile):
    """
    Applies biometric equations using NumPy to establish dynamic 
    caloric ceilings and macro distributions tailored to user objectives.
    """
    weight = float(user_profile['Body_Weight'])
    height = float(user_profile['Height'])
    age = int(user_profile['Age'])
    gender = user_profile['Gender']
    activity = user_profile['Activity_Level']
    objective = user_profile['Objective']

    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725
    }
    tdee = bmr * activity_multipliers.get(activity, 1.2)

    if objective == 'Bulk':
        target_calories = tdee + 400
        protein_grams = weight * 2.2 
    elif objective == 'Cut':
        target_calories = tdee - 500
        protein_grams = weight * 2.4  
    else:
        target_calories = tdee
        protein_grams = weight * 2.0  

    fat_grams = (target_calories * 0.25) / 9
    
    allocated_calories = (protein_grams * 4) + (fat_grams * 9)
    carbs_grams = max(0, (target_calories - allocated_calories) / 4)

    return {
        'calories': int(np.round(target_calories)),
        'protein': int(np.round(protein_grams)),
        'carbs': int(np.round(carbs_grams)),
        'fats': int(np.round(fat_grams)),
        'footsteps': 10000  
    }

def format_historical_summary(raw_logs):
    """
    Consumes raw row lists from the database layer, shifting them into 
    a Pandas DataFrame to reverse index records into chronological order.
    """
    if not raw_logs:
        return []

    df = pd.DataFrame(raw_logs)

    df = df.iloc[::-1].copy()

    df['Formatted_Date'] = pd.to_datetime(df['Log_Date']).dt.strftime('%b %d')

    return df.to_dict(orient='records')