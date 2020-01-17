import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

with open("../data/others/summary_genders.json", 'r') as f:
    gender_data = json.load(f)

facts = gender_data['fact']
labels = ['Male all ages(Total)', 'Female all ages(Total)', 'Both 0-14', 'Both 15-44', 'Both +45']
guinea = []
liberia = []
sierra = []
total = []

for dimx in facts:
    dim = dimx['dims']
    if dim['COUNTRY'] == 'Guinea':
        guinea.append({
            'Value': int(dimx['Value']),
            'Country': dim['COUNTRY'],
            'Type': dim['SEX'] + ' ' + dim['AGEGROUP']
        })
    elif dim['COUNTRY'] == 'Liberia':
        liberia.append({
            'Value': int(dimx['Value']),
            'Country': dim['COUNTRY'],
            'Type': dim['SEX'] + ' ' + dim['AGEGROUP']
        })
    elif dim['COUNTRY'] == 'Sierra Leone':
        sierra.append({
            'Value': int(dimx['Value']),
            'Country': dim['COUNTRY'],
            'Type': dim['SEX'] + ' ' + dim['AGEGROUP']
        })
    else:
        total.append({
            'Value': int(dimx['Value']),
            'Country': dim['COUNTRY'],
            'Type': dim['SEX'] + ' ' + dim['AGEGROUP']
        })

r1 = np.arange(len(labels))
width = 0.2
r2 = [x + width for x in r1]
r3 = [x + width for x in r2]
r4 = [x + width for x in r3]
plt.figure(figsize=(12, 5))
rects1 = plt.bar(r1, [dim['Value'] for dim in guinea], width, label='Guinea')
rects2 = plt.bar(r2, [dim['Value'] for dim in liberia], width, label='Liberia')
rects3 = plt.bar(r3, [dim['Value'] for dim in sierra], width, label='Sierra Leone')
rects4 = plt.bar(r4, [dim['Value'] for dim in total], width, label='Total countries')

 # width:20, height:3
def paint_rectangle_values(data):
    for rectangle in data:
        height = rectangle.get_height()
        if height == 0:
            continue
        plt.annotate('{}'.format(height),
                     xy=(rectangle.get_x() + rectangle.get_width() / 2, height),
                     xytext=(0, 2),
                     textcoords="offset points",
                     ha='center', va='bottom')


paint_rectangle_values(rects1)
paint_rectangle_values(rects2)
paint_rectangle_values(rects3)
paint_rectangle_values(rects4)
plt.xlabel('Genders in Ebola Case', fontweight='bold')
plt.xticks([r + width for r in range(len(total))], labels)

plt.legend()
plt.show()
