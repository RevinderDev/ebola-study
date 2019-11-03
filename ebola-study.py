import json
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt

DATABASES = {
    'Guinea': ['guinea_weekly.json',
               'guinea_conarky_weekly.json',
               'guinea_district_weekly.json'],

    'Liberia': ['liberia_weekly.json',
                'liberia_monsterrado_weekly.json',
                'liberia_district_weekly.json'],

    'Sierra_Leone': ['sierra_weekly.json',
                     'sierra_westernarea_weekly.json',
                     'sierra_district_weekly.json']
}

DATA_SOURCES = ['Situation report', 'Patient database']

HIST_SIZE = (32, 16)
HIST_FONT_SIZE = 30
HIST_LABEL_SIZE = 7
HIST_BAR_WIDTH = 0.35


def create_hist(parsed_data):
    title = parsed_data['Country'] + parsed_data.get("Location", '')

    index = np.arange(len(parsed_data['Probable']))

    bar_width = HIST_BAR_WIDTH

    fig, ax = plt.subplots(figsize=HIST_SIZE)

    probable = ax.bar(index, [dic['value'] for dic in parsed_data['Probable']]
                      , bar_width, label='Probable cases')
    confirmed = ax.bar(index + bar_width, [dic['value'] for dic in parsed_data['Confirmed']]
                       , bar_width, label='Confirmed cases')

    ax.set_title(title, fontsize=HIST_FONT_SIZE)
    ax.set_xlabel('Weeks', fontsize=HIST_FONT_SIZE)
    ax.set_ylabel('Value', fontsize=HIST_FONT_SIZE)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels([dic['week'] for dic in parsed_data['Probable']], fontsize=HIST_LABEL_SIZE, rotation=90)
    ax.legend(fontsize=HIST_FONT_SIZE)
    paint_rectangle_values(probable)
    paint_rectangle_values(confirmed)
    plt.show()


def paint_rectangle_values(data):
    for rectangle in data:
        height = rectangle.get_height()
        if height == 0:
            continue
        plt.annotate('{}'.format(height),
                     xy=(rectangle.get_x() + rectangle.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom')


def parse_non_district_to_summary(weekly_data, country_name):
    parsed_data = {'Country': country_name,
                   'Probable': [],
                   'Confirmed': []
                   }
    try:
        parsed_data['Location'] = weekly_data['fact'][0]['dims']['LOCATION'].capitalize()
    except KeyError:
        pass

    for report in weekly_data['fact']:
        dims = report['dims']
        try:
            value = int(report['Value'])
        except ValueError:
            value = 0
        case = {
            'value': value,
            'week': dims['EPI_WEEK']  # (\(.*\))
        }
        if dims['CASE_DEFINITION'] == 'Confirmed':
            parsed_data['Confirmed'].append(case)
        elif dims['CASE_DEFINITION'] == 'Probable':
            parsed_data['Probable'].append(case)

    return parsed_data


if __name__ == '__main__':
    with open('db_auth.json') as json_file:
        auth_data = json.load(json_file)
        client = MongoClient(auth_data['client_string'])

    for country in DATABASES:
        summaries = client[country]
        for document in DATABASES[country]:
            doc_data = summaries[document]
            if 'district' in document:
                pass  # TODO: zpasrowac z district jakos
            else:
                parsed_situation = parse_non_district_to_summary(weekly_data=doc_data.find().next(),
                                                                 country_name=country)
                create_hist(parsed_data=parsed_situation)

            # TODO: Wytworzyc histogram tutaj
            # TODO: Dodac modele dalej

    client.close()
