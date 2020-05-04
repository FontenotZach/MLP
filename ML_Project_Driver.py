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
import os
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler



os.system('cls')
print()
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
### REMOVE BAD DATA ###
stdDev = 1.5
intervalList = gr.selectData(intervalList, stdDev, classes)
### GENERATE FEATURES ###
numDataPoints = 15
numFeatures = 9 * numDataPoints
data = gr.generateFeatures(intervalList, numDataPoints, numFeatures)
x = data[0]
y = data[1]
gr.printIntervals(y)
x = gr.addBias(x)


### Finding Optimal Layers
# learningAccMatrix = []
# validationAccMatrix = []
#
# networkIter = 10
# pbar = tqdm(total=(6*6*networkIter), desc="Generating Optimal Neural Network", ascii=" ░▒█")
# for layer1 in range(4, 10):
#     learningAccRow = []
#     validationAccRow = []
#     for layer2 in range(2,8):
#         for i in range(0,networkIter):
#             learningAcc = []
#             validationAcc = []
#
#             # neural network
#             splitData = gr.splitData(x, y, learningProportion, testingProportion, crossValidationProportion)
#             xLearn = splitData[0]
#             yLearn = splitData[1]
#             xTest = splitData[2]
#             yTest = splitData[3]
#             xCrossValidation = splitData[4]
#             yCrossValidation = splitData[5]
#
#
#             clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(layer1, layer2), random_state=1)
#             clf.fit(xLearn, yLearn)
#
#             prediction = clf.predict(xTest)
#             predictionCorrectness = prediction - yTest
#             error = np.count_nonzero(predictionCorrectness)
#             errorProportion = error/np.size(yTest)
#             validationAcc.append(errorProportion)
#
#             prediction = clf.predict(xLearn)
#             predictionCorrectness = prediction - yLearn
#             error = np.count_nonzero(predictionCorrectness)
#             errorProportion = error/np.size(yLearn)
#             learningAcc.append(errorProportion)
#
#             pbar.update()
#
#         learningAccRow.append(np.sum(learningAcc)/ len(learningAcc))
#         validationAccRow.append(np.sum(validationAcc)/ len(validationAcc))
#     learningAccMatrix.append(learningAccRow)
#     validationAccMatrix.append(validationAccRow)
# pbar.close()
# gr.post("LearningAccuracy.csv", learningAccMatrix)
# gr.post("ValidationAccuracy.csv", validationAccMatrix)

scaler = StandardScaler()
scaler.fit(x)

splitData = gr.splitData(x, y, learningProportion, testingProportion, crossValidationProportion)
xLearn = splitData[0]
yLearn = splitData[1]
xTest = splitData[2]
yTest = splitData[3]
xCrossValidation = splitData[4]
yCrossValidation = splitData[5]

clf = MLPClassifier(solver='lbfgs', alpha=.1, hidden_layer_sizes=(8, 2), learning_rate_init=3)
clf.fit(xLearn, yLearn)

prediction = clf.predict(xTest)
predictionCorrectness = prediction - yTest
error = np.count_nonzero(predictionCorrectness)
errorProportion = error/np.size(yTest)
print("Testing Error:")
print(errorProportion)

prediction = clf.predict(xLearn)
predictionCorrectness = prediction - yLearn
error = np.count_nonzero(predictionCorrectness)
errorProportion = error/np.size(yLearn)
print("Learning Error:")
print(errorProportion)

# LogReg
# ### NUMBER OF RUNS ###
# for k in range(0,6):
#     ### SPLIT DATA ###
#     splitData = gr.splitData(x, y, learningProportion, testingProportion, crossValidationProportion)
#     xLearn = splitData[0]
#     yLearn = splitData[1]
#     xTest = splitData[2]
#     yTest = splitData[3]
#     xCrossValidation = splitData[4]
#     yCrossValidation = splitData[5]
#     ### GENERATE MODELS ###
#     lambdaVal = .1
#     models = gr.generateModels(xLearn, yLearn, classes, lambdaVal)
#     gr.post('models.csv', models)
#     ### CHECK ACCURACY ###
#     if testingProportion > 0:
#         good = 0
#         total = 0
#         predictions = []
#         prediction = gr.predict(xTest, yTest, models)
#         # print("Errors")
#         # for i in range(0, classes):
#         #     print(prediction[2][i])
#         print()
#         #print("\n\n\tModel Accuracy = ")
#         for i in range(0, classes):
#             if (i != 1):
#                 good += prediction[0][i]
#                 total += prediction[1][i]
#                 p = prediction[0][i]/prediction[1][i]
#                 predictions.append(p)
#                 #print(p)
#         print("Testing Accuracy: ")
#         print(good/total)
#
#         prediction = gr.predict(xLearn, yLearn, models)
#         print()
#         for i in range(0, classes):
#             if (i != 1):
#                 good += prediction[0][i]
#                 total += prediction[1][i]
#                 p = prediction[0][i]/np.sum(prediction[1][i])
#                 predictions.append(p)
#                 #print(p)
#         print("Learning Accuracy: ")
#         print(good/total)
#         print()
#         with open('accuracyIn.csv', 'a+', newline='') as write_obj:
#             # Create a writer object from csv module
#             csv_writer = csv.writer(write_obj)
#             # Add contents of list as last row in the csv file
#             csv_writer.writerow(predictions)
