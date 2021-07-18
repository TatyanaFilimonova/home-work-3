from abc import ABC, abstractmethod
from termcolor import colored
import os

class Clear_view():
    def __init__(self):
        self.system_type = os.name

    def refresh(self):
        if self.system_type == 'nt':
            os.system('cls')
        if self.system_type == 'posix':
            os.system('clear')

class message(ABC):
    def __init__(self, message):
        self.text = message
        

class View(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def output(self):
        pass

class View_contact(View):
    def output(self):
        print(colored(self.data, 'green'))

class View_note(View):
    def output(self):
        print(colored(self.data, 'blue'))

class View_help(View):
    def output(self):
        for key in self.data.keys():
            print (self.data[key][1])

class View_message(View):
    def __init__(self, data,color='white'):
        self.data = data
        self.color = color
    def output(self):
        print(colored(self.data, self.color))

class View_phone(View):
    def output(self):
        print("      "+self.data.value)        

       
class User_input(ABC):
    def __init__(self, message):
        self.message = message

    @abstractmethod
    def input(self):
        pass        

class Text_input(User_input):
    def __init__(self, message=''):
        self.message = message

    def input(self):
        return input(self.message)

class Int_input(User_input):
    def __init__(self, message=''):
        self.message = message

    def input(self):
        while True:
            try:
                res = int(input(self.message))
                break
            except:
                print(colored("Incorrect input, should be numeric",'red'))
        return res
