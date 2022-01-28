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
    return dotprod / (magA * magB)