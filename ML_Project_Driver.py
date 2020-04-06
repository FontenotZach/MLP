from pprint import pprint
import json
import sys
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from DataInterval import *
import statistics
import random
import numpy as np
import math

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

output_JSON = 0
output_CSV = 0
output_TXT = 0
output_XLSX = 0

learning_Proportion = 1
testing_Proportion = 0
degree_Proportion = 0

small_Interval = 0
default_Interval = 0
large_Interval = 0
interval_Size = 120

classes = [0, 1, 2, 3, 4, 5 ,6 ,7]

with open('options.json') as options:
    data = json.load(options)

parsedOptions = data['Feature Generation Options']

# check options
if ('JSON Input' in parsedOptions):
    input_JSON = 1
    print("JSON Input option not implemented")
    sys.exit()

if ('CSV Input' in parsedOptions):
    input_CSV = 1

if ('TXT Input (See README)' in parsedOptions):
    input_TXT = 1
    print("TXT Input option not implemented")
    sys.exit()

if ('XLSX Input' in parsedOptions):
    input_XLSX = 1
    print("XLSX Input option not implemented")
    sys.exit()

if ('All Files in Directory' in parsedOptions):
    files_This_Dir = 1
    print("All Files in Directory option not implemented")
    sys.exit()

if ('All Files in Tree' in parsedOptions):
    files_This_Dir_Tree = 1
    print("All Files in Tree option not implemented")
    sys.exit()

if ('Choose Files' in parsedOptions):
    files_File_Chooser = 1

if ('Small (~ 1 Second)' in parsedOptions):
    small_Interval = 1
    interval_Size = 60

if ('Default (~ 2 Seconds)' in parsedOptions):
    default_Interval = 1
    interval_Size = 120

if ('Large (~ 5 Seconds)' in parsedOptions):
    large_Interval = 1
    interval_Size = 300

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

if ('JSON Output' in parsedOptions):
    input_JSON = 1
    print("JSON Output option not implemented")
    sys.exit()

if ('CSV Output' in parsedOptions):
    input_CSV = 1

if ('TXT Output (See README)' in parsedOptions):
    input_TXT = 1
    print("TXT Output option not implemented")
    sys.exit()

if ('XLSX Output' in parsedOptions):
    input_XLSX = 1
    print("XLSX Output option not implemented")
    sys.exit()

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

if (small_Interval + default_Interval + large_Interval > 1):
    print("Choose only one interval size.")
if (small_Interval + default_Interval + large_Interval > 1):
    small_Interval = 0
    default_Interval = 1
    large_Interval = 0
    interval_Size = 120

root = Tk()
root.withdraw()
selectedFiles = filedialog.askopenfilenames(parent=root,title='Choose a file')
parsedFiles = root.splitlist(selectedFiles)

intervalList = []
activity = -1
# a bit hacky, consider alternate
for file in parsedFiles:
    if (file.find('KaCy') != -1):
        activity = 0
    if (file.find('KaDr') != -1):
        activity = 1
    if (file.find('KaRu') != -1):
        activity = 2
    if (file.find('KaSit') != -1):
        activity = 3
    if (file.find('KaSd') != -1):
        activity = 4
    if (file.find('KaSu') != -1):
        activity = 5
    if (file.find('KaSt') != -1):
        activity = 6
    if (file.find('KaWa') != -1):
        activity = 7
    with open(file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        numIntervals = 0
        time = []
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
                if (list(items)[0] != ''):
                    time.append(list(items)[0])
                    if (list(items)[2] != ''):
                        p1.append(list(items)[2])
                    if (list(items)[3] != ''):
                        p2.append(list(items)[3])
                    if (list(items)[4] != ''):
                        p3.append(list(items)[4])
                    if (list(items)[5] != ''):
                        p4.append(list(items)[5])
                    if (list(items)[6] != ''):
                        p5.append(list(items)[6])
                    if (list(items)[7] != ''):
                        p6.append(list(items)[7])
                    if (list(items)[8] != ''):
                        p7.append(list(items)[8])
                    if (list(items)[9] != ''):
                        p8.append(list(items)[9])
                line_count += 1
                if line_count % interval_Size == 0:
                    intervalList.append(DataInterval(-1, time, p1, p2, p3, p4, p5, p6, p7, p8, activity))
                    numIntervals += 1
                    time = []
                    p1 = []
                    p2 = []
                    p3 = []
                    p4 = []
                    p5 = []
                    p6 = []
                    p7 = []
                    p8 = []
        print(f'\nProcessed {line_count} lines into {numIntervals} intervals from file: \n\t{file}.')


print("\nGenerating features...")
x = []
y = []
for interval in intervalList:
    p1Float = [x for x in map(float, interval.p1)]
    p1Avg = sum(p1Float) / len(interval.p1)
    p1SD = statistics.pstdev(p1Float)
    #p1Mode = statistics.mode(p1Float)
    p1Median = statistics.median(p1Float)
    p1Var = statistics.pvariance(p1Float)

    p2Float = [x for x in map(float, interval.p2)]
    p2Avg = sum(p1Float) / len(interval.p2)
    p2SD = statistics.pstdev(p2Float)
    #p2Mode = statistics.mode(p2Float)
    p2Median = statistics.median(p2Float)
    p2Var = statistics.pvariance(p2Float)

    p3Float = [x for x in map(float, interval.p3)]
    p3Avg = sum(p1Float) / len(interval.p3)
    p3SD = statistics.pstdev(p3Float)
    #p3Mode = statistics.mode(p3Float)
    p3Median = statistics.median(p3Float)
    p3Var = statistics.pvariance(p3Float)

    p4Float = [x for x in map(float, interval.p4)]
    p4Avg = sum(p1Float) / len(interval.p4)
    p4SD = statistics.pstdev(p4Float)
    #p4Mode = statistics.mode(p4Float)
    p4Median = statistics.median(p4Float)
    p4Var = statistics.pvariance(p4Float)

    p5Float = [x for x in map(float, interval.p5)]
    p5Avg = sum(p1Float) / len(interval.p5)
    p5SD = statistics.pstdev(p5Float)
    #p5Mode = statistics.mode(p5Float)
    p5Median = statistics.median(p5Float)
    p5Var = statistics.pvariance(p5Float)

    p6Float = [x for x in map(float, interval.p6)]
    p6Avg = sum(p1Float) / len(interval.p6)
    p6SD = statistics.pstdev(p6Float)
    #p6Mode = statistics.mode(p6Float)
    p6Median = statistics.median(p6Float)
    p6Var = statistics.pvariance(p6Float)

    p7Float = [x for x in map(float, interval.p7)]
    p7Avg = sum(p1Float) / len(interval.p7)
    p7SD = statistics.pstdev(p7Float)
    #p7Mode = statistics.mode(p7Float)
    p7Median = statistics.median(p7Float)
    p7Var = statistics.pvariance(p7Float)

    p8Float = [x for x in map(float, interval.p8)]
    p8Avg = sum(p1Float) / len(interval.p8)
    p8SD = statistics.pstdev(p8Float)
    #p8Mode = statistics.mode(p8Float)
    p8Median = statistics.median(p8Float)
    p8Var = statistics.pvariance(p8Float)

    act = interval.activity
    features = []

    features.append(p1Avg)
    #features.append(p1Mode)
    features.append(p1Median)
    features.append(p1Var)
    features.append(p1SD)

    features.append(p2Avg)
    #features.append(p2Mode)
    features.append(p2Median)
    features.append(p2Var)
    features.append(p2SD)

    features.append(p3Avg)
    #features.append(p3Mode)
    features.append(p3Median)
    features.append(p3Var)
    features.append(p3SD)

    features.append(p4Avg)
    #features.append(p4Mode)
    features.append(p4Median)
    features.append(p4Var)
    features.append(p4SD)

    features.append(p5Avg)
    #features.append(p5Mode)
    features.append(p5Median)
    features.append(p5Var)
    features.append(p5SD)

    features.append(p6Avg)
    #features.append(p6Mode)
    features.append(p6Median)
    features.append(p6Var)
    features.append(p6SD)

    features.append(p7Avg)
    #features.append(p7Mode)
    features.append(p7Median)
    features.append(p7Var)
    features.append(p7SD)

    features.append(p8Avg)
    #features.append(p8Mode)
    features.append(p8Median)
    features.append(p8Var)
    features.append(p8SD)

    x.append(features)
    y.append(act)

#features compiled
cycling = 0
driving = 0
running = 0
sitting = 0
standing = 0
stair_up = 0
stair_down = 0
walking = 0

for act in y:
    if act == 0:
        cycling += 1
    if act == 1:
        driving += 1
    if act == 2:
        running += 1
    if act == 3:
        sitting += 1
    if act == 4:
        standing += 1
    if act == 5:
        stair_up += 1
    if act == 6:
        stair_down += 1
    if act == 7:
        walking += 1

print("\nTotal intervals for each activity:")
print(f"\tcycling: \t{cycling}")
print(f"\tdriving: \t{driving}")
print(f"\trunning: \t{running}")
print(f"\tsitting: \t{sitting}")
print(f"\tstanding: \t{standing}")
print(f"\tstairs up: \t{stair_up}")
print(f"\tstairs down: \t{stair_down}")
print(f"\twalking: \t{walking}")

x_Learn = []
y_Learn = []
x_Test = []
y_Test = []
x_Degree = []
y_Degree = []

if proportion_L100 == 0:
    print("\nSplitting data...")
    for row in x:
        row.insert(0, 1)
        rand = random.randint(0,100) / 100
        if rand < learning_Proportion:
            x_Learn.append(row)
        elif rand - learning_Proportion < testing_Proportion:
            x_Test.append(row)
        else:
            x_Degree.append(row)

with open('learningActivity.csv', 'w', newline='') as f:
     wr = csv.writer(f, quoting=csv.QUOTE_ALL)
     wr.writerow(y_Learn)

with open("learningData.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(x_Learn)

if testing_Proportion > 0:
    with open("testingData.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(x_Test)
    with open("testingActivity.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(y_Test)

if degree_Proportion > 0:
    with open("degreeData.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(x_Degree)
    with open("degreeActivity.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(y_Degree)

a = np.array(x_Learn)
b = np.array(y_Learn)
s = (len(classes), np.size(a,1))

all_Theta = np.zeros(s)

for i in classes:
    index = 0
    theta = all_Theta[i]
    result = b
    for j in b:
        if j == i:
            result[index] = 1
        else:
            result[index] = 0
        index += 1
    z = np.dot(a, theta)
    h = 1.0 / (1.0 + np.power(math.e, z))

prediction = np.dot(a, theta)
print(a.shape)
print(prediction.shape)
