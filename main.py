import re
import csv
from itertools import groupby
from collections import OrderedDict
from itertools import chain

PHONE_PATTERN = r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*'
PHONE_SUB = r'+7(\2)\3-\4-\5 \6\7'

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contacts_new = []
for i in contacts_list:
    full_name = ' '.join(i[:3]).split()
    contacts_new.append(full_name + [i[3], i[4], re.sub(PHONE_PATTERN, PHONE_SUB, i[5]), i[6]])
contacts_new.sort(key=lambda x: (x[0], x[1]))

grouped_list = [list(data) for _, data in groupby(contacts_new, key=lambda x: (x[0], x[1]))]

res = [list(OrderedDict.fromkeys(chain(*x))) for x in grouped_list]

position = res[3].pop()
res[3][4] = position

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(res)
