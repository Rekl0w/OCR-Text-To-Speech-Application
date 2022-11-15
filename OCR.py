from tkinter.messagebox import showinfo
from click import style
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import *
from os.path import exists as file_exists
import sv_ttk
import pyscreenshot
import requests

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\Tesseract.exe'

options = {"English":"en","Turkish":"tr","German":"de","French":"fr","Italian":"it","Spanish ":"es","Russian":"ru","Portuguese(Brazil)":"br","Danish":"da","Dutch":"nl","Polish":"pl","Ukrainian":"uk","Afrikaans":"af","Arabic":"ar","Bengali":"bn","Bulgarian":"bg","Catalan":"ca","Chinese":"yue","Czech":"cs","Filipino":"fil","Finnish":"fi","Greek":"el","Gujarati":"gu","Hindi":"hi","Hungarian":"hu","Icelandic":"is","Indonesian":"id","Japanese":"ja","Kannada":"kn","Korean":"ko","Latvian":"lv","Malay":"ms","Malayalam":"ml","Mandarin Chinese":"cmn","Norwegian":"nb","Portuguese(Portugal)":"pt","Punjabi":"pa","Romanian":"ro","Serbian":"sr","Slovak":"sk","Swedish":"sv","Tamil":"ta","Telugu":"te","Thai":"th","Vietnamese":"vi"} 

root= tk.Tk()
root.geometry("720x350")
root.title("OCR & Text To Speech - © 2022 Batuhan Tomo")
root.resizable(False, False)
sv_ttk.set_theme("dark")

root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

canvas = tk.Canvas(root, width = 500, height = 400)
canvas.pack()

is_on = True
def switch():
    global is_on
    
    if is_on:
        sv_ttk.set_theme("light")
        is_on = False
    else:
        sv_ttk.set_theme("dark")
        is_on = True
    

def show():
    global lang
    lang = entry2.get()
    return lang

material = tk.StringVar()

combo = ttk.Combobox(root, state = "readonly", values= list(options.keys()), textvariable=material)
combo.current()

combo.bind("<<ComboboxSelected>>", lambda event:[show(),entry2.delete(0,"end"),(entry2.insert(0,options[material.get()]))])
canvas.create_window(250, 245, window=combo)

label = tk.Label(text="Lütfen Seslendirilmesini İstediğiniz Dosyanın Bilgisayarınızdaki Yolunu Giriniz. \n Elle Girmek İstemezseniz 'Dosya Seç' Tuşuna Basarak Dosyayı Seçebilirsiniz. \n Web Sitesinden Görsel Seslendirilmesi İçin Görselin Linkini Girip 'Webden Görüntü Al' Tuşuna Basabilirsiniz. \n 'Ekran Görüntüsü Al' Tuşuna Basarak Mevcut Ekranın Görüntüsünü Alıp Seslendirilmesini Sağlayabilirsiniz.",font='Helvetica 10 bold')
canvas.create_window(250, 60, window=label)

label2 = tk.Label(text="Lütfen seslendirme dilini seçiniz.", font='Helvetica 10 bold')
canvas.create_window(250, 210, window=label2)

switch1 = ttk.Checkbutton(root, text="Temayı Değiştir", style="Switch.TCheckbutton", command = switch)
canvas.create_window(-25,325,window=switch1)

def setTextInput(text):
    entry1.delete(0,"end")
    entry1.insert(0, text)

def screenshot():
    asd = pyscreenshot.grab()
    asd.save("screenshot.png")
    entry1.delete(0,"end")
    entry1.insert(0, "screenshot.png")

def web():
    abc = entry1.get()
    img_data = requests.get(abc).content
    with open('image.png', 'wb') as handler:
        handler.write(img_data)
    entry1.delete(0,"end")
    entry1.insert(0, "image.png") 
       
entry1 = tk.Entry()
canvas.create_window(220, 120, width= 420, window=entry1)

entry2 = tk.Entry()

def fileSelect():
    filetypes = (('PNG files', '*.png*'), ('JPG files', '*.jpg'))
    global fz
    fz = fd.askopenfilename(title='Open files', initialdir='/', filetypes=filetypes)

open_button = ttk.Button(root,text='Dosya Seç', style='Accent.TButton', command=lambda:[fileSelect(),setTextInput(fz)])
canvas.create_window(480, 120, window=open_button)

    
def Process():
    xqc = entry1.get()
    if xqc == "":
        showinfo(title="UYARI!", message="Dosyayı Seçmediniz.")
    elif not xqc.endswith(".png" or ".jpg"):
        showinfo(title="UYARI!", message="Dosya Yolu ya da Dosya Formatı Hatalı. Dosya '.jpg' ya da '.png' uzantılı olmalıdır.")
    elif file_exists(xqc) == False:
        showinfo(title="UYARI!", message="Girdiğiniz dizinde böyle bir dosya bulunmamaktadır.")
    img = cv2.imread(xqc)
    imS = cv2.resize(img, (600, 400))
    cv2.namedWindow("Image")
    cv2.moveWindow("Image", 40,30)
    cv2.imshow("Image", imS)
    cv2.waitKey(0)
    data = pytesseract.image_to_data(img)
    

    filewrite = open("text.txt","w")
    for z, a in enumerate(data.splitlines()):
        if z != 0:
            a = a.split()
            if len(a) == 12:
                x, y = int(a[6]), int(a[7])
                w, h = int(a[8]), int(a[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 1)
                cv2.putText(img, a[11], (x, y + 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                filewrite.write(a[11] + " ")

    filewrite.close()

    fileread = open("text.txt", "r")
    lang = show()
    if lang == "":
        showinfo(title="UYARI!", message="Seslendirme Dilini Seçmediniz.")
        fileread.close()
        os.remove("text.txt")
    line = fileread.read()

    if line != "":
        speech = gTTS(text=line, lang=lang, slow=False)
        speech.save("record.mp3")
        fileread.close()
        os.remove("text.txt")
        playsound("record.mp3")
        os.remove("record.mp3")  
    elif line == "":
        showinfo(title="UYARI!", message="Görselde okunacak metin bulunamamıştır.")
        fileread.close()
        os.remove("text.txt")
    
    # Kelimelerin nasıl işlendiğin son halini görmek isterseniz buradaki yorum satırlarını kaldırabilirsiniz.
    # cv2.imshow("image 1", img)
    # cv2.waitKey(0)
 
button1 = ttk.Button(text='Seslendir', style='Accent.TButton',command=lambda:[Process()])
canvas.create_window(250, 295, height= 35 ,width=90 , window=button1)

button2 = ttk.Button(text='Ekran Görüntüsü Al', style='Accent.TButton',command=lambda:[screenshot()])
canvas.create_window(320, 165, height= 35 ,width=140 , window=button2)

button3 = ttk.Button(text='Webden Görüntü Al', style='Accent.TButton',command=lambda:[web()])
canvas.create_window(170, 165, height= 35 ,width=140 , window=button3)

root.mainloop()