import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from mpim_tools.startup import names as n
from mpim_tools.utils import cosine_similarity_words


cm = n['match']


def create_matches(df, output_path, maximum_matches, mode='Relationship'):
    for i, row in tqdm(df.iterrows(), total=len(df)):
        matches_df = pd.DataFrame(columns=df.columns)
        matches_df['fitness'] = -1
        gender = row[cm['GENDER_COL']]

        orientation = None
        if mode == 'Relationship' or mode == 'FWB':
            orientation = row[cm['ORIENTATION_COL']]
            if orientation in cm['DEF_HOMO']:
                orientation = cm['HOMO']
            if orientation == cm['NOT_KNOWN']:
                continue

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
                if match_orientation == cm['NOT_KNOWN']:
                    continue

            match_fitness = calc_match_fitness(row, match_row, mode)
            # match_row_dict = match_row.to_dict()
            match_row['fitness'] = match_fitness
            matches_df = matches_df.append(match_row, ignore_index=True)

        matches_sorted_df = matches_df.sort_values(by="fitness", ascending=False)
        matches_sorted_df.head(maximum_matches).to_csv(os.path.join(output_path, f'{row[n["notification"]["FORM_ID"]]}.csv'), index=False, sep=';')


def calc_mcq_fitness(answer_a, answer_b):
    answer_a, answer_b = answer_a.split(", "), answer_b.split(", ")
    cos_sim = cosine_similarity_words(answer_a, answer_b)

    count = cos_sim * n['VALUE_IMPORTANCE_HIGH']
    return int(np.round(count))


def calc_match_fitness(person_a, person_b, mode):
    fitness = 0

    # Ranged values
    age_comp = n['VALUE_IMPORTANCE_MED'] - np.absolute(int(person_a[cm['range']['AGE_COL']][:2]) - int(person_b[cm['range']['AGE_COL']][:2]))
    age_comp = int(age_comp) if not np.isnan(age_comp) else 0
    fitness += age_comp
    if mode == 'Relationship' or mode == 'FWB':
        trust_comp = n['VALUE_IMPORTANCE_MED'] - np.absolute(person_a[cm['range']['TRUST_COL']] - person_b[cm['range']['TRUST_COL']])
        trust_comp = int(trust_comp) if not np.isnan(trust_comp) else 0
        fitness += trust_comp

    # MCQ categories
    for k, v in cm['mcq'].items():
        if person_a.get(v) == None:
            continue
        fitness += calc_mcq_fitness(person_a[v], person_b[v])

    # Simple questions
    for k, v in cm['simple'].items():
        if person_a.get(v) == None:
            continue
        fitness += n['VALUE_IMPORTANCE_MED'] if person_a[v] == person_b[v] else 0


    # faculty_comp = n['VALUE_IMPORTANCE_HIGH'] if person_a[n['match']['FACULTY_COL']] == person_b[n['match']['FACULTY_COL']] else 0
    # hobby_comp = calc_mcq_fitness(person_a[n['match']['HOBBY_COL']], person_b[n['match']['HOBBY_COL']])
    # fitness = age_comp + faculty_comp + hobby_comp + trait_comp + ll_comp + belief_comp + prio_comp + marriage_comp + children_comp + trust_comp
    return fitness
