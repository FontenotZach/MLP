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
from scipy import misc
import Gradient as gr
from scipy.optimize import minimize
from scipy.optimize import fmin_bfgs, fmin_l_bfgs_b
from tqdm import tqdm
from time import sleep
from Options import *

with open('options.json') as options:
    data = json.load(options)

parsedOptions = data['Feature Generation Options']
learning_Proportion = float(data['learning'])
testing_Proportion = float(data['learning'])
cross_Validation_Proportion = float(data['learning'])
classes = int(data['classes'])

opt = Options(parsedOptions, learning_Proportion, testing_Proportion, cross_Validation_Proportion, classes)
if not bool(opt.valid):
    print(opt.error)
    sys.exit()

opt.checkOptions()
if not bool(opt.valid):
    print(opt.error)
    sys.exit()

interval_Size = opt.interval_Size
parsedFiles = gr.getFiles()

intervalList = []
activity = -1

pbar = tqdm(total=len(parsedFiles), desc="Processing Files", ascii=" ░▒█")

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
    pbar.update()
pbar.close()
print("Done.")

numDataPoints = 9
numFeatures = 5 * numDataPoints
numIters = len(intervalList) * numFeatures * 7
pbar = tqdm(total=numIters, desc="Generating Features", ascii=" ░▒█")

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
    features.append(p1Var)

    pbar.update(numFeatures)

    features.append(p2Avg)
    #features.append(p2Mode)
    features.append(p2Median)
    features.append(p2Var)
    features.append(p2SD)
    features.append(p2Var)

    pbar.update(numFeatures)

    features.append(p3Avg)
    #features.append(p3Mode)
    features.append(p3Median)
    features.append(p3Var)
    features.append(p3SD)
    features.append(p3Var)

    pbar.update(numFeatures)

    features.append(p4Avg)
    #features.append(p4Mode)
    features.append(p4Median)
    features.append(p4Var)
    features.append(p4SD)
    features.append(p4Var)

    features.append(p5Avg)
    #features.append(p5Mode)
    features.append(p5Median)
    features.append(p5Var)
    features.append(p5SD)
    features.append(p5Var)

    pbar.update(numFeatures)

    features.append(p6Avg)
    #features.append(p6Mode)
    features.append(p6Median)
    features.append(p6Var)
    features.append(p6SD)
    features.append(p6Var)

    pbar.update(numFeatures)

    features.append(p7Avg)
    #features.append(p7Mode)
    features.append(p7Median)
    features.append(p7Var)
    features.append(p7SD)
    features.append(p7Var)

    pbar.update(numFeatures)

    features.append(p8Avg)
    #features.append(p8Mode)
    features.append(p8Median)
    features.append(p8Var)
    features.append(p8SD)
    features.append(p8Var)

    pbar.update(numFeatures)

    x.append(features)
    y.append(act)
pbar.close()
print("Done.")

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

x_Learn = []
y_Learn = []
x_Test = []
y_Test = []
x_Cross_Validation = []
y_Cross_Validation = []
pbar = tqdm(total=len(x), desc="Splitting Data", ascii=" ░▒█")
index = 0
for row in x:
    pbar.update()
    row.insert(0, 1)
    rand = random.randint(0,100) / 100
    if rand < learning_Proportion:
        x_Learn.append(row)
        y_Learn.append(y[index])
    elif rand - learning_Proportion < testing_Proportion:
        x_Test.append(row)
        y_Test.append(y[index])
    else:
        x_Cross_Validation.append(row)
        y_Cross_Validation.append(y[index])
    index += 1
pbar.close()
print("Done.")

gr.post('learningData.csv', x_Learn)
gr.post('learningActivity.csv', y_Learn)

if testing_Proportion > 0:
    gr.post('testingData.csv', x_Test)
    gr.post('testingActivity.csv', y_Test)

if cross_Validation_Proportion > 0:
    gr.post('cross_ValidationData.csv', x_Cross_Validation)
    gr.post('cross_ValidationActivity.csv', y_Cross_Validation)


models = gr.generateModels(x_Learn, y_Learn, classes)

gr.post('models.csv', models)

prediction = gr.predict(x_Test, y_Test, models)

print("\nTotal intervals for each activity:")
print(f"\tcycling: \t{cycling}")
print(f"\tdriving: \t{driving}")
print(f"\trunning: \t{running}")
print(f"\tsitting: \t{sitting}")
print(f"\tstanding: \t{standing}")
print(f"\tstairs up: \t{stair_up}")
print(f"\tstairs down: \t{stair_down}")
print(f"\twalking: \t{walking}")

print("\n\n\tModel Accuracy = ")
print(prediction[0]/prediction[1])
