import json
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np


def create_hist(data):
    names = []
    values = []
    title = "Total summary as of " + data[0]['dims']['COUNTRY']

    for data_object in data:
        try:
            values.append(int(data_object['Value']))
        except ValueError:
            continue
        name_str = data_object['dims']['CASE_DEFINITION'] + '-' + data_object['dims']['EBOLA_MEASURE']
        names.append(name_str)

    y_pos = np.arange(len(values))

    rects = plt.bar(y_pos, values)

    plt.ylabel('Value', fontsize=10)
    plt.xticks(y_pos, names, fontsize=10, rotation=45)
    plt.title(title, fontsize=10)
    for rectangle in rects:
        height = rectangle.get_height()
        plt.annotate('{}'.format(height),
                    xy=(rectangle.get_x() + rectangle.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    plt.show()


def parse_summary_patients(db_dict):
    data_objects = db_dict['fact']

    guinea_objects = []
    sierra_leone_objects = []
    liberia_objects = []

    for fact_object in data_objects:
        if fact_object['dims']['COUNTRY'] == 'Guinea':
            guinea_objects.append(fact_object)
        elif fact_object['dims']['COUNTRY'] == 'Sierra Leone':
            sierra_leone_objects.append(fact_object)
        elif fact_object['dims']['COUNTRY'] == 'Liberia':
            liberia_objects.append(fact_object)

    create_hist(guinea_objects)
    create_hist(liberia_objects)
    create_hist(sierra_leone_objects)


def create_query_dict(parameters, values):
    return dict(zip(parameters, values))


if __name__ == '__main__':
    with open('../db_auth.json') as json_file:
        auth_data = json.load(json_file)
        client = MongoClient(auth_data['client_string'])

    db_summary = client['Summaries']
    document = db_summary['summary_patients']
    parse_summary_patients(document.find().next())

    client.close()