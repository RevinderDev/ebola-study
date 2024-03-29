import re
from collections import defaultdict


class WeeklyData:

    def __init__(self, country_name, weekly_report=None, interval=1):
        self.country_name = country_name
        self.interval = interval * 2  # because the data is in set of 2

        self.probable = []
        self.confirmed = []
        self.location = None
        self.missing_data_confirmed = []
        self.missing_data_probable = []

        if weekly_report is not None:
            self.__parse_fields__(weekly_report)
        self.probable = self.__squish_intervals__(self.probable)
        self.confirmed = self.__squish_intervals__(self.confirmed)

    def __parse_fields__(self, weekly_report):
        try:
            self.location = weekly_report['fact'][0]['dims']['LOCATION'].capitalize()
        except KeyError:
            pass

        for report in weekly_report['fact']:
            missing_value_found = False
            dims = report['dims']
            try:
                value = int(report['Value'])
            except ValueError:
                value = 0
            case = {
                'value': value,
                'week': re.search(r'(\(.*\))', dims['EPI_WEEK']).group(0)  # pulls () part from date
            }
            if dims['CASE_DEFINITION'] == 'Confirmed':
                if missing_value_found:
                    self.missing_data_confirmed.append(case)
                else:
                    self.confirmed.append(case)
            elif dims['CASE_DEFINITION'] == 'Probable':
                if missing_value_found:
                    self.missing_data_probable.append(case)
                else:
                    self.probable.append(case)

    def __squish_intervals__(self, list_to_squish):
        if self.interval == 2:
            return list_to_squish
        new_list = []
        tmp_list = []
        for i, dic in enumerate(list_to_squish, 1):
            tmp_list.append(dic)
            if i % self.interval == 0:
                new_list.append({
                    'value': sum(item['value'] for item in tmp_list),
                    'week': tmp_list[0]['week'] + ' - ' + tmp_list[-1]['week']
                })
                tmp_list.clear()
        return new_list

    @staticmethod
    def sum_all_weekly(list_of_weeklies, country_name):
        summed_weekly = WeeklyData(country_name=country_name)
        probables_list = []
        confirmed_list = []
        for weekly_data in list_of_weeklies:
            probables_list.append(weekly_data.probable)
            confirmed_list.append(weekly_data.confirmed)

        summed_weekly.probable = WeeklyData.__sum_case_list__(probables_list)
        summed_weekly.confirmed = WeeklyData.__sum_case_list__(confirmed_list)
        return summed_weekly

    @staticmethod
    def __sum_case_list__(list_to_sum):
        tmp_dict = defaultdict(int)
        for list_of_dictionaries in list_to_sum:
            for case in list_of_dictionaries:
                tmp_dict[case['week']] += case['value']
        new_list = []
        for key, value in tmp_dict.items():
            new_list.append({
                'value': value,
                'week': key
            })

        return new_list

    @staticmethod
    def sum_number_of_records(list_of_number_of_records) -> defaultdict:
        sum_to_ret = defaultdict(int)
        for record in list_of_number_of_records:
            sum_to_ret['Missing_Probable'] += record['Missing_Probable']
            sum_to_ret['Missing_Confirmed'] += record['Missing_Confirmed']
            sum_to_ret['Confirmed'] += record['Confirmed']
            sum_to_ret['Probable'] += record['Probable']
            sum_to_ret['Total_Missing'] += record['Missing_Probable'] + record['Missing_Confirmed']
            sum_to_ret['Total_Records'] += record['Confirmed'] + record['Probable']

        return sum_to_ret

    def get_number_of_records(self) -> dict:
        return {
            'Country': self.country_name,
            'Location': self.location,
            'Missing_Probable': len(self.missing_data_probable),
            'Missing_Confirmed': len(self.missing_data_confirmed),
            'Confirmed': len(self.confirmed),
            'Probable': len(self.probable)
        }
