import re


class WeeklyData:

    def __init__(self, weekly_report, country_name, interval=1):
        self.country_name = country_name
        self.interval = interval * 2  # because the data is in set of 2

        self.probable = []
        self.confirmed = []

        self.__parse_fields__(weekly_report)
        self.probable = self.__squish_intervals__(self.probable)
        self.confirmed = self.__squish_intervals__(self.confirmed)

    def __parse_fields__(self, weekly_report):
        try:
            self.location = weekly_report['fact'][0]['dims']['LOCATION'].capitalize()
        except KeyError:
            self.location = ''

        for report in weekly_report['fact']:
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
                self.confirmed.append(case)
            elif dims['CASE_DEFINITION'] == 'Probable':
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
