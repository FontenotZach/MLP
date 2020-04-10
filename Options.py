class Options:
    options = 0

    input_JSON = 0
    input_CSV = 0
    input_TXT = 0
    input_XLSX = 0

    # how should output be formatted
    output_JSON = 0
    output_CSV = 0
    output_TXT = 0
    output_XLSX = 0

    # does the user want testing or cross-validation datasets?
    learning_Proportion = 1
    testing_Proportion = 0
    degree_Proportion = 0

    # interval size is the number of data points in each interval
    interval_Size = 120

    numClasses = 0

    valid = True
    error = ""

    def __init__(self, parsedOptions, l, t, cv, cl):
        valid = True
        error = ""

        self.learning_Proportion = l
        self.testing_Proportion = t
        self.cross_validation_Proportion = cv
        self.numClasses = cl

        self.options = parsedOptions

        if ('JSON Input' in parsedOptions):
            self.input_JSON = 1
            error = "JSON Input option not implemented"
            valid = False

        if ('CSV Input' in parsedOptions):
            self.input_CSV = 1

        if ('TXT Input (See README)' in parsedOptions):
            self.input_TXT = 1
            error = "TXT Input option not implemented"
            valid = False

        if ('XLSX Input' in parsedOptions):
            self.input_XLSX = 1
            error = "XLSX Input option not implemented"
            valid = False

        if ('Default (~ 2 Seconds)' in parsedOptions):
            self.interval_Size = 120
        elif ('Small (~ 1 Second)' in parsedOptions):
            self.interval_Size = 60
        elif ('Large (~ 5 Seconds)' in parsedOptions):
            self.interval_Size = 300
        else:
            self.interval_Size = 120

        if ('JSON Output' in parsedOptions):
            self.output_JSON = 1
            error = "JSON Output option not implemented"
            valid = False

        if ('CSV Output' in parsedOptions):
            self.output_CSV = 1

        if ('TXT Output (See README)' in parsedOptions):
            self.output_TXT = 1
            error = "TXT Output option not implemented"
            valid = False

        if ('XLSX Output' in parsedOptions):
            self.output_XLSX = 1
            error = "XLSX Output option not implemented"
            valid = False

        self.error = error
        self.valid = valid

    def checkOptions(self):
        valid = True
        error = ""
        #check inputs
        if (self.input_CSV + self.input_TXT + self.input_JSON + self.input_XLSX > 1):
            error = "Choose only one input type."
            valid = False
        if (self.input_CSV + self.input_TXT + self.input_JSON + self.input_XLSX < 1):
            error = "Choose an input type"
            valid = False

        if (self.output_CSV + self.output_TXT + self.output_JSON + self.output_XLSX > 1):
            error = "Choose only one output type."
            valid = False
        if (self.output_CSV + self.output_TXT + self.output_JSON + self.output_XLSX < 1):
            error = "Choose an output type"
            valid = False

        self.error = error
        self.valid = valid
