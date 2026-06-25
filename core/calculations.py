import numpy as np
import pandas as pd

def compute_fitness_targets(user_profile):
    """
    Applies biometric equations using NumPy to establish dynamic 
    caloric ceilings and macro distributions tailored to user objectives.
    """
    weight = user_profile['Body_Weight']
    height = user_profile['Height']
    age = user_profile['Age']
    gender = user_profile['Gender']
    activity = user_profile['Activity_Level']
    objective = user_profile['Objective']

    # Vectorized calculation configuration via Mifflin-St Jeor formulas
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Scalar mappings for individual active metrics
    activity_multipliers = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725
    }
    tdee = bmr * activity_multipliers.get(activity, 1.2)

    # Establish energetic targets modulated by core objective types
    if objective == 'Bulk':
        target_calories = tdee + 400
        protein_grams = weight * 2.2  # 2.2g per kg of body mass
    elif objective == 'Cut':
        target_calories = tdee - 500
        protein_grams = weight * 2.4  # Retain lean muscle tissue during deficit
    else:
        target_calories = tdee
        protein_grams = weight * 2.0  # Balance state baseline maintenance

    # Isolate caloric distributions for fat structures (25% total energy footprint)
    fat_grams = (target_calories * 0.25) / 9
    
    # Allocate remainder to carbohydrate structures
    allocated_calories = (protein_grams * 4) + (fat_grams * 9)
    carbs_grams = max(0, (target_calories - allocated_calories) / 4)

    return {
        'calories': int(np.round(target_calories)),
        'protein': int(np.round(protein_grams)),
        'carbs': int(np.round(carbs_grams)),
        'fats': int(np.round(fat_grams)),
        'footsteps': 10000  # Default daily standard benchmark
    }

def format_historical_summary(raw_logs):
    """
    Consumes raw row lists from the database layer, shifting them into 
    a Pandas DataFrame to reverse index records into chronological order.
    """
    if not raw_logs:
        return []

    # Map directly into a structured DataFrame
    df = pd.DataFrame(raw_logs)

    # Invert order chronologically (oldest first to newest) for chart layouts
    df = df.iloc[::-1].copy()

    # Formats date string timelines (e.g., '2026-06-26' -> 'Jun 26')
    df['Formatted_Date'] = pd.to_datetime(df['Log_Date']).dt.strftime('%b %d')

    # Convert native timestamp structures out into pure serial dictionary lists
    return df.to_dict(orient='records')