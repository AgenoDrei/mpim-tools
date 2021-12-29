import math
import requests
from mpim_tools.startup import config
from string import Template
from mpim_tools.utils import load_person_by_id
from mpim_tools import templates
import importlib.resources as pkg_resources
from jinja2 import Environment


PERSON_ID = 'person_id'
MATCH_IDS = 'match_ids'
MATCH_ID = 'id'
NAME_COL = 'What is your name?'


def send_mails(matches_df, people_df, mode, debug=False):
    for i, row in matches_df.iterrows():
        print(f"Working on person with id {row[PERSON_ID]} now..")
        person_a_id = row[PERSON_ID]
        person_a = load_person_by_id(person_a_id, people_df)
        if not person_a:
            continue
        match_ids = row[MATCH_IDS]
        match_ids = match_ids.replace(" ", "").strip()
        match_ids = match_ids.split(',')

        matches = []
        for match_id in match_ids:
            match = load_person_by_id(match_id, people_df)
            if not match:
                continue
            try:
                del match['By filling this form you give consent that your personal data (i.e. all answers given in this form as well as your contact details) will be used during the matching process and will be sent to your matches afterwards.']
                del match[MATCH_ID]
            except KeyError:
                pass
            match = {k: v for k, v in match.items() if not (type(v) == float and math.isnan(v))}
            matches.append(match)

        # construct mail
        #mail_body = render_mail_body(person_a, matches)
        env = Environment()
        mail_template = pkg_resources.read_text(templates, 'mail_tmpl.html')
        mail_template = env.from_string(mail_template)
        mail_body = mail_template.render(forename=person_a[NAME_COL], number=len(matches), matches=matches, mode=mode)
        # send mail
        send_html_mail(mail_body, person_a['mail'], mode, debug=False) # mail should be replaced by person_a['mail']

        # print(mail)


def send_html_mail(mail_body, recipient, mode, debug=True):
    if debug: recipient = "s.mueller1995@gmail.com"
    res = requests.post(f"{config['base_url']}{config['domain']}/messages",
                        auth=("api", config['apikey']),
                        data={"from": f"mail@{config['domain']}",
                              "to": [recipient],
                              "subject": f"Your Meet-People-In-Maastricht matches - {mode}",
                              "html": mail_body
                              }
                        )
    if res.status_code == 200:
        print(f'Mail to {recipient} successfully sent!')
    else:
        print(f'There was a problem sending the email to {recipient}')
