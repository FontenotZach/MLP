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
import Utility as gr
from scipy.optimize import minimize
from tqdm import tqdm
from Options import *
### OPTIONS PARSING/CHECKING ###
with open('options.json') as options:
    data = json.load(options)
parsedOptions = data['Feature Generation Options']
learningProportion = float(data['learning'])
testingProportion = float(data['learning'])
crossValidationProportion = float(data['learning'])
classes = int(data['classes'])
opt = Options(parsedOptions, learningProportion, testingProportion, crossValidationProportion, classes)
if not bool(opt.valid):
    print(opt.error)
    sys.exit()
opt.checkOptions()
if not bool(opt.valid):
    print(opt.error)
    sys.exit()
intervalSize = opt.intervalSize
parsedFiles = gr.getFiles()
### GENERATE INTERVALS ###
intervalList = gr.generateIntervals(parsedFiles, intervalSize)
print("Done generating intervals.")
### REMOVE BAD DATA ###
stdDev = 1.5
intervalList = gr.selectData(intervalList, stdDev, classes)
### GENERATE FEATURES ###
numDataPoints = 11
numFeatures = 9 * numDataPoints
data = gr.generateFeatures(intervalList, numDataPoints, numFeatures)
x = data[0]
y = data[1]
gr.printIntervals(y)
print("Done generating features.")
### NUMBER OF RUNS ###
for k in range(0,6):
    ### SPLIT DATA ###
    splitData = gr.splitData(x, y, learningProportion, testingProportion, crossValidationProportion)
    xLearn = splitData[0]
    yLearn = splitData[1]
    xTest = splitData[2]
    yTest = splitData[3]
    xCrossValidation = splitData[4]
    yCrossValidation = splitData[5]
    ### GENERATE MODELS ###
    models = gr.generateModels(xLearn, yLearn, classes)
    gr.post('models.csv', models)
    ### CHECK ACCURACY ###
    if testingProportion > 0:
        good = 0
        total = 0
        predictions = []
        prediction = gr.predict(xTest, yTest, models)
        print("Errors")
        for i in range(0, classes):
            print(prediction[2][i])
        print()
        print("\n\n\tModel Accuracy = ")
        for i in range(0, classes):
            if (i != 1):
                good += prediction[0][i]
                total += prediction[1][i]
                p = prediction[0][i]/prediction[1][i]
                predictions.append(p)
                print(p)
        print("Total Accuracy")
        print(good/total)
        with open('accuracyIn.csv', 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(predictions)
