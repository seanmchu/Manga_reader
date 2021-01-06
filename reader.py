# Manga reader in Python 3, using pysimplegui as a GUI framework
# Written by seanmchu on github starting Jan 4 2020
import cloudscraper as cs 
import PySimpleGUI as sg
import time, os, sys, re, json, html
#Theme
sg.SetOptions(background_color='#db37d0',
       text_element_background_color='#db37d0',
       element_background_color='#9FB8AD',
       scrollbar_color=None,
       input_elements_background_color='#F7F3EC',
       progress_meter_color = ('green', 'blue'),
       button_color=('white','#ae3de3'))

def to_float(x):
    if (x == ""):
        x = 0
    else:
        x = float(x)
    return x

#Reader GUI
def reader():
    layout = [
        [sg.Text("Manga reader will be here in the future")],
        [sg.Button("OK",size = (30, 4))]
    ]
    window = sg.Window("Readonger",layout,resizable= True) 
    event,values = window.read()
    if(event != sg.WIN_CLOSED):
        main_page()
    window.close()
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
        m_info = json.loads(scrapped.text)
    except (json.decoder.JSONDecodeError, ValueError) as e:
        sg.popup_ok("An error occured!")
        return 
    try:
        title = m_info['manga']['title']
        desc = m_info ['manga']['description']
        #Now, we get all chapters in our required language and sort
        cinfo = {}
        chap = []
        chap_data = []
        for c in m_info["chapter"]:
            if (m_info["chapter"][str(c)]["lang_code"] == "gb"):
                cinfo["chap_no"] = m_info["chapter"][str(c)]["chapter"]
                cinfo["chap_id"] = c
                chap.append(m_info["chapter"][str(c)]["chapter"])
                chap_data.append(cinfo)
                cinfo = {}
        chap = list(set(chap))
        chap.sort(key = to_float)
        for c in chap:
            if (c == ""):
                c = "Oneshot"
        if (not chap):
            sg.popup_ok("No Chapters available!")
        guiplace = []
        temp = [] 
        counter = 0
        for c in chap:
            temp.append(sg.Checkbox(str(c),default = True,key = c))
            counter += 1
            if (not counter % 15):
                guiplace.append(temp)
                temp = []
        guiplace.append(temp)
        #turned off resizeable because elements don't resize themselves unlike CSS in PSG
        layout = [
            [sg.Text(text = title,font = 'comic 18',justification='center')],
            #use multiline until I can get text wrapping to work properly
            [sg.Multiline(default_text= desc, font = 'comic 13',size = (60,15),justification='center', key = "desc")],
            [sg.Text(text = "Available chapters:", font = 'comic 16',justification='center')],
            [sg.Button("Download"),sg.Button("Cancel"),sg.Button("Check/Uncheck all", key = "-CHECK-")]
        ]
        for listt in guiplace:
            layout.append(listt)
        win = sg.Window("Manga info",layout)
        dl = False
        dl_chapters = []
        dl_cinfo = []
        while 1:
            event, values = win.read()
            if (event == "Download"):
                dl = True
                for v in values:
                    if (v != "desc" and values[v]):
                        dl_chapters.append(int(v))
                for a in dl_chapters:
                    for c in chap_data:
                        if (c['chap_no'] == str(a)):
                            dl_cinfo.append(c)
                dl_cinfo.sort(key = lambda x : to_float(x['chap_no']))
                sg.PopupOK('downloading chapters, please wait')
                actually_download(dl_cinfo,title,scrap)
                sg.PopupOK("done!")
                break
            if (event == "Cancel" or event == sg.WIN_CLOSED):
                break 
            if (event == "-CHECK-"):
                for c in chap:
                    if (values[c]):
                        win[c].update(False)
                    else:
                        win[c].update(True)
    except:
        sg.popup("an error occured :(")
def actually_download(dl,title,scrap):
    for c in dl:
        #Use while loop to catch mangadex throttling 
        while 1:
            try:
                cinfo = scrap.get(f"https://mangadex.org/api/chapter/{c['chap_id']}")
                chap = json.loads(cinfo.text)
                #get all image links
                if (chap['status'] == 'deleted'):
                    continue
                server = chap["server"]
                img_list = []
                #Fix formatting issues
                if ('mangadex' not in server):
                    server = f'https://mangadex.org{server}'  
                hashh = chap['hash']
                #append images to list 
                for p in chap['page_array']:
                    img_list.append(f'{server}{hashh}/{p}') 
                elist = enumerate(img_list,1)
                for pnum,link in elist:
                    fn = os.path.basename(link)
                    extension = os.path.splitext(fn)[1]
                    #files cannot have certain characters
                    title = re.sub('[<>:"//\\|?*]','_',title)
                    dfold = os.path.join(os.getcwd(),"downloads",title,f"chapter {c['chap_no']}")
                    if not os.path.exists(dfold):
                        #use mkdirs in case 'downloads' or 'title' doesn't exist
                        os.makedirs(dfold)
                    page_fn = f'{pnum} {extension}'
                    out = os.path.join(dfold,page_fn)
                    data = scrap.get(link)
                    if (data.status_code == 200):
                        with open(out,'wb') as f:
                            f.write(data.content)
                    else:
                        sg.popup_ok(f"Error no {f.status_code} while downloading chapter {c['chap_no']} page {pnum}")

            except json.JSONDecodeError:
                continue 
            break
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
