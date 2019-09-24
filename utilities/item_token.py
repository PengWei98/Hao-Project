# Created by yuwenhao at 15/01/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""


class Token:
    def __init__(self, filename=str, label=str, position=str, indicator=str, content=list):
        self.filename = filename
        self.label = label
        self.position = position
        self.indicator = indicator
        self.content = content

    def __str__(self):
        return 'filename ={}, label = {}, position = {}, indicator = {}, content = {}'.format(
             self.filename, self.label, self.position, self.indicator, self.content
        )


