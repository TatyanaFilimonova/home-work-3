from datetime import datetime
from datetime import date
import time
import math
import re
import json
#from .clean import *
#from .notebook import *
#from .addressbook import *
#from .neural_code import *
#from .user_view import *
from clean import *
from notebook import *
from addressbook import *
from neural_code import *
from user_view import *


import warnings 
warnings.filterwarnings('ignore')



################################################################################
#         CLI BOT section                                                      #
################################################################################

exit_command = ["good bye", "close", "exit"]

def format_phone_number(func):
   def inner(phone):
      result=func(phone)
      if len(result) == 12:
          result='+'+result
      else: result='+38'+result    
      return result
   return inner
         
@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone

def hello_(data):
    return "How can I help You?"

def add_phone(name):
    while True:
        phone = choose_phone()
        if phone == 'exit':
           return 0 
        if phone not in [ph.value for ph in a.data[name].phones]:
            try:
               a.data[name].add_phone(Phone(phone))
               View_message("Phone number succesfully added").output()
               return 1
            except:
               View_message("incorrect phone format. Try again or type 'Exit'", 'red').output()
               continue
        else:
            View_message("This number already belonged to contact "+name+", please try again", 'red').output()

def add_email(name):
    while True:
        View_message("Input email for the contact "+name).output()
        email = Text_input().input()
        if email == 'exit':
            return 0 
        else:
            try:
                a.data[name].add_email(Email(email))
                View_message("Email succesfully added").output()
                return 1
            except:
                View_message("incorrect email format. Try again or type 'Exit'").output()
                continue

def add_address(name):
    address_dict = {}
    View_message("Input address for the contact "+name).output()
    address_dict["country"] = Text_input("Input country: ").input()
    address_dict["zip"] = Text_input("Input ZIP code: ").input()
    address_dict["region"] = Text_input("Input region: ").input()
    address_dict["city"] = Text_input("Input city: ").input()
    address_dict["street"] = Text_input("Input street: ").input()
    address_dict["building"] = Text_input("Input building: ").input()
    address_dict["apartment"] = Text_input("Input apartment: ").input()
    a.data[name].add_address(Address(address_dict))
    View_message("Address succesfully added").output()
            

def add_birthday(name):
    birthday = choose_date()
    if birthday == 'exit':
        View_message("Operation canselled").output()
    else:
        b=Birthday(birthday)
        a.data[name].add_birthday(b)
        View_message("Birthday setted successfully").output()
    return "How can I help you?"

############################# add the record to address book ####################################################
 
def add_contact(data):
    Ok_message = View_message("OK, let's go ahead")   
    while True:
        View_message("Input the name of a contact").output() 
        name = Text_input().input()
        if name not in a.data.keys():
            r = Record(name)
            a.add_record(r)
            break
        else:
            View_message("Contact already exists. Try again").output()
    while True:
        view = View_contact(a.data[name]) 
        Clear_view().refresh()
        view.output()
        View_message("Type 'P' to add phone, 'O' skip to other details").output()
        choose = Text_input().input().lower()
        if choose =='p':
            add_phone(name)
        if choose == 'o':
            Ok_message.output()
            time.sleep(1)
            break
    while True:
        Clear_view().refresh()
        view.output() 
        View_message("Type 'E to enter e-mail, 'O' skip to other details").output()
        choose = Text_input().input().lower()
        if choose =='e':
            add_email(name)
            break
        if choose == 'o':
            Ok_message.output()
            time.sleep(1)
            break
    while True:
        Clear_view().refresh()
        view.output() 
        View_message("Type 'A to enter address,  'O' skip to other details").output()
        choose = Text_input().input().lower()
        if choose =='a':
            add_address(name)
            break
        if choose == 'o':
            Ok_message.output()
            time.sleep(1)
            break
    while True:
        Clear_view().refresh()
        view.output() 
        View_message("Type 'B' to enter birthday,'F' to finish").output()
        choose = Text_input().input().lower()
        if choose =='b':
            add_birthday(name)
            break
        if choose == 'f':
            break
    Clear_view().refresh()  
    View_message("New contact details:").output()
    view = View_contact(a.data[name])
    view.output()
    return "How can I help you?" 


############################# edit the record in address book ####################################################

def edit_contact(data):
    Ok_message = View_message("OK, let's go ahead")
    name = choose_record()
    if name == 'exit':
        View_message("Operation canselled").output()
        return "How can I help you?"

    while True:
        View_message("Type 'N' to edit a name, 'O' skip other details").output()
        choose = Text_input().input().lower()
        if choose =='n':
            View_message("Please let me new name: "+name).output()
            name_new = input()
            a.data[name_new] = a.data[name]
            a.data[name_new].name=Name(name_new)
            a.data.pop(name)
            name = name_new
            View_message("The name succesfully changed").output()
            view = View_contact(a.data[name])
            break 
         
        if choose == 'o':
            view = View_contact(a.data[name])
            View_message("OK, let's go ahead").output()
            time.sleep(1)
            break
    while True:
        Clear_view().refresh()
        view.output()
        View_message("Type 'P' to edit phones, 'O' skip to other details").output()
        choose = Text_input().input().lower()
        if choose =='p':
            View_message("Existing phone numbers for the "+name).output()
            for ph in a.data[name].phones:
                View_phone(ph).output()
            while True:
                View_message("Type 'A' to add  phone, 'E' to edit, 'D' for delete, 'O' skip to other details").output()
                choose_p = Text_input().input().lower()
                if choose_p == 'a':
                     add_phone(name)
                elif choose_p == 'e':
                    while True:
                        View_message("I need the old number to change").output()
                        phone = choose_phone()
                        if phone == 'exit':
                            View_message("Operation canselled", 'red').output()
                            break
                        if phone in [ph.value for ph in a.data[name].phones]:
                            View_message("I need the new number to save").output()
                            phone_new = choose_phone()
                            a.data[name].edit_phone(phone, phone_new)
                            View_message("Phone changed succesfully").output()
                            View_contact(a.data[name]).output()
                        else:
                            View_message("This number doesn't belong to the "+name, 'red').output()
                            continue
                        break
                elif choose_p == 'd':
                    while True:
                        View_message("input the number you would like to delete").output()
                        phone = choose_phone()
                        if phone == 'exit':
                            View_message("Operation canselled", 'red').output()
                            break
                        elif phone in [ph.value for ph in a.data[name].phones]:
                            a.data[name].del_phone(phone)
                            View_message("Phone deleted succesfully").output()
                            View_contact(a.data[name]).output()
                            break
                        else:
                            View_message("Number doesn't belong to the "+name+" Try again", 'red').output()
                elif choose_p == 'o':
                    Ok_message.output()
                    break
                break
        elif choose == "o":
            Ok_message.output()
            break
    while True:
        time.sleep(1)
        Clear_view().refresh()
        view.output()
        View_message("Type 'E to edit e-mail,  'O' skip to other details").output()
        choose = Text_input().input().lower()
        if choose =='e':
            if type(a.data[name].email)!=type(""):
                View_message("Current email for the record "+name+" is:"+a.data[name].email.value).output() 
            add_email(name)
            break
        if choose == 'o':
            Ok_message.output()
            break
    while True:
        time.sleep(1)
        Clear_view().refresh()
        view.output()          
        View_message("Type 'A to edit  address,  'O'  skip to other details").output()
        choose = Text_input().input().lower()
        if choose =='a':
            if type(a.data[name].address)!=type(""):
                View_message("Current saved address for record "+name+" is:").output()
                for key in record["address"].keys():
                   View_message("            "+key+" "*(len("apartment")-len(key))+": "+record["address"][key]).output()

            add_address(name)
            break
        if choose == 'o':
            Ok_message.output()
            break
    while True:
        time.sleep(1)
        Clear_view().refresh()
        view.output()  
        View_message("Type 'B' to edit birthday, 'F' to finish with contact").output()
        choose = Text_input().input().lower()
        if choose =='b':
            if type(a.data[name].address)!=type(""):
                View_message("Current birthday for record "+name+" is: "+a.data[name].birthday.value).output()
            add_birthday(name)
            break
        if choose == 'f':
            break    
    time.sleep(1)
    Clear_view().refresh()
    View_message("Contact details saved").output()
    view.output()  
    return "How can I help you?"

def find_contacts(data):
    res_lst =[]
    View_message("Please input the name, phone or even a part of them").output()
    search_str = input().rstrip()
    search_str = (
        search_str.strip()
            .replace("+","\+")
            .replace("*", "\*")
            .replace("{", "\{")
            .replace("}", "\}")
            .replace("[", "\[")
            .replace("]", "\]")
            .replace("?", "\?")
            .replace("$", "\$")
            .replace("'\'", "\\")
        
    )

    res_lst = a.find(search_str)
    if res_lst == []:
        View_message("Couldn't find records in the phone book").output()
    else:
        View_message("Found next contacts:").output()
        for contact in res_lst:
            view = View_contact(a.data[contact])
            view.output()
    return "How can I help you?"

def show_all(data):
    adress_book = a    
    for page in adress_book:
        for record in page:
            View_contact(a.data[record["Name"]]).output()
            
        input("Press enter to continue")
    return "How can I help you?"

def help_(command):
    Clear_view().refresh()   
    View_help(exec_command).output()  
    return "How can I help you?"


def choose_record():
    View_message("Please enter the name of a contact").output()
    while True:
        name = input()
        if name.lower() in [x.lower() for x in a.data.keys()]:
            for key in   a.data.keys():
                if name.lower() == key.lower():
                    name = key
            break
        elif name.lower() == 'exit':
            break
        else:
            View_message("Couldn`t find this name in adress book.").output()
            View_message("Here are the list of the contacts with similar spelling:").output()
            for c in a.find(name):
                View_message("     "+c).output()
            View_message("Please try to choose the name again or type 'Exit' to come back to main menu").output()    
    return name

def choose_phone():
    View_message("Please enter the phone number").output()
    while True:
        phone = Text_input().input().lower()
        if phone == 'exit':
            break
        is_correct_format= re.search("\+?[\ \d\-\(\)]+$",phone)
        phone= sanitize_phone_number(phone)
        if is_correct_format!=None and len(phone) == 13: 
            break
        else:
            View_message("Phone number is incorrect format, please try again or type 'Exit' to come back to main menu").output()
    return phone

def choose_date():
    View_message("Please enter the date of birthday in format dd.mm.yyyy").output()
    while True:
        birthday = Text_input().input().lower()
        is_correct_format= re.search("\d{2}[\/\.\:]\d{2}[\/\.\:]\d{4}",birthday)
        if is_correct_format!=None:
            birthday = birthday.replace("/",".")
            birthday = birthday.replace(":",".")
            b_array = birthday.split(".")
            try:
                datetime.strptime(birthday, '%d.%m.%Y').date()
            except ValueError:
                View_message("You gave me incorrect date, be carefull nex time").output()
            else:
                break
        elif birthday == 'exit':
            break
        View_message("Date has incorrect format, please try again or type 'Exit' to come back to main menu", 'red').output()
    return birthday

def delete_contact(command):
    choose = ""
    while True:
        name = choose_record()
        while True:
            View_message("Find a contact "+name+", are you sure to delete it? Please type Y/N?").output()
            choose_d = Text_input().input().lower()
            if choose_d == 'y': 
                a.delete(name)
                View_message("Contact "+name+" deleted").output()
                return "How can I help you?"
            elif choose_d == 'n':
                View_message("Operation canselled", 'red').output()
                return "How can I help you?"
            else:
                View_message("Make a correct choise, please").output()
        return  "How can I help you?"         

############################# add the note to note book ####################################################
def add_note(command):
    while True:
        View_message("Input the text of your note here. Use a hashtags # for key_words. Allowed to use copy/paste to speed up" ).output()
        note = Note(Text_input().input())
        if len(note.keyword) ==0:
            View_message("You forgot to add a keywords, please let me them, using # and separate them by spaces").output()
            input_str = Text_input("#Key words: ").input()
            lst = input_str.split(" ")
            for kw in lst:
                note.keyword.append(kw[1:])
        n.add_note(note)        
        break
      
    return "How can I help you?"

############################# edit the note  ####################################################
def edit_note(command):
    while True:
        res_lst=[]
        View_message("Input the keywords for the note you would like to edit (You could input a couple of keywords separated by spaces)" ).output()
        input_str=Text_input().input()
        res_lst=n.find(input_str)
        if res_lst!=[]:
            View_message("I found some notes connected to your request:").output()
            for result in res_lst:
                View_note(result).output()  
            break                   
        elif input_str.lower() == 'exit':
            View_message("Operation canselled", 'red').output()
            return 0
        else:
            View_message("Couldn't find notes with specified keywords, try again or type 'exit'", 'red').output()
            continue       
    while True:
        choose = Text_input("Input ID of note you would like to edit: ").input()
        if  choose in [str(x.id) for x in res_lst]:
            k_lst  = ["# "+k for k in n.data[int(choose)].keyword]
            View_message("Keywords: ").output()
            View_message(k_lst).output()
            View_message("----------------- you could copy here ------------------------").output()
            View_message(n.data[int(choose)].note).output()    
            View_message("------------------ avoid new line character when copy --------").output()
            View_message("You could use copy/paste to speed up. Use # to mark up keywords").output()
            new_text = Text_input().input()
            note_temp = Note(new_text)
            View_message("Please add a keywords for a note, separated by space.").output()
            kw_lst=Text_input("Keywords: ").input().split(" ")
            View_message(kw_lst).output()
            note_temp.keyword.extend(kw_lst)
            n.data[int(choose)] = note_temp
            View_message("Note succesfully changed").output()
            break
        elif choose.lower() == 'exit':
            View_message("Operation cancelled", 'red').output()
            break
        else:
            View_message("Make a correct choice").output()
            continue
        break

           
    return "How can I help you?"

############################# delete the note ####################################################
def delete_note(command):
    while True:
        res_lst=[]
        View_message("Input the keyword for the note you would like to delete" ).output()
        input_str=Text_input("You could input a couple of keywords separated by spaces: ").input()
        res_lst = n.find(input_str)    
        if len(res_lst)!=0:
            View_message("I found some notes connected to your request:").output()
            for result in res_lst:
                View_note(result).output()
            while True:
                choose = Text_input("Input ID of note you would like to delete: ").input()
                if  choose in [str(x.id) for x in res_lst]:
                    n.delete(int(choose))
                    View_message("Note succesfully deleted").output()
                    break
                elif choose.lower() == 'exit':
                    View_message("Operation cancelled", 'red').output()
                    break
                else:
                    View_message("Make a correct choice").output()
                    continue
            break

        elif input_str.lower() == 'exit':
            View_message("Operation cancelled",'red').output()
            break
        
        else:
            View_message("Couldn't find notes with specified keywords, try again or type 'exit'", 'red').output()
            continue
    return "How can I help you?"


def find_notes(command):
    while True:
        res_lst=[]
        View_message("Input the keyword for the note you would like to find" ).output()
        input_str=Text_input("Allowed input of multiply keywords separated by spaces: ").input()
        res_lst=n.find(input_str)   
        if len(res_lst)!=0:
            View_message("I found some notes connected to your request:").output()
            for result in res_lst:
                View_note(result).output()
            break
        elif input_str.lower() == 'exit':
            View_message("Operation cancelled", 'red').output()
            break
        else:
            View_message("Couldn't find notes with specified keywords, try again or type 'exit'", 'red').output()
            continue
    return "How can I help you?"



############################# show all the notes ####################################################
def show_notes(command):
    for page in n:
        for record in page:
            View_note(record).output()
        input("Press enter to continue")
    return "How can I help you?"


############################# sorting the notes by keywords list ####################################################
def sort_notes(command):
    sort_notebook = Notebook("temp")
    sort_notebook.data = dict(sorted(n.data.items(), key=lambda item: sorted(item[1].keyword, key = lambda x: x.upper())))
    n.data = sort_notebook.data
    for item in n.data.keys():
        n.data[item].keyword =  sorted(n.data[item].keyword, key = lambda x: x.upper())   
        View_note(n.data[item]).output()
    View_message("Sorting completed").output()
    return "How can I help you?"


############           add code of sorting function here ######################################################
def sort_folder(command):
    while True: 
        View_message("Type path to the folder, use '/' to folders").output()
        path = Path(Text_input().input())
        if path.exists(): 
            parse_folder(path)
            break 
        else:
            View_message("Path doesn`t exist", 'red').output()    
    View_message("Sorting completed").output()
    return "How can I help you?"


################################################################################################################

def next_birthday(command):
    res_lst = []
    while True:    
        period = Int_input("How many days in the period we are looking for: ").input()
        if period >365 or period <=0:
           View_message("Incorrect, should be integer between 0 and 365 days", 'red').output()
           continue
        else:
           max_len = 0 
           for name in a.data.keys():
              if int(a.data[name].days_to_birthday())<period:
                 res_lst.append(a.data[name])
                 if len(name) > max_len:
                    max_len = len(name)
            
           if len(res_lst)>0:
              View_message("List of contacts that have birthday in "+ str(period)+" days:", 'green').output()
              for res in res_lst:
                 View_message("      "+res.name.value+": "+" "*(max_len - len(res.name.value))+str(res.birthday.value), "green").output()
              break 
           else:
              View_message("I'm sorry, couldn't find any", 'red').output()
              break
    return "How can I help you?"



def save_(data):
    #a.dump("assistant/Work telephones.json")
    #n.dump("assistant/Work notes.json")
    a.dump("data/Work telephones.json")
    n.dump("data/Work notes.json")
    View_message("All data saved").output()
    return "How can I help you?"
    
exec_command = { 
    "hello": [hello_,                  "hello:              Greetings", 0], 
    "add contact":  [add_contact,      "add contact:        Add a new contact", 2], # adopted to the project needs
    "edit contact": [edit_contact,     "edit contact:       Edit the contact detail", 2], # adopted to the project needs
    "find contact": [find_contacts,    "find contact:       Find the records by phone or name", 1], # adopted to the project needs
    "find notes":   [find_notes,       "find notes:         Find the notes by text or keywords", 1], # adopted to the project needs
    "show all contacts": [show_all,    "show all contacts:  Print all the records of adress book, page by page", 0], # adopted to the project needs
    "show all notes":    [show_notes,  "show all notes:     Print all the records of adress book, page by page", 0], # adopted to the project needs
    "help": [help_,                    "help:               Print a list of the available commands",0],  # adopted to the project needs,
    "add note": [add_note,             "add note:           Add new text note ", 0],# adopted to the project needs
    "edit note": [edit_note,           "edit note:          Edit existing text note ", 0],# adopted to the project needs
    "delete contact": [delete_contact, "delete contact:     Delete contact", 2], # adopted to the project needs,
    "delete note": [delete_note,       "delete note:        Delete text note", 2], # adopted to the project needs,
    "sort notes": [sort_notes,         "sort note:          Sort of the notes by keywords", 2], # adopted to the project needs
    "sort folder": [sort_folder,       "sort folder:        Sort selected folder by file types", 2], # adopted to the project needs
    "next birthday": [next_birthday,   "next birthday:      Let you the contats with birthdays in specified period", 2], # adopted to the project needs
    "save": [save_,                    "save:               Save the current state of data to disk", 0]  # adopted to the project needs,
                           
             }


def handler(command):
    if command == 'exit':
        return 'exit'
    else:
        return exec_command[command][0]("")
          
def listener():
    command = ""
    communication_str = "Hi! Looking for your order!"
    while ( communication_str) not in exit_command:
        View_message(communication_str).output()
        message = Text_input().input().lower()
        Clear_view().refresh()  
        ints = predict_class(message)
        res = get_response(ints, intents)
        View_message(res[0][0]).output()
        communication_str = handler(res[1])

a = AddressBook("Work telephones")
n=Notebook("Work notes")

def start_bot():
   Clear_view().refresh()
   try:
      #a.load("assistant/Work telephones.json")
      a.load("data/Work telephones.json")
   except:
      View_message("Couldn't find file, starting with empty adress book", 'red').output()
   try:
      #n.load("assistant/Work notes.json")
      n.load("data/Work notes.json")
   except:
      View_message("Couldn't load file, starting with empty note book", 'red').output()
   listener() 
   try:
      #a.dump("assistant/Work telephones.json")
      #n.dump("assistant/Work notes.json")
      a.dump("data/Work telephones.json")
      n.dump("data/Work notes.json")
   except:
      View_message("Couldn't save file, all the changes could be loose").output()
start_bot()
