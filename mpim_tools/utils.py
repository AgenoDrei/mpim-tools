import pandas as pd
from mpim_tools.startup import names


def load_person_by_id(person_id, df):
    person = df.loc[df[names['notification']['FORM_ID']] == int(person_id)]

    if len(person) != 1:
        print(f'Could not find corresponding person {person_id} in data...')
        return None

    return person.to_dict('records')[0]