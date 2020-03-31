from pprint import pprint
import json
import sys
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from DataInterval import *

input_JSON = 0
input_CSV = 0
input_TXT = 0
input_XLSX = 0

files_This_Dir = 0
files_This_Dir_Tree = 0
files_File_Chooser = 0

proportion_L100 = 0
proportion_L70_T30 = 0
proportion_L70_T15_D15 = 0
proportion_L60_T20_D20 = 0

learning_Proportion = 1
testing_Proportion = 0
degree_Proportion = 0

with open('options.json') as options:
    data = json.load(options)
pprint(data)

parsedOptions = data['Feature Generation Options']

# check options
if ('JSON Input' in parsedOptions):
    input_JSON = 1

if ('CSV Input' in parsedOptions):
    input_CSV = 1

if ('TXT Input (See README)' in parsedOptions):
    input_TXT = 1

if ('XLSX Input' in parsedOptions):
    input_XLSX = 1

if ('All Files in Directory' in parsedOptions):
    files_This_Dir = 1

if ('All Files in Tree' in parsedOptions):
    files_This_Dir_Tree = 1

if ('Choose Files' in parsedOptions):
    files_File_Chooser = 1

if ('Learning:100' in parsedOptions):
    proportion_L100 = 1
    learning_Proportion = 1

if ('Learning:70|Testing:30' in parsedOptions):
    proportion_L70_T30 = 1
    learning_Proportion = .70
    testing_Proportion = .30

if ('Learning:70|Testing:15|Degree:15' in parsedOptions):
    proportion_L70_T15_D15 = 1
    learning_Proportion = .70
    testing_Proportion = .15
    degree_Proportion = .15

if ('Learning:60|Testing:20|Degree:20' in parsedOptions):
    proportion_L60_T20_D20 = 1
    learning_Proportion = .60
    testing_Proportion = .20
    degree_Proportion = .20

#check inputs
if (input_CSV + input_TXT + input_JSON + input_XLSX > 1):
    print("Choose only one input type.")
    sys.exit()

if (input_CSV + input_TXT + input_JSON + input_XLSX < 1):
    print("Choose an input type")
    sys.exit()

if (files_This_Dir + files_File_Chooser + files_This_Dir_Tree > 1):
    print("Choose only one file location.")
    sys.exit()

if (files_This_Dir + files_File_Chooser + files_This_Dir_Tree < 1):
    print("Choose a file location.")
    sys.exit()

if (proportion_L100 + proportion_L70_T30 + proportion_L60_T20_D20 + proportion_L70_T15_D15 > 1):
    print("Choose only one proprtion.")
    sys.exit()

if (proportion_L100 + proportion_L70_T30 + proportion_L60_T20_D20 + proportion_L70_T15_D15 > 1):
    print("Choose a proprtion.")
    sys.exit()

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
root = Tk()
selectedFiles = filedialog.askopenfilenames(parent=root,title='Choose a file')
print(selectedFiles)
parsedFiles = root.splitlist(selectedFiles)
print(parsedFiles)

intervalList = []
i = -1
activity = -1

for file in parsedFiles:
    if (file.find('Cy') != -1):
        activity = 0
    if (file.find('Dr') != -1):
        activity = 1
    if (file.find('Ru') != -1):
        activity = 2
    if (file.find('Sit') != -1):
        activity = 3
    if (file.find('Sd') != -1):
        activity = 4
    if (file.find('Su') != -1):
        activity = 5
    if (file.find('St') != -1):
        activity = 6
    if (file.find('Wa') != -1):
        activity = 7
    print(file)
    with open(file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        p1 = []
        p2 = []
        p3 = []
        p4 = []
        p5 = []
        p6 = []
        p7 = []
        p8 = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                items = row.values()
                p1.append(list(items)[2])
                p2.append(list(items)[3])
                p3.append(list(items)[4])
                p4.append(list(items)[5])
                p5.append(list(items)[6])
                p6.append(list(items)[7])
                p7.append(list(items)[8])
                p8.append(list(items)[9])
                line_count += 1
        intervalList.append(DataInterval(-1, p1, p2, p3, p4, p5, p6, p7, p8, activity))
        i += 1
        print(f'Processed {line_count} lines.')

print(intervalList[0].p1[0])
print(intervalList[1].p1[0])

print(intervalList[0].activity)
print(intervalList[1].activity)
