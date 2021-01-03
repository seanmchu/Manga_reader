# img_viewer.py


import PySimpleGUI as sg

import os.path

sg.SetOptions(background_color='#9FB8AD',
       text_element_background_color='#9FB8AD',
       element_background_color='#9FB8AD',
       scrollbar_color=None,
       input_elements_background_color='#F7F3EC',
       progress_meter_color = ('green', 'blue'),
       button_color=('white','#475841'))

def reader():
    layout = [
        [sg.Text("Manga reader will be here in the future")],
        [sg.Button("ok")]
    ]
    window = sg.Window("Manga reader",layout) 
    event,values = window.read()
    window.close()
    main_page()

def download():
    layout = [ 
        [sg.Text('Enter MangaDex Link: ',font = 'Garamond 15'), sg.Input()],
        [sg.Button('Find available chapters')]
    ]
    window = sg.Window('Manga Downloader',layout)
    event, values = window.read()
    window.close()
    main_page()


def main_page():
    layout = [
        [sg.Text("Which application would you like to use?",font = 'Times 20')],
        [sg.Button("Download",size = (40,10)),sg.Button("Reader",size = (40,10))]
    ]
    window = sg.Window("DongReader app",layout)
    event,values = window.read() 
    window.close()
    if (event == "Download"):
        download()
    elif (event == "Reader"):
        reader()
    

if (__name__ == "__main__"):
    main_page()
