from collections import Counter
import math
from mpim_tools.startup import names, comp_matrix


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


def get_mbti_type(person):
    version = 0
    if person[names['match']['personality']['INTRO_EXTROVERSION'][0]] == "With other people":
        version += 1
    if person[names['match']['personality']['INTRO_EXTROVERSION'][1]] == "Enjoy":
        version += 1
    if person[names['match']['personality']['INTRO_EXTROVERSION'][2]] == "Out-going and social":
        version += 1
    version = 'E' if version > 1 else 'I'

    sensing = 0
    if person[names['match']['personality']['SENSING_INTUITION'][0]] == "Facts, details and go step-by-step":
        sensing += 1
    if person[names['match']['personality']['SENSING_INTUITION'][1]] == "Things that are actual and practical":
        sensing += 1
    if person[names['match']['personality']['SENSING_INTUITION'][2]] == "Realistic and rely on your common sense":
        sensing += 1
    sensing = 'S' if sensing > 1 else 'N'

    feeling = 0
    if person[names['match']['personality']['FEELING_THINKING'][0]] == "Heart, feelings and emotions":
        feeling += 1
    if person[names['match']['personality']['FEELING_THINKING'][1]] == "Close and personal way":
        feeling += 1
    if person[names['match']['personality']['FEELING_THINKING'][2]] == "Being too emotional":
        feeling += 1
    feeling = 'F' if feeling > 1 else 'T'

    judging = 0
    if person[names['match']['personality']['JUDGING_PERCEIVING'][0]] == "Liberating":
        judging += 1
    if person[names['match']['personality']['JUDGING_PERCEIVING'][1]] == "Structured and planned out":
        judging += 1
    if person[names['match']['personality']['JUDGING_PERCEIVING'][2]] == "Control your environment":
        judging += 1
    judging = 'J' if judging > 1 else 'P'

    return version + sensing + feeling + judging


def compare_types(personality_type_a, personality_type_b):
    compatibility = comp_matrix.loc[personality_type_a, personality_type_b]
    return compatibility
