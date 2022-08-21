from collections import Counter
import pandas as pd
import math
from mpim_tools.startup import names


def load_person_by_id(person_id, df):
    person = df.loc[df[names['notification']['FORM_ID']] == int(person_id)]

    if len(person) != 1:
        print(f'Could not find corresponding person {person_id} in data...')
        return None

    return person.to_dict('records')[0]


def cosine_similarity_words(words1, words2):
    c1 = Counter(words1)
    c2 = Counter(words2)

    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    res = dotprod / (magA * magB)
    return res


# TODO: Complete other subtypes
def get_mbti_type(person):
    version = 0
    if names['match']['personality']['INTRO_EXTROVERSION'][0] == "With other people":
        version += 1
    if names['match']['personality']['INTRO_EXTROVERSION'][1] == "Enjoy":
        version += 1
    if names['match']['personality']['INTRO_EXTROVERSION'][2] == "Out-going and social":
        version += 1
    version = 'E' if version > 1 else 'I'

    sensing = 0

    feeling = 0
    judging = 0

    return version, 'S', 'F', 'J'


def compare_types(personality_type_a, personality_type_b):
    return 1
