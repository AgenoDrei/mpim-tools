import pandas as pd
import requests as requests

from mpim_tools.startup import config
from string import Template


def send_mails(matches_df, people_df, debug=False):
    for i, row in matches_df.iterrows():
        print(f"Working on person with id {row['person_id']} now..")
        person_a_id = row['person_id']
        person_a = load_person_by_id(person_a_id, people_df)
        if not person_a:
            continue

        match_ids = row['match_ids']
        match_ids = match_ids.replace(" ", "").strip()
        match_ids = match_ids.split(',')

        matches = []
        for match_id in match_ids:
            match = load_person_by_id(match_id, people_df)
            if not match:
                continue
            matches.append(match)

        # construct mail
        mail_body = render_mail_body(person_a, matches)
        # send mail
        # print(mail)
        send_mail(mail_body, "s.mueller1995@gmail.com", debug=debug)


def render_mail_body(person, matches):
    template_start = Template("Hello $forename!\n"
                              "\n"
                              "Thanks for participating in this round of Meet People in Maastricht. After carefully\n"
                              "working through all of the participants we are happy to present you with the following\n"
                              "$number matches:\n\n")
    template_single_match = Template("\n"
                                     "--- Match Number ${id}: ------------------------------------------------------\n"
                                     "Name: $name\n"
                                     "Age: $age\n"
                                     "Faculty: $faculty\n"
                                     "Gender: $gender\n"
                                     "Sexual orientation: $orientation\n"
                                     "")
    template_end = Template("\n"
                            "--------------------------------------------------------------------------------------\n"
                            "We hope you are happy with the selection. Enjoying reaching out to your matches with the\n"
                            "provided address. Remember to be respectful to each other and enjoy meeting all of these\n"
                            "new people!\n"
                            "\n"
                            "Kind regards\n"
                            "The Meet-People-In-Maastricht Team")

    mail_string = template_start.substitute(forename=person['id'], number=len(matches))
    for i, m in enumerate(matches):
        mapping = {
            'id': i + 1,
            'name': m['id'],
            'age': m['How old are you?'],
            'faculty': m['If you are a student, at which faculty are you studying?'],
            'gender': m['What is your gender?'],
            'orientation': m['What is your sexual orientation?']
        }
        mail_string += template_single_match.substitute(mapping)
    mail_string += template_end.substitute()
    return mail_string


def send_mail(mail_body, recipient, debug=True):
    if debug:
        recipient = "s.mueller1995@gmail.com"
    res = requests.post(f"https://api.mailgun.net/v3/{config['domain']}/messages",
                        auth=("api", config['apikey']),
                        data={"from": f"mailgun@{config['domain']}",
                              "to": [recipient],
                              "subject": "Your Meet-People-In-Maastricht matches",
                              "text": mail_body
                              }
                        )
    print(res)


def load_person_by_id(person_id, people_df):
    person = people_df.loc[people_df['id'] == int(person_id)]

    if len(person) != 1:
        print(f'Could not find corresponding person {person_id} in data...')
        return None

    return person.to_dict('records')[0]
