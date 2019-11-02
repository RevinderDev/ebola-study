import json
from pymongo import MongoClient

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


def create_hist(xvalues, yvalues):
    # TODO: Stworzyc histogram chyba z sumaryczny z tygodnia na tydzien dla Confirmed i Probable.
    raise Exception("Not implemented")


def parse_non_district_to_summary(weekly_data, country_name, ):
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

            #TODO: Wytworzyc histogram tutaj
            #TODO: Dodac modele dalej

    client.close()
