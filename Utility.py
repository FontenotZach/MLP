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
from scipy.optimize import minimize
from tqdm import tqdm
from time import sleep

def cost(theta, result, a, lambdaVal):
    z = np.dot(a, theta)
    z = z * -1

    counter = 0
    for element in z:
        if element > 21:
            z[counter] = 21
        counter += 1
    h = 1.0 / (1.0 + np.power(math.e, z))
    counter = 0
    for element in h:
        if element <= 0:
            h[counter] = .01
        if element >= 1:
            h[counter] = 1
        counter += 1
    p1 = (-1 * result) * np.log(h)
    p2 = (1 - result) * np.log(1 - h)
    p = (p1 - p2)
    J = np.sum(p) / np.size(a, 0)
    reg = np.sum(np.power(theta, 2))
    J += lambdaVal * reg
    return J * 100

def predict(x, y, models):
    classNames = ["Cycling", "Driving", "Running", "Sitting", "Standing", "St Up", "St Down", "Walking"]
    biasBaseline = 20
    bias = biasBaseline
    models = np.transpose(models)
    prediction = np.dot(x, models)
    index = 0
    good = np.zeros(np.size(models,0))
    total = np.zeros(np.size(models,0))
    s = (np.size(models,0), np.size(models,1))
    wrong = np.zeros(s)
    lastPrediction = -1
    for p in prediction:
        if lastPrediction != -1:
            p[lastPrediction] += bias
        if (np.argmax(p) == y[index]):
            #print(f"Correct {classNames[y[index]]}=={classNames[np.argmax(p)]} bias={bias}")
            good[np.argmax(p)] += 1
        else:
            #print(f"Wrong {classNames[y[index]]}!={classNames[np.argmax(p)]} bias={bias}")
            wrong[y[index]][np.argmax(p)] += 1
        ### if prediction was repeaeted, decrease the bias ###
        if np.argmax(p) == lastPrediction:
            bias *= .9
        else:
            bias = biasBaseline
        if bias < 1.1:
            bias = 1.1
        total[np.argmax(p)] += 1
        lastPrediction = np.argmax(p)
        index += 1
    return (good, total, wrong)

def generateModels(xLearn, yLearn, classes, lambdaVal):
    a = np.array(xLearn)
    b = np.array(yLearn)
    s = (classes, np.size(a,1))

    allTheta = np.zeros(s)
    models = []

    pbar = tqdm(total=classes, desc="Generating Models One vs All", ascii=" ░▒█")

    for i in range(0, classes):
        index = 0
        theta = allTheta[i]
        result = b.copy()
        for j in b:
            if j == i:
                result[index] = 1
            else:
                result[index] = 0
            index += 1
        res = minimize(cost, theta, args=(result, a, lambdaVal), method='nelder-mead')
        pbar.update()
        models.append(res.x)
    pbar.close()
    return models

def post(fileName, list):
    npArray = np.array(list)
    with open(fileName, 'w', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        if npArray.ndim == 1:
            wr.writerow(npArray)
        else:
            wr.writerows(npArray)

def getFiles():
    root = Tk()
    root.withdraw()
    selectedFiles = filedialog.askopenfilenames(parent=root,title='Choose a file')
    parsedFiles = root.splitlist(selectedFiles)
    return parsedFiles

def generateFeatures(intervalList, numDataPoints, numFeatures):
    numIters = len(intervalList) * numFeatures * numDataPoints
    pbar = tqdm(total=numIters, desc="Generating Features", ascii=" ░▒█")

    x = []
    y = []
    for interval in intervalList:
        features = []
        act = interval.activity
        sensors = [[x for x in map(float, interval.p1)], [x for x in map(float, interval.p2)], [x for x in map(float, interval.p3)], [x for x in map(float, interval.p4)], [x for x in map(float, interval.p5)], [x for x in map(float, interval.p6)], [x for x in map(float, interval.p7)],[x for x in map(float, interval.p8)],[x for x in map(float, interval.aX)],[x for x in map(float, interval.aY)],[x for x in map(float, interval.aZ)]]
        sensors.append(np.sqrt(np.power(sensors[8], 2) + np.power(sensors[9], 2) + np.power(sensors[10], 2)))
        sensors.append(sensors[0] + sensors[1])
        sensors.append(sensors[2] + sensors[3])
        sensors.append(sensors[4] + sensors[5] + sensors[6])
        for i in range(0, len(sensors)):
            pFloat = sensors[i]
            pAvg = sum(pFloat) / len(sensors[i])
            pSD = statistics.pstdev(pFloat)
            pMedian = statistics.median(pFloat)
            pQ1 = np.percentile(sensors[i], 25)
            pQ3 = np.percentile(sensors[i], 75)
            pVar = statistics.pvariance(pFloat)
            pMax = np.max(pFloat)
            pMin = np.min(pFloat)
            pRange = pMin - pMax

            features.append(pAvg)
            features.append(pMedian)
            features.append(pVar)
            features.append(pSD)
            features.append(pQ1)
            features.append(pQ3)
            features.append(pMax)
            features.append(pMin)
            features.append(pRange)
            pbar.update(numFeatures)
        x.append(features)
        y.append(act)

    pbar.close()
    return (x, y)

def generateIntervals(parsedFiles, intervalSize):
    intervalList = []
    activity = -1

    pbar = tqdm(total=len(parsedFiles), desc="Processing Files", ascii=" ░▒█")


    for file in parsedFiles:
        if (file.find('KaCy') != -1):
            activity = 0
        if (file.find('KaDr') != -1):
            activity = 3
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

        with open(file) as csvfile:
            csvreader = csv.DictReader(csvfile)
            linecount = 0
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
            aX = []
            aY = []
            aZ = []
            for row in csvreader:
                if linecount == 0:
                    linecount += 1
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
                        if (list(items)[10] != ''):
                            aX.append(list(items)[10])
                        if (list(items)[11] != ''):
                            aY.append(list(items)[11])
                        if (list(items)[12] != ''):
                            aZ.append(list(items)[12])
                    linecount += 1
                    if linecount % intervalSize == 0:
                        intervalList.append(DataInterval(-1, time, p1, p2, p3, p4, p5, p6, p7, p8, aX, aY, aZ, activity))
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
                        aX = []
                        aY = []
                        aZ = []
        pbar.update()
    pbar.close()
    return intervalList

def printIntervals(y):

    #features compiled
    cycling = 0
    driving = 0
    running = 0
    sitting = 0
    standing = 0
    stairup = 0
    stairdown = 0
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
            stairup += 1
        if act == 6:
            stairdown += 1
        if act == 7:
            walking += 1
    print("\n\tTotal intervals for each activity:")
    print(f"\t\tcycling: \t{cycling}")
    #print(f"\tdriving: \t{driving}")
    print(f"\t\trunning: \t{running}")
    print(f"\t\tsitting: \t{sitting}")
    print(f"\t\tstanding: \t{standing}")
    print(f"\t\tstairs up: \t{stairup}")
    print(f"\t\tstairs down: \t{stairdown}")
    print(f"\t\twalking: \t{walking}\n")

def addBias(x):
    for row in x:
        row.insert(0, 1)
    return x


def splitData(x, y, learningProportion, testingProportion, crossValidationProportion):
    xLearn = []
    yLearn = []
    xTest = []
    yTest = []
    xCrossValidation = []
    yCrossValidation = []
    #pbar = tqdm(total=len(x), desc="Splitting Data", ascii=" ░▒█")
    index = 0
    for row in x:
        #pbar.update()
        rand = random.randint(0,100) / 100
        if rand < learningProportion:
            xLearn.append(row)
            yLearn.append(y[index])
        elif rand - learningProportion < testingProportion:
            xTest.append(row)
            yTest.append(y[index])
        else:
            xCrossValidation.append(row)
            yCrossValidation.append(y[index])
        index += 1
    #pbar.close()

    post('learningData.csv', xLearn)
    post('learningActivity.csv', yLearn)

    if testingProportion > 0:
        post('testingData.csv', xTest)
        post('testingActivity.csv', yTest)

    if crossValidationProportion > 0:
        post('crossValidationData.csv', xCrossValidation)
        post('crossValidationActivity.csv', yCrossValidation)

    return (xLearn, yLearn, xTest, yTest, xCrossValidation, yCrossValidation)

def selectData(intervalList, stdDev, classes):
    total = 0
    bad = 0
    selectedList = []
    pbar = tqdm(total=len(intervalList), desc="Cleaning Data", ascii=" ░▒█")
    for interval in intervalList:
        invalidIndex = []
        sensors = [[x for x in map(float, interval.p1)], [x for x in map(float, interval.p2)], [x for x in map(float, interval.p3)], [x for x in map(float, interval.p4)], [x for x in map(float, interval.p5)], [x for x in map(float, interval.p6)], [x for x in map(float, interval.p7)],[x for x in map(float, interval.p8)],[x for x in map(float, interval.aX)],[x for x in map(float, interval.aY)],[x for x in map(float, interval.aZ)]]
        for i in range(0, len(sensors)):
            pQ1 = np.percentile(sensors[i], 25)
            pQ3 = np.percentile(sensors[i], 75)
            IQR = pQ3 - pQ1
            for j in sensors[i]:
                if (pQ3 + ( stdDev * IQR)) < j:
                    sensors[i].remove(j)
                    bad+= 1
                if (pQ1 - ( stdDev * IQR)) > j:
                    sensors[i].remove(j)
                    bad +=1
                total +=1
        interval.p1 = sensors[0]
        interval.p2 = sensors[1]
        interval.p3 = sensors[2]
        interval.p4 = sensors[3]
        interval.p5 = sensors[4]
        interval.p6 = sensors[5]
        interval.p7 = sensors[6]
        interval.p8 = sensors[7]

        pbar.update()
    pbar.close()
    return intervalList
