import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from mpim_tools.constants import *


def create_matches(df, output_path, maximum_matches):
    for i, row in tqdm(df.iterrows(), total=len(df)):
        matches_df = pd.DataFrame(columns=df.columns)
        gender = row[GENDER_COL]
        orientation = row[ORIENTATION_COL]
        matches_df['fitness'] = -1

        for j, match_row in df.iterrows():
            if j == i:
                continue
            if gender == match_row[GENDER_COL] and orientation == HETERO:
                continue
            if gender != match_row[GENDER_COL] and orientation == HOMO:
                continue
            if orientation == BI and match_row[GENDER_COL] == gender and match_row[ORIENTATION_COL] == HETERO:
                continue
            if orientation == BI and match_row[GENDER_COL] != gender and match_row[ORIENTATION_COL] == HOMO:
                continue
            match_fitness = calc_match_fitness(row, match_row)
            # match_row_dict = match_row.to_dict()
            match_row['fitness'] = match_fitness
            matches_df = matches_df.append(match_row, ignore_index=True)

        matches_sorted_df = matches_df.sort_values(by="fitness", ascending=False)
        matches_sorted_df.head(maximum_matches).to_csv(os.path.join(output_path, f'{i}.csv'), index=False, sep=';')


def calc_mcq_fittness(answer_a, answer_b):
    answer_a, answer_b = answer_a.split(", "), answer_b.split(", ")
    count = 0
    for answer in answer_a:
        count += answer_b.count(answer)

    count = count / len(answer_a) * VALUE_IMPORTANCE_HIGH
    return int(np.round(count))


def calc_match_fitness(person_a, person_b):
    age_comp = VALUE_IMPORTANCE_HIGH - np.absolute(int(person_a[AGE_COL][:2]) - int(person_b[AGE_COL][:2]))
    happy_comp = VALUE_IMPORTANCE_MED - np.absolute(person_a[HAPPY_COL] - person_b[HAPPY_COL])
    faculty_comp = VALUE_IMPORTANCE_HIGH if person_a[FACULTY_COL] == person_b[FACULTY_COL] else 0
    nationality_comp = VALUE_IMPORTANCE_LOW if person_a[FACULTY_COL] == person_b[FACULTY_COL] else 0
    hobby_comp = calc_mcq_fittness(person_a[HOBBY_COL], person_b[HOBBY_COL])
    trait_comp = calc_mcq_fittness(person_a[TRAIT_COL], person_b[TRAIT_COL])
    ll_comp = calc_mcq_fittness(person_a[LOVE_LANGUAGE_COL], person_b[LOVE_LANGUAGE_COL])
    belief_comp = VALUE_IMPORTANCE_HIGH if person_a[BELIEF_COL] == person_b[BELIEF_COL] else 0
    prio_comp = VALUE_IMPORTANCE_MED if person_a[PRIO_COL] == person_b[PRIO_COL] else 0

    # ToDo: marriage, kids, showering, trust, therapy, ideal date

    happy_comp = int(happy_comp) if not np.isnan(happy_comp) else 0
    age_comp = int(age_comp) if not np.isnan(age_comp) else 0

    fitness = age_comp + faculty_comp + nationality_comp + happy_comp + hobby_comp + trait_comp + ll_comp + belief_comp + prio_comp
    return fitness
