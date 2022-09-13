import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from mpim_tools.startup import names as n
from mpim_tools.process_details import get_mbti_type, compare_types, calc_mcq_fitness
from mpim_tools.utils import adjust_orientations

cm = n['match']


def create_matches(df, output_path, maximum_matches, mode='Relationship'):
    if mode == 'Relationship' or mode == 'FWB':
        adjust_orientations(df)

    for i, row in tqdm(df.iterrows(), total=len(df)):
        # Create table with matches for the current person
        matches_df = pd.DataFrame(columns=df.columns)
        matches_df['fitness'] = -1
        matches_df['compatibility'] = -1
        gender = row[cm['GENDER_COL']]
        orientation = row[cm['ORIENTATION_COL']]

        # Compare the current person with everyone else
        for j, match_row in df.iterrows():
            match_gender = match_row[cm['GENDER_COL']]
            if row[n["notification"]["FORM_ID"]] == match_row[n["notification"]["FORM_ID"]]:
                continue
            if mode == 'Relationship' or mode == 'FWB':
                match_orientation = match_row[cm['ORIENTATION_COL']]
                if gender == match_gender and (match_orientation == cm['HETERO'] or orientation == cm['HETERO']):
                    continue
                if gender != match_gender and (match_orientation == cm['HOMO'] or orientation == cm['HOMO']):
                    continue
                if orientation == cm['BI'] and match_gender == gender and match_orientation == cm['HETERO']:
                    continue
                if orientation == cm['BI'] and match_gender != gender and match_orientation == cm['HOMO']:
                    continue
                if match_orientation == cm['NOT_KNOWN'] and orientation == cm['NOT_KNOWN']:
                    continue

            # Calculate match similarity based on questions
            match_fitness = calc_match_fitness(row, match_row, mode)
            # Measure similarity by personality traits
            match_compatibility = compare_personalities(row, match_row)

            match_row['fitness'] = match_fitness
            match_row['compatibility'] = match_compatibility

            matches_df = matches_df.append(match_row, ignore_index=True)

        # Get mix of similar, compatible and random matches for this person
        top_matches = matches_df.sort_values(by="fitness", ascending=False)
        top_matches = top_matches.head(maximum_matches - n["NUM_RANDOM_MATCHES"] - n["NUM_COMPATIBLE_MATCHES"]).copy()
        compatible_matches = matches_df.sort_values(by="compatibility", ascending=False).head(n["NUM_COMPATIBLE_MATCHES"]).copy()
        top_matches = top_matches.append(compatible_matches, ignore_index=True)
        if len(df) > maximum_matches:
            random_matches = matches_df.sample(n=n["NUM_RANDOM_MATCHES"])
            top_matches = top_matches.append(random_matches, ignore_index=True)

        # Save matches for this person
        top_matches = top_matches.drop_duplicates(subset=[n['notification']['FORM_ID']])
        top_matches.to_csv(os.path.join(output_path, f'{row[n["notification"]["FORM_ID"]]}.csv'), index=False, sep=';')


def calc_match_fitness(person_a, person_b, mode):
    fitness = 0
    # Ranged values
    age_comp = n['VALUE_IMPORTANCE_MED'] - np.absolute(int(person_a[cm['range']['AGE_COL']][:2]) - int(person_b[cm['range']['AGE_COL']][:2]))
    age_comp = int(age_comp) if not np.isnan(age_comp) else 0
    fitness += age_comp
    if mode == 'Relationship' or mode == 'FWB':
        trust_comp = n['VALUE_IMPORTANCE_MED'] - np.absolute(person_a[cm['range']['TRUST_COL']] - person_b[cm['range']['TRUST_COL']])
        trust_comp = int(trust_comp) if not np.isnan(trust_comp) else 0
        #weight_comp = n['VALUE_IMPORTANCE_MED'] - np.absolute(person_a[cm['range']['WEIGHT_COL']] - person_b[cm['range']['WEIGHT_COL']])
        #weight_comp = int(weight_comp) if not np.isnan(weight_comp) else 0
        weight_comp = 0
        fitness += weight_comp + trust_comp

    # MCQ categories
    for k, v in cm['mcq'].items():
        if person_a.get(v) is None:
            continue
        fitness += calc_mcq_fitness(person_a[v], person_b[v])

    # Simple questions
    for k, v in cm['simple'].items():
        if person_a.get(v) is None:
            continue
        fitness += n['VALUE_IMPORTANCE_MED'] if person_a[v] == person_b[v] else 0

    return fitness


def compare_personalities(person_a, person_b):
    personality_type_a = get_mbti_type(person_a)
    personality_type_b = get_mbti_type(person_b)

    compatibility = compare_types(personality_type_a, personality_type_b)

    return compatibility
