# '''
#   A minimalist Notepad built with the PySimpleGUI TKinter framework
#   Author:     Israel Dryer
#   Email:      israel.dryer@gmail.com
#   Modified:   2019-10-13
#------------------------- to do list------------------
# done make the window smaller (right now it fills the screen)
# add function for word search
# add function to select all
# add function for count of words
# get popup in center of screen
# export results of individual word count into file save as
# to fix
#  popups are not closing
# '''
from collections import Counter

import PySimpleGUI as sg 

sg.ChangeLookAndFeel('BrownBlue') # change style

WIN_W: int = 20
WIN_H: int = 15
filename:str = None

# string variables to shorten loop and menu code
file_new: str = 'New............(CTRL+N)'
file_open: str = 'Open..........(CTRL+O)' # 
file_save: str = 'Save............(CTRL+S)'

menu_layout: list = [['&File', [file_new, file_open, file_save, '&Save As', '---', 'Exit']],
                     ['&Tools', ['help text','Word Count', 'Count Individual Words']],
                     ['&Help', ['About']]]

layout: list = [[sg.Menu(menu_layout)],
                [sg.Text('> New file <', font=('Consolas', 10), size=(WIN_W, 1), key='_INFO_')],
                [sg.Multiline(font=('Consolas', 12), size=(WIN_W, WIN_H), key='_BODY_'),sg.Output(key="-OUTPUT-")]]

# I set the location to open in top left corner


window: object = sg.Window('Notepad', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True, location=(2100,100))
window.read(timeout=1)

#if you maximize you can't see any of the button options/ close/ minimize etc
#window.maximize()
window['_BODY_'].expand(expand_x=True, expand_y=True)

def new_file() -> str:
    ''' Reset body and info bar, and clear filename variable '''
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New File <')
    filename = None
    return filename

def open_file() -> str:
    ''' Open file and update the infobar '''
    try:
        filename: str = sg.popup_get_file('Open File', no_window=True)
    except:
        return
    if filename not in (None, '') and not isinstance(filename, tuple):
        with open(filename, 'r') as f:
            window['_BODY_'].update(value=f.read())
        window['_INFO_'].update(value=filename)
    return filename

def save_file(filename: str):
    ''' Save file instantly if already open; otherwise use `save-as` popup '''
    if filename not in (None, ''):
        with open(filename,'w') as f:
            f.write(values.get('_BODY_'))
        window['_INFO_'].update(value=filename)
    else:
        save_file_as()

def save_file_as() -> str:
    ''' Save new file or save existing file with another name '''
    try:
        filename: str = sg.popup_get_file('Save File', save_as=True, no_window=True)
    except:
        return
    if filename not in (None, '') and not isinstance(filename, tuple):
        with open(filename,'w') as f:
            f.write(values.get('_BODY_'))
        window['_INFO_'].update(value=filename)
    return filename

def help_text():
    '''testing help in edit window'''
    about_text = '''
    A minimalist Notepad 
    built with 
    PySimpleGUI TKinter 
    original coder:    
    Israel Dryer    
    Email:      israel.dryer@gmail.com   
    Modified:   2020-dec-14 
    by DGD dennisgdaniels@gmail.com
    
    TODO: generate json arrays from a word list

    '''
    print(about_text)


def word_count():
    ''' Display estimated word count '''
    words: list = [w for w in values['_BODY_'].split(' ') if w!='\n']
    word_count: int = len(words)
    sg.PopupQuick('Word Count: {:,d}'.format(word_count), auto_close=False, location=(2100,100))

def count_ind_words():
    ''' Display count  of individual words'''
    #words1: list = [w.strip().lower() for w in values['_BODY_'].split(' ') if w!='\n']
    text = values['_BODY_']
    ####print("text first:", text)
    evil_punc = [
        ",",
        ".",
        "\n",
        ";",
        ":",
        "'",
        '"',
        "`",
        "-",
        "_",
        "!",
        "?",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
    ]
    # make a clean version of the text
    for evil_char in evil_punc:
        text = text.replace(evil_char, " ")
    ####print("text after:", text)
    # make a list of space-seperated words from the text
    wordlist = text.split(" ")
    # strip each word from leading/trailing whitespace and lowercase it
    #list comprehension
    #inline for loop
    wordlist = [word.strip().lower() for word in wordlist if len(word) >0]
    # use collections Counter because it makes everything we want
    # the text below will show up in the output
    output = "==individual word count==\n"
    # create counter object (like a dict) from wordlist
    # get longest word
    maxlen = max([len(word) for word in wordlist])
    # sorting tool
    # https://stackoverflow.com/a/613230/1338127
    for word, how_often in sorted([(value,key) for (key,value) in Counter(wordlist).items()],reverse=True):  
        output += "{}: {}\n".format(word, how_often)
    print(output)
    

    
    #I want to write the output into a editable window
    # and then be able to save it.
    # I have tried wuing Multiline.print() but no joy
    
    

def about_me():
    #TODO: get a popup that will allow users to copy text from popup 
    sg.PopupQuick('''A minimalist Notepad 
    built with 
    PySimpleGUI TKinter 
    original coder:    
    Israel Dryer    Email:      israel.dryer@gmail.com   
    Modified:   2020-dec-14 by DGD'''

    , auto_close=False, location=(2100,300))

while True:

    event, values = window.read()

    if event in (None, 'Exit'):
        break
    if event in (file_new, 'n:78'):
        filename = new_file()
    if event in (file_open, 'o:79'):
        filename = open_file()
    if event in (file_save, 's:83'):
        save_file(filename)
    if event in ('Save As',):
        filename = save_file_as()   
    if event in ('Word Count',):
        word_count() 
    if event in ('help text',):
        help_text() 

    if event in ('Count Individual Words',):

        count_ind_words() 
    if event in ('About',):
        about_me()
