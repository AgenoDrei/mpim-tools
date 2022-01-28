import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from mpim_tools.startup import names as n
from mpim_tools.utils import cosine_similarity_words


def create_matches(df, output_path, maximum_matches):
    for i, row in tqdm(df.iterrows(), total=len(df)):
        matches_df = pd.DataFrame(columns=df.columns)
        gender = row[n['match']['GENDER_COL']]
        orientation = row[n['match']['ORIENTATION_COL']]
        if orientation in n['match']['DEF_HOMO']:
            orientation = n['match']['HOMO']
        matches_df['fitness'] = -1

        for j, match_row in df.iterrows():
            if j == i:
                continue
            if gender == match_row[n['match']['GENDER_COL']] and orientation == n['match']['HETERO']:
                continue
            if gender != match_row[n['match']['GENDER_COL']] and orientation == n['match']['HOMO']:
                continue
            if orientation == n['match']['BI'] and match_row[n['match']['GENDER_COL']] == gender and match_row[n['match']['ORIENTATION_COL']] == n['match']['HETERO']:
                continue
            if orientation == n['match']['BI'] and match_row[n['match']['GENDER_COL']] != gender and match_row[n['match']['ORIENTATION_COL']] == n['match']['HOMO']:
                continue
            match_fitness = calc_match_fitness(row, match_row)
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


def calc_match_fitness(person_a, person_b):
    age_comp = n['VALUE_IMPORTANCE_MED'] - np.absolute(int(person_a[n['match']['AGE_COL']][:2]) - int(person_b[n['match']['AGE_COL']][:2]))
    happy_comp = n['VALUE_IMPORTANCE_MED'] - np.absolute(person_a[n['match']['HAPPY_COL']] - person_b[n['match']['HAPPY_COL']])
    trust_comp = n['VALUE_IMPORTANCE_MED'] - np.absolute(person_a[n['match']['TRUST_COL']] - person_b[n['match']['TRUST_COL']])
    faculty_comp = n['VALUE_IMPORTANCE_HIGH'] if person_a[n['match']['FACULTY_COL']] == person_b[n['match']['FACULTY_COL']] else 0
    # nationality_comp = n['VALUE_IMPORTANCE_LOW'] if person_a[n['match']['FACULTY_COL']] == person_b[n['match']['FACULTY_COL']] else 0
    hobby_comp = calc_mcq_fitness(person_a[n['match']['HOBBY_COL']], person_b[n['match']['HOBBY_COL']])
    trait_comp = calc_mcq_fitness(person_a[n['match']['TRAIT_COL']], person_b[n['match']['TRAIT_COL']])
    ll_comp = calc_mcq_fitness(person_a[n['match']['LOVE_LANGUAGE_COL']], person_b[n['match']['LOVE_LANGUAGE_COL']])
    belief_comp = n['VALUE_IMPORTANCE_HIGH'] if person_a[n['match']['BELIEF_COL']] == person_b[n['match']['BELIEF_COL']] else 0
    prio_comp = n['VALUE_IMPORTANCE_MED'] if person_a[n['match']['PRIO_COL']] == person_b[n['match']['PRIO_COL']] else 0
    marriage_comp = n['VALUE_IMPORTANCE_MED'] if person_a[n['match']['MARRIAGE_COL']] == person_b[n['match']['MARRIAGE_COL']] else 0
    children_comp = n['VALUE_IMPORTANCE_MED'] if person_a[n['match']['CHILDREN_COL']] == person_b[n['match']['CHILDREN_COL']] else 0
    shower_comp = n['VALUE_IMPORTANCE_LOW'] if person_a[n['match']['SHOWER_COL']] == person_b[n['match']['SHOWER_COL']] else 0

    happy_comp = int(happy_comp) if not np.isnan(happy_comp) else 0
    trust_comp = int(trust_comp) if not np.isnan(trust_comp) else 0
    age_comp = int(age_comp) if not np.isnan(age_comp) else 0

    fitness = age_comp + faculty_comp + happy_comp + hobby_comp + trait_comp + ll_comp + \
              belief_comp + prio_comp + marriage_comp + children_comp + shower_comp + trust_comp
    return fitness
