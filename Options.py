class Options:
    options = 0

    inputJSON = 0
    inputCSV = 0
    inputTXT = 0
    inputXLSX = 0

    # how should output be formatted
    outputJSON = 0
    outputCSV = 0
    outputTXT = 0
    outputXLSX = 0

    # does the user want testing or cross-validation datasets?
    learningProportion = 1
    testingProportion = 0
    degreeProportion = 0

    # interval size is the number of data points in each interval
    intervalSize = 120

    numClasses = 0

    valid = True
    error = ""

    def __init__(self, parsedOptions, l, t, cv, cl):
        valid = True
        error = ""

        self.learningProportion = l
        self.testingProportion = t
        self.crossvalidationProportion = cv
        self.numClasses = cl

        self.options = parsedOptions

        if ('JSON Input' in parsedOptions):
            self.inputJSON = 1
            error = "JSON Input option not implemented"
            valid = False

        if ('CSV Input' in parsedOptions):
            self.inputCSV = 1

        if ('TXT Input (See README)' in parsedOptions):
            self.inputTXT = 1
            error = "TXT Input option not implemented"
            valid = False

        if ('XLSX Input' in parsedOptions):
            self.inputXLSX = 1
            error = "XLSX Input option not implemented"
            valid = False

        if ('Default (~ 2 Seconds)' in parsedOptions):
            self.intervalSize = 120
        elif ('Small (~ 1 Second)' in parsedOptions):
            self.intervalSize = 60
        elif ('Large (~ 5 Seconds)' in parsedOptions):
            self.intervalSize = 300
        else:
            self.intervalSize = 120

        if ('JSON Output' in parsedOptions):
            self.outputJSON = 1
            error = "JSON Output option not implemented"
            valid = False

        if ('CSV Output' in parsedOptions):
            self.outputCSV = 1

        if ('TXT Output (See README)' in parsedOptions):
            self.outputTXT = 1
            error = "TXT Output option not implemented"
            valid = False

        if ('XLSX Output' in parsedOptions):
            self.outputXLSX = 1
            error = "XLSX Output option not implemented"
            valid = False

        self.error = error
        self.valid = valid

    def checkOptions(self):
        valid = True
        error = ""
        #check inputs
        if (self.inputCSV + self.inputTXT + self.inputJSON + self.inputXLSX > 1):
            error = "Choose only one input type."
            valid = False
        if (self.inputCSV + self.inputTXT + self.inputJSON + self.inputXLSX < 1):
            error = "Choose an input type"
            valid = False

        if (self.outputCSV + self.outputTXT + self.outputJSON + self.outputXLSX > 1):
            error = "Choose only one output type."
            valid = False
        if (self.outputCSV + self.outputTXT + self.outputJSON + self.outputXLSX < 1):
            error = "Choose an output type"
            valid = False

        self.error = error
        self.valid = valid
