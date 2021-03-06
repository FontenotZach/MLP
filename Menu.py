from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import json


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Selected: '#6030b7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'checkbox',
        'message': 'Select Options',
        'name': 'Feature Generation Options',
        'choices': [
            Separator('= File Type ='),
            {
                'name': 'CSV Input'
            },
            {
                'name': 'JSON Input'
            },
            {
                'name': 'TXT Input (See README)'
            },
            {
                'name': 'XLSX Input'
            },
            Separator('= Interval Size ='),
            {
                'name': 'Small (~ 1 Second)'
            },
            {
                'name': 'Default (~ 2 Seconds)'
            },
            {
                'name': 'Large (~ 5 Seconds)'
            },
            Separator('= Output Format ='),
            {
                'name': 'CSV Output'
            },
            {
                'name': 'JSON Output'
            },
            {
                'name': 'TXT Output (See README)'
            },
            {
                'name': 'XLSX Output'
            }
        ],
        'validate': lambda answer: 'You must choose at least one option.'
            if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'learning',
        'message': 'What proportion of the data should be reserved for training? (0-1)',
    },
    {
        'type': 'input',
        'name': 'testing',
        'message': 'What proportion of the data should be reserved for testing? (0-1)',
    },
    {
        'type': 'input',
        'name': 'cross-validation',
        'message': 'What proportion of the data should be reserved for cross-validation? (0-1)',
    },
    {
        'type': 'input',
        'name': 'classes',
        'message': 'How many data classifications are there?',
    }

]

#def getOptions(self):
answers = prompt(questions, style=style)

with open('options.json', 'w') as jsonFile:
    json.dump(answers, jsonFile)
