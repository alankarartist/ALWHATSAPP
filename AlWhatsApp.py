import pyttsx3
import speech_recognition as sr 
from word2number import w2n
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
try:
    import autoit
except ModuleNotFoundError:
    pass
import time
import os
from tkinter import*
from tkinter import font
import argparse

parser = argparse.ArgumentParser(description='PyWhatsapp Guide')
parser.add_argument('--chrome_driver_path', action='store', type=str, default='./chromedriver.exe', help='chromedriver executable path (MAC and Windows path would be different)')
parser.add_argument('--message', action='store', type=str, default='', help='Enter the msg you want to send')
parser.add_argument('--remove_cache', action='store', type=str, default='False', help='Remove Cache | Scan QR again or Not')
args = parser.parse_args()

if args.remove_cache == 'True':
    os.system('rm -rf User_Data/*')
browser = None
Contacts = None
message = None if args.message == '' else args.message
Link = "https://web.whatsapp.com/"
wait = None
docfilename = None
imagename = None
unsavedContacts = None

def whatsapp_login(chrome_path):
    global wait, browser, Link
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()

class AlWhatsApp:
    def __init__(self):
        root = Tk(className=" AlWhatsApp ")
        root.geometry("400x600+1510+415")
        root.config(bg="#58e764")
        color = '#58e764'

        def speak(audio):
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.say(audio)
            engine.runAndWait()
            
        def inputContacts():
            global Contacts, unsavedContacts
            Contacts = []
            unsavedContacts = []
            name = receiver.get()
            if ',' not in name:
                if re.search('^(\d){11,12}$',name):
                    unsavedContacts.append(name)
                elif re.search('^[A-Za-z]+([\ A-Za-z]+)*',name):    
                    name = '"' + name + '"'
                    Contacts.append(name)
                elif re.search('^(\d){10}$',name):
                    name = '"' + name + '"'
                    Contacts.append(name)
            elif ',' in name:
                name = name.split(',')
                for i in name:
                    if re.search('^(\d){11,12}$',i):
                        unsavedContacts.append(i)
                    elif re.search('^[A-Za-z]+([\ A-Za-z]+)*',i):    
                        i = '"' + i + '"'
                        Contacts.append(i)
                    elif re.search('^(\d){10}$',i):
                        i = '"' + i + '"'
                        Contacts.append(i)
            if len(Contacts) != 0:
                print("Here is the list of saved contacts: ", Contacts)
            if len(unsavedContacts) != 0:
                print("Here is the list of unsaved contacts: ", unsavedContacts)

        def inputMessage():
            global message
            message = []
            temp = ""
            done = False
            while not done:
                temp = body.get('1.0', 'end-1c')   
                temp = temp + '~'
                if len(temp) != 0 and temp[-1] == "~":
                    done = True
                    message.append(temp[:-1])
                else:
                    message.append(temp)
            message = "\n".join(message)

        def sendMessage(target):
            global message, wait, browser
            try:
                x_arg = '//span[contains(@title,' + target + ')]'
                ct = 0
                while ct != 10:
                    try:
                        group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                        group_title.click()
                        break
                    except:
                        ct += 1
                        time.sleep(3)
                input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                for i in message:
                    if i == "\n":
                        ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
                    else:
                        input_box.send_keys(i)
                input_box.send_keys(Keys.ENTER)
                speak("Message sent successfuly")
                return "Message sent successfuly"
                time.sleep(1)
            except NoSuchElementException:
                speak("Failed to send message")       
                return None

        def sendUnsavedContactMessage():
            global message
            try:
                time.sleep(7)
                input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                for i in message:
                    if i == "\n":
                        ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
                    else:
                        input_box.send_keys(i)
                input_box.send_keys(Keys.ENTER)
                speak("Message sent successfuly") 
                return "Message sent successfuly"      
            except NoSuchElementException:
                speak("Failed to send message")       
                return None

        def sendAttachment():
            global imagename
            if imagename:
                if ',' not in imagename:
                    # Attachment Drop Down Menu
                    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
                    clipButton.click()
                    time.sleep(1)

                    # To send Videos and Images.
                    mediaButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
                    mediaButton.click()
                    time.sleep(3)
                    imagePath = os.getcwd() + "\\AlWhatsApp\\Documents\\" + imagename
                    autoit.control_focus("Open", "Edit1")
                    autoit.control_set_text("Open", "Edit1", (imagePath))
                    autoit.control_click("Open", "Button1")
                    time.sleep(3)
                    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
                    whatsapp_send_button.click()
                if ',' in imagename:
                    imagename = imagename.split(',')
                    for i in imagename:
                        # Attachment Drop Down Menu
                        clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
                        clipButton.click()
                        time.sleep(1)

                        # To send Videos and Images.
                        mediaButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
                        mediaButton.click()
                        time.sleep(3)
                        imagePath = os.getcwd() + "\\AlWhatsApp\\Documents\\" + i
                        autoit.control_focus("Open", "Edit1")
                        autoit.control_set_text("Open", "Edit1", (imagePath))
                        autoit.control_click("Open", "Button1")
                        time.sleep(3)
                        whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
                        whatsapp_send_button.click()
            
        def sendFiles():
            global docfilename
            if docfilename:
                if ',' not in docfilename:
                    # Attachment Drop Down Menu
                    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
                    clipButton.click()
                    time.sleep(1)

                    # To send Videos and Images.
                    mediaButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
                    mediaButton.click()
                    time.sleep(3)
                    docPath = os.getcwd() + "\\AlWhatsApp\\Documents\\" + docfilename
                    autoit.control_focus("Open", "Edit1")
                    autoit.control_set_text("Open", "Edit1", (docPath))
                    autoit.control_click("Open", "Button1")
                    time.sleep(3)
                    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
                    whatsapp_send_button.click()
                if ',' in docfilename:
                    docfilename = docfilename.split(',')
                    for d in docfilename:
                        # Attachment Drop Down Menu
                        clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
                        clipButton.click()
                        time.sleep(1)

                        # To send Videos and Images.
                        mediaButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
                        mediaButton.click()
                        time.sleep(3)
                        docPath = os.getcwd() + "\\AlWhatsApp\\Documents\\" + d
                        autoit.control_focus("Open", "Edit1")
                        autoit.control_set_text("Open", "Edit1", (docPath))
                        autoit.control_click("Open", "Button1")
                        time.sleep(3)
                        whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
                        whatsapp_send_button.click()

        def sender():
            global Contacts, imagename, docfilename, unsavedContacts
            for i in Contacts:
                if sendMessage(i) == "Message sent successfuly":
                    text.insert(1.0, "Message sent to "+i+". ")
                    speak("Message sent to "+i)
                if imagename:
                    try:
                        sendAttachment()  
                        speak('Attachments sent')
                    except:
                        speak("Can't send attachments")
                if docfilename:
                    try:
                        sendFiles()
                        speak('Files sent')
                    except:
                        speak("Can't send files")
            time.sleep(5)
            if len(unsavedContacts) > 0:
                for i in unsavedContacts:
                    link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(i)
                    #driver  = webdriver.Chrome()
                    browser.get(link)
                    if sendUnsavedContactMessage() == "Message sent successfuly":
                        text.insert(1.0, "Message sent to "+i+". ")
                        speak("Sending message to"+ i)
                    if imagename:
                        try:
                            sendAttachment() 
                            speak('Files sent')
                        except:
                            speak("Can't send files")
                    if docfilename:
                        try:
                            sendFiles()
                            speak('Attachments sent')
                        except:
                            speak("Can't send attachments")
                    time.sleep(5)

        def main():
            global docfilename, imagename, browser, message
            try:
                inputContacts()
                inputMessage()
                imagename = imgvid.get()
                docfilename = doc.get()
                sender()
                speak("Task Completed")
                message = None
            except:
                speak("Didn't understand that")
        
        appHighlightFont = font.Font(family='sans-serif', size=12, weight='bold')

        receiver = Label(root, text="Contact")
        receiver.pack( )
        receiver.config(bg=color,fg="white",font=appHighlightFont)
        receiver = Entry(root, highlightbackground=color, highlightcolor=color, highlightthickness=3, bd=0, font=appHighlightFont)
        receiver.pack(fill=X)

        body = Text(root, font="sans-serif",  relief=SUNKEN , highlightbackground='#1ca48c', highlightcolor='#1ca48c', highlightthickness=5, bd=0)
        body.config(bg="#247464", fg='white', height=15, font=appHighlightFont)
        body.pack(fill=BOTH, expand=True)

        imgvid= Label(root, text="Image and Video Attachment")
        imgvid.pack( )
        imgvid.config(bg=color,fg="white",font=appHighlightFont)
        imgvid = Entry(root, highlightbackground=color, highlightcolor=color, highlightthickness=3, bd=0, font=appHighlightFont)
        imgvid.pack(fill=X)

        doc= Label(root, text="Document Attachment")
        doc.pack( )
        doc.config(bg=color,fg="white",font=appHighlightFont)
        doc = Entry(root, highlightbackground=color, highlightcolor=color, highlightthickness=3, bd=0, font=appHighlightFont)
        doc.pack(fill=X)

        whatsapp = Button(root, text="WhatsApp",  command=main)
        whatsapp.config(bg=color,fg="white",font=appHighlightFont)
        whatsapp.pack(fill=X)

        text = Text(root, font="sans-serif",  relief=SUNKEN , highlightbackground='#1ca48c', highlightcolor='#1ca48c', highlightthickness=5, bd=0)
        text.config(bg="#247464", fg='white', height=2, font=appHighlightFont)
        text.pack(fill=BOTH, expand=True)

        root.mainloop()
        browser.close()

if __name__ == "__main__":
    whatsapp_login(args.chrome_driver_path)
    alw = AlWhatsApp()