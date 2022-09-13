from collections import Counter
import math
from mpim_tools.startup import names


cm = names['match']


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


def adjust_orientations(df):
    for i, row in df.iterrows():
        orientation = row[cm['ORIENTATION_COL']]
        if orientation in cm['DEF_HOMO']:
            df.loc[i, cm['ORIENTATION_COL']] = cm['HOMO']
            orientation = cm['HOMO']
        if orientation != cm['HOMO'] and orientation != cm['HETERO'] and orientation != cm['BI']:
            df.loc[i, cm['ORIENTATION_COL']] = cm['NOT_KNOWN']