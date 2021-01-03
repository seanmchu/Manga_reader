# Manga reader in Python 3, using pysimplegui as a GUI framework
# Written by seanmchu on github starting Jan 4 2020

import PySimpleGUI as sg
import cloudscraper as cs
import time, os, sys, re, json, html

#Theme
sg.SetOptions(background_color='#db37d0',
       text_element_background_color='#db37d0',
       element_background_color='#9FB8AD',
       scrollbar_color=None,
       input_elements_background_color='#F7F3EC',
       progress_meter_color = ('green', 'blue'),
       button_color=('white','#ae3de3'))

#Reader GUI
def reader():
    layout = [
        [sg.Text("Manga reader will be here in the future")],
        [sg.Button("OK",size = (30, 4))]
    ]
    window = sg.Window("Readonger",layout,resizable= True) 
    event,values = window.read()
    window.close()
    if(event != sg.WIN_CLOSED):
        main_page()

#Downloader GUI
def download():
    #Downloader layout
    layout = [ 
        [sg.Text('Enter MangaDex Link: ',font = 'Comic 17'), sg.Input(font = 'Comic 13',key = "-MLINK-")],
        [sg.Button('Find available chapters',size = (30, 4)),sg.Button('Return to main page',size = (30,4),key = "MAIN")]
    ]
    window = sg.Window('Dongloader',layout,resizable= True)

    #default loop
    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED):
            return
        if (values["-MLINK-"] == ""):
            print("No manga link ")
        else:
            try:
                string_get = values["-MLINK-"]
                string_split = string_get.split('/')
                is_mdex_link = False
                for s in string_split:
                    if "mangadex" in s:
                        is_mdex_link = True 
                if (is_mdex_link):
                    m_id = string_split[-2]
                    window.close()
                    dl(m_id)
                else:
                    sg.Popup("Invalid link")
            except:
                sg.Popup('Error with link, please make sure you entered a valid mangadex manga link')
        if(event == "MAIN"):
            window.close()
            break
    main_page()

#download            
def dl(m_id):
    scrap = cs.create_scraper()
    print(m_id)
    try:
        scrapped = scrap.get(f"https://mangadex.org/api/manga/{m_id}/")
        print(scrapped)
        m_info = json.loads(scrapped.text)
        print(m_info)
    except (json.decoder.JSONDecodeError, ValueError) as e:
        sg.popup_ok("An error occured!")
        return 
    try:
        title = m_info['manga']['title']
        desc = m_info ['manga']['description']
        layout = [
            [sg.Text(text = title,font = 'comic 18',justification='center')],
            [sg.Multiline(default_text= desc, font = 'comic 13',size = (60,15),justification='center')],
            [sg.Text(text = "Available chapters:", font = 'comic 16',justification='center')],
            [sg.Button("OK","center")]
        ]
        win = sg.Window("Manga info",layout)
        
        event, values = win.read()
    except:
        sg.popup_ok("Error with link, please make sure you entered a mangadex manga link, not a chapter link")

     
#Default page
def main_page():
    layout = [
        [sg.Text("Which application would you like to use?",font = 'Comic 20',border_width = 30)],
        [sg.Button("Downloader",size = (40,10),border_width= 6),sg.Button("Reader",size = (40,10),border_width = 6)]
    ]
    window = sg.Window("DongReader app",layout,resizable= True)
    event,values = window.read() 
    window.close()
    if (event == "Downloader"):
        download()
    elif (event == "Reader"):
        reader()
    

if (__name__ == "__main__"):
    sg
    main_page()
