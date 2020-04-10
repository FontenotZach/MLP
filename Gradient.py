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
from scipy.optimize import fmin_bfgs, fmin_l_bfgs_b
from tqdm import tqdm
from time import sleep

def cost(theta, result, a):
    z = np.dot(a, theta)
    z = z * -1

    counter = 0
    for element in z:
        if element > 21:
            z[counter] = 21
        counter += 1
    # print()
    # print("z")
    # print(z.shape)
    # print(z)
    h = 1.0 / (1.0 + np.power(math.e, z))
    # print("h")
    # print(h.shape)
    # print(h)
    counter = 0
    for element in h:
        if element <= 0:
            h[counter] = .01
        if element >= 1:
            h[counter] = .99
        counter += 1
    p1 = (-1 * result) * np.log(h)
    # print(p1.shape)
    # print(p1)
    p2 = (1 - result) * np.log(1 - h)
    # print(p2.shape)
    # print(p2)
    p = (p1 - p2)
    # print(p.shape)
    # print(p)
    J = np.sum(p) / np.size(a, 0)
    # print("Cost")
    return J * 100

def predict(x, y, models):
    models = np.transpose(models)
    prediction = np.dot(x, models)
    index = 0
    good = 0
    for p in prediction:
        if (np.argmax(p) == y[index]):
            good += 1
        index += 1
    return (good, index)

def generateModels(x_Learn, y_Learn, classes):
    a = np.array(x_Learn)
    b = np.array(y_Learn)
    s = (classes, np.size(a,1))

    all_Theta = np.zeros(s)
    models = []

    pbar = tqdm(total=classes, desc="Generating Models One vs All", ascii=" ░▒█")

    for i in range(0, classes):
        index = 0
        theta = all_Theta[i]
        result = b.copy()
        for j in b:
            if j == i:
                result[index] = 1
            else:
                result[index] = 0
            index += 1
        res = minimize(cost, theta, args=(result, a), method='nelder-mead')
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
