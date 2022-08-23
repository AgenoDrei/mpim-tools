import numpy as np
import importlib.resources as pkg_resources
import pandas as pd
from io import StringIO
from mpim_tools import resources
from mpim_tools.startup import names, names as n
from mpim_tools.utils import cosine_similarity_words


pers = names['match']['personality']


def get_mbti_type(person):
    version = 0
    for i in range(3):
        if person[pers['INTRO_EXTROVERSION'][i]] == pers['EXTROVERSION_ANS'][i]:
            version += 1
    version = 'E' if version > 1 else 'I'

    sensing = 0
    for i in range(3):
        if person[pers['SENSING_INTUITION'][i]] == pers['SENSING_ANS'][i]:
            sensing += 1
    sensing = 'S' if sensing > 1 else 'N'

    feeling = 0
    for i in range(3):
        if person[pers['FEELING_THINKING'][i]] == pers['FEELING_ANS'][i]:
            feeling += 1
    feeling = 'F' if feeling > 1 else 'T'

    judging = 0
    for i in range(3):
        if person[pers['JUDGING_PERCEIVING'][i]] == pers['JUDGING_ANS'][i]:
            judging += 1
    judging = 'J' if judging > 1 else 'P'

    return version + sensing + feeling + judging


def compare_types(personality_type_a, personality_type_b):
    mtbi_table = pkg_resources.read_text(resources, "mtbi_table.csv")
    comp_matrix = pd.read_csv(StringIO(mtbi_table), index_col=0)

    compatibility = comp_matrix.loc[personality_type_a, personality_type_b]
    return compatibility


def calc_mcq_fitness(answer_a, answer_b):
    answer_a, answer_b = answer_a.split(", "), answer_b.split(", ")
    cos_sim = cosine_similarity_words(answer_a, answer_b)

    count = cos_sim * n['VALUE_IMPORTANCE_HIGH']
    return int(np.round(count))