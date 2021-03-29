import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.font import Font

import sqlite3
from sqlite3 import Error

import os
import json
import shutil
from ast import literal_eval

def getHalfWindowSize(window):
    return int(window.winfo_screenwidth() / 2) + 250, int(window.winfo_screenheight() / 1)

def getCoordinate(window, width, height):
    return int((window.winfo_screenwidth() / 2) - (width / 2)), int((window.winfo_screenheight() / 2) - (height / 2))

def createConnection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def queryKeyword(conn, keyword):
    if len(keyword) > 0:
        del listOneMorpho[:]
        del listTwoMorpho[:]
        del listReversedTwoMorpho[:]
        del listThreeMorpho[:]
        del listFourMorpho[:]
        del listOthersMorpho[:]

        listboxOneMorpho.delete(0, END)
        listboxTwoMorpho.delete(0, END)
        listboxTwoReversedMorpho.delete(0, END)
        listboxThreeMorpho.delete(0, END)
        listboxFourMorpho.delete(0, END)
        listboxOthersMorpho.delete(0, END)

        cur = conn.cursor()
        row = cur.execute(f"""SELECT * FROM dict WHERE word MATCH '{keyword}' """).fetchall()
        cur.close()

        for item in row:
            word = item[0]
            pos = item[1]
            definition = item[2]

            if keyword in word:
                if len(word.strip().split()) == 1:
                    listOneMorpho.append(item)
                elif len(word.strip().split()) == 2:
                    if word.strip().startswith(keyword):
                        listTwoMorpho.append(item)
                    else:
                        listReversedTwoMorpho.append(item)
                elif len(word.strip().split()) == 3:
                    listThreeMorpho.append(item)
                elif len(word.strip().split()) == 4:
                    listFourMorpho.append(item)
                else:
                    listOthersMorpho.append(item)

        # Add data to morpho list
        for oneIndex, oneItem in enumerate(listOneMorpho):
            listboxOneMorpho.insert(oneIndex + 1, oneItem[0])

        for twoIndex, twoItem in enumerate(listTwoMorpho):
            listboxTwoMorpho.insert(twoIndex + 1, twoItem[0])

        for rtwoIndex, rtwoItem in enumerate(listReversedTwoMorpho):
            listboxTwoReversedMorpho.insert(rtwoIndex + 1, rtwoItem[0])

        for threeIndex, threeItem in enumerate(listThreeMorpho):
            listboxThreeMorpho.insert(threeIndex + 1, threeItem[0])

        for fourIndex, fourItem in enumerate(listFourMorpho):
            listboxFourMorpho.insert(fourIndex + 1, fourItem[0])

        for othersIndex, othersItem in enumerate(listOthersMorpho):
            listboxOthersMorpho.insert(othersIndex + 1, othersItem[0])

def updateIndep(indepText):
    with open('./resources/doclap.txt', 'w') as fdl:
        fdl.write(indepText)

    messagebox.showinfo("Trạng thái", "Đã lưu thành công")

def updateDep(depText):
    with open('./resources/khongdoclap.txt', 'w') as fkdl:
        fkdl.write(depText)

    messagebox.showinfo("Trạng thái", "Đã lưu thành công")

def updateImageKeyword(conn, keyword):
    if keyword is not None and len(keyword.get()) > 0:
        filetypes = (
            ('Image files', ('.png', '.jpg', '.jpeg')),
        )

        filename = askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        if filename or len(filename) > 0:
            if os.path.exists('./images/' + os.path.basename(filename)) is False:
                keyword = literal_eval(keyword.get())

                strImagePaths = StringVar()

                if keyword[3] == 'None':
                    strImagePaths.set('[]')
                else:
                    strImagePaths.set(keyword[3])

                lstImagePaths = json.loads(strImagePaths.get())
                lstImagePaths.append(os.path.basename(filename))

                strImagePathsToSave = json.dumps(lstImagePaths)

                cur = conn.cursor()
                cur.execute(f"""UPDATE dict SET images='{strImagePathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
                conn.commit()
                cur.close()

                listboxImage.insert(len(lstImagePaths), os.path.basename(filename))

                shutil.copy2(filename, './images')

                messagebox.showinfo(
                    title='Đã lưu thành công',
                    message=filename
                )
            else:
                messagebox.showinfo(
                    title='Tập tin đã tồn tại',
                    message='./images/' + os.path.basename(filename)
                )

def updateVideoKeyword(conn, keyword):
    if keyword is not None and len(keyword.get()) > 0: 
        filetypes = (
            ('Video files', ('.mp4', '.avi', '.mov', '.mpg', '.m4v', '.flv', '.mkv', '.webm')),
        )

        filename = askopenfilename(
            title='Open a video',
            initialdir='/',
            filetypes=filetypes
        )

        if filename or len(filename) > 0:
            if os.path.exists('./videos/' + os.path.basename(filename)) is False:
                keyword = literal_eval(keyword.get())

                strVideoPaths = StringVar()

                if keyword[4] == 'None':
                    strVideoPaths.set('[]')
                else:
                    strVideoPaths.set(keyword[4])

                lstVideoPaths = json.loads(strVideoPaths.get())
                lstVideoPaths.append(os.path.basename(filename))

                strVideoPathsToSave = json.dumps(lstVideoPaths)

                cur = conn.cursor()
                cur.execute(f"""UPDATE dict SET videos='{strVideoPathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
                conn.commit()
                cur.close()

                listboxVideo.insert(len(lstVideoPaths), os.path.basename(filename))

                shutil.copy2(filename, './videos')

                messagebox.showinfo(
                    title='Đã lưu thành công',
                    message=filename
                )
            else:
                messagebox.showinfo(
                    title='Tập tin đã tồn tại',
                    message='./videos/' + os.path.basename(filename)
                )

def deleteImageKeyword(conn, keyword):
    if keyword is not None and len(keyword.get()) > 0:
        filename = listboxImage.get(listboxImage.curselection())

        # Remove on UI
        idx = listboxImage.get(0, END).index(filename)
        listboxImage.delete(idx)

        # Remove in hard disk
        if os.path.exists('./images/' + filename):
            os.remove('./images/' + filename)

        # Remove on database
        keyword = literal_eval(keyword.get())

        strImagePaths = StringVar()

        if keyword[3] == 'None':
            strImagePaths.set('[]')
        else:
            strImagePaths.set(keyword[3])

        lstImagePaths = json.loads(strImagePaths.get())
        lstImagePaths.remove(filename)

        strImagePathsToSave = json.dumps(lstImagePaths)

        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET images='{strImagePathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        messagebox.showinfo(
            title='Đã xoá thành công',
            message='./images/' + filename
        )

def deleteVideoKeyword(conn, keyword):
    if keyword is not None and len(keyword.get()) > 0:
        filename = listboxVideo.get(listboxVideo.curselection())
        
        # Remove on UI
        idx = listboxVideo.get(0, END).index(filename)
        listboxVideo.delete(idx)

        # Remove in hard disk
        if os.path.exists('./videos/' + filename):
            os.remove('./videos/' + filename)

        # Remove on database
        keyword = literal_eval(keyword.get())

        strVideoPaths = StringVar()

        if keyword[3] == 'None':
            strVideoPaths.set('[]')
        else:
            strVideoPaths.set(keyword[3])

        lstVideoPaths = json.loads(strVideoPaths.get())
        lstVideoPaths.remove(filename)

        strVideoPathsToSave = json.dumps(lstVideoPaths)

        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET images='{strVideoPathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        messagebox.showinfo(
            title='Đã xoá thành công',
            message='./videos' + filename
        )

def updateNoteKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET notes='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        if cur.rowcount < 1:
            messagebox.error("Trạng thái", "Lưu thất bại")
        else:
            messagebox.showinfo("Trạng thái", "Đã lưu thành công")

def updateForeignKeyword(conn, keyword):
    pass

def callbackOneMorpho(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = listOneMorpho[index]
        currentSelectedKeyword.set(data)

        txt_def = data[1] + '\n' + data[2]

        textDefinition.delete('1.0', END)

        textDefinition.insert('1.0', txt_def)

        # image
        if data[3] is not None:
            img_list = json.loads(data[3])
            
            for imgIndex, imgItem in enumerate(img_list):
                listboxImage.insert(imgIndex + 1, imgItem)

        # video
        if data[4] is not None:
            vid_list = json.loads(data[4])

            for vidIndex, vidItem in enumerate(vid_list):
                listboxVideo.insert(vidIndex + 1, vidItem)

        # note
        if data[5] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[5])

        # foreign
        if data[6] is not None:
            forg_list = data[6].split(';')

            for forgIndex, forgItem in enumerate(forg_list):
                listboxForeign.insert(forgIndex + 1, forgItem.split('<|>')[0])

        return data

def callbackTwoMorpho(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = listTwoMorpho[index]
        currentSelectedKeyword.set(data)

        txt_def = data[1] + '\n' + data[2]

        textDefinition.delete('1.0', END)

        textDefinition.insert('1.0', txt_def)

       # image
        if data[3] is not None:
            img_list = json.loads(data[3])
            
            for imgIndex, imgItem in enumerate(img_list):
                listboxImage.insert(imgIndex + 1, imgItem)

        # video
        if data[4] is not None:
            vid_list = json.loads(data[4])

            for vidIndex, vidItem in enumerate(vid_list):
                listboxVideo.insert(vidIndex + 1, vidItem)

        # note
        if data[5] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[5])

        # foreign
        if data[6] is not None:
            forg_list = data[6].split(';')

            for forgIndex, forgItem in enumerate(forg_list):
                listboxForeign.insert(forgIndex + 1, forgItem.split('<|>')[0])

def callbackTwoReversedMorpho(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = listReversedTwoMorpho[index]
        currentSelectedKeyword.set(data)

        txt_def = data[1] + '\n' + data[2]

        textDefinition.delete('1.0', END)

        textDefinition.insert('1.0', txt_def)

        # image
        if data[3] is not None:
            img_list = json.loads(data[3])
            
            for imgIndex, imgItem in enumerate(img_list):
                listboxImage.insert(imgIndex + 1, imgItem)

        # video
        if data[4] is not None:
            vid_list = json.loads(data[4])

            for vidIndex, vidItem in enumerate(vid_list):
                listboxVideo.insert(vidIndex + 1, vidItem)

        # note
        if data[5] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[5])

        # foreign
        if data[6] is not None:
            forg_list = data[6].split(';')

            for forgIndex, forgItem in enumerate(forg_list):
                listboxForeign.insert(forgIndex + 1, forgItem.split('<|>')[0])

def callbackThreeMorpho(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = listThreeMorpho[index]
        currentSelectedKeyword.set(data)

        txt_def = data[1] + '\n' + data[2]

        textDefinition.delete('1.0', END)

        textDefinition.insert('1.0', txt_def)

        # image
        if data[3] is not None:
            img_list = json.loads(data[3])
            
            for imgIndex, imgItem in enumerate(img_list):
                listboxImage.insert(imgIndex + 1, imgItem)

        # video
        if data[4] is not None:
            vid_list = json.loads(data[4])

            for vidIndex, vidItem in enumerate(vid_list):
                listboxVideo.insert(vidIndex + 1, vidItem)

        # note
        if data[5] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[5])

        # foreign
        if data[6] is not None:
            forg_list = data[6].split(';')

            for forgIndex, forgItem in enumerate(forg_list):
                listboxForeign.insert(forgIndex + 1, forgItem.split('<|>')[0])

def callbackFourMorpho(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = listFourMorpho[index]
        currentSelectedKeyword.set(data)

        txt_def = data[1] + '\n' + data[2]

        textDefinition.delete('1.0', END)

        textDefinition.insert('1.0', txt_def)

        # image
        if data[3] is not None:
            img_list = json.loads(data[3])
            
            for imgIndex, imgItem in enumerate(img_list):
                listboxImage.insert(imgIndex + 1, imgItem)

        # video
        if data[4] is not None:
            vid_list = json.loads(data[4])

            for vidIndex, vidItem in enumerate(vid_list):
                listboxVideo.insert(vidIndex + 1, vidItem)

        # note
        if data[5] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[5])

        # foreign
        if data[6] is not None:
            forg_list = data[6].split(';')

            for forgIndex, forgItem in enumerate(forg_list):
                listboxForeign.insert(forgIndex + 1, forgItem.split('<|>')[0])

def callbackOthersMorpho(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = listOthersMorpho[index]
        currentSelectedKeyword.set(data)

        txt_def = data[1] + '\n' + data[2]

        textDefinition.delete('1.0', END)

        textDefinition.insert('1.0', txt_def)

        # image
        if data[3] is not None:
            img_list = json.loads(data[3])
            
            for imgIndex, imgItem in enumerate(img_list):
                listboxImage.insert(imgIndex + 1, imgItem)

        # video
        if data[4] is not None:
            vid_list = json.loads(data[4])

            for vidIndex, vidItem in enumerate(vid_list):
                listboxVideo.insert(vidIndex + 1, vidItem)

        # note
        if data[5] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[5])

        # foreign
        if data[6] is not None:
            forg_list = data[6].split(';')

            for forgIndex, forgItem in enumerate(forg_list):
                listboxForeign.insert(forgIndex + 1, forgItem.split('<|>')[0])

def callbackImage(event):
    selection = event.widget.curselection()
    if selection:
        value = event.widget.get(selection[0])
        os.startfile(os.path.normpath(os.path.join('./images/' + value)))

def callbackVideo(event):
    selection = event.widget.curselection()
    if selection:
        value = event.widget.get(selection[0])
        os.startfile(os.path.normpath(os.path.join('./videos/' + value)))

print('Starting to pre-processing...')

# create a tkinter window
window = tkinter.Tk()

str_unbind = ""

currentSelectedKeyword = StringVar()

dependentContent = ""
independentContent = ""

listOneMorpho = []
listTwoMorpho = []
listReversedTwoMorpho = []
listThreeMorpho = []
listFourMorpho = []
listOthersMorpho = []

# Connect to db
conn = createConnection('./my_fts_data_update.db')

# Init frame
width, height = getHalfWindowSize(window)
x, y = getCoordinate(window, width, height)

# Open window having dimension 100x100
window.geometry(f'{width}x{height}+{x}+{y}')

# to rename the title of the window
window.title("Từ điển tiếng Việt")

container = Frame(window)
canvas = Canvas(container)
scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="my_tag")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.bind(
    "<Configure>", 
    lambda e: canvas.itemconfig(
        "my_tag", width=e.width
    )
)

####################################################
# pack is used to show the object in the window
tkinter.Label(scrollable_frame, text = "Chào mừng đến với Từ điển Tiếng Việt").pack()

if os.path.isdir('./videos') is False:
    os.makedirs('./videos')

if os.path.isdir('./images') is False:
    os.makedirs('./images')

if os.path.isdir('./resources') is False:
    os.makedirs('./resources')
else:
    if os.path.exists('./resources/doclap.txt') is False:
        with open('./resources/doclap.txt', 'a') as fdl:
            pass

    with open('./resources/doclap.txt') as fdl:
            dependentContent = fdl.read()
        
    if os.path.exists('./resources/khongdoclap.txt') is False:
        with open('./resources/khongdoclap.txt', 'a') as fkdl:
            pass

    with open('./resources/khongdoclap.txt') as fkdl:
            independentContent = fkdl.read()

# Set position for search bar
frame_searchBar = Frame(scrollable_frame, relief=RAISED)
frame_searchBar.pack(fill=X, padx=6, pady=4)

def deleteText(event, entry):
    entry.delete(0, END)
    entry.unbind('<Button>', str_unbind)

userInput = StringVar(window)

button = Button(frame_searchBar, text="Tìm kiếm", command=lambda : queryKeyword(conn, userInput.get()))
button.pack(side=RIGHT)

myFont = Font(family="Times New Roman", size=14)

entry = Entry(frame_searchBar, textvariable=userInput)
entry.insert(0, "Nhập từ cần tìm...")
entry.configure(font=myFont)
str_unbind = entry.bind("<Button>", lambda event: deleteText(event, entry))
entry.pack(fill=X)

# set position for word class
frame_wordClass = Frame(scrollable_frame)
frame_wordClass.pack(expand=True, padx=6, pady=4)

labelIndependent = Label(frame_wordClass, text="Độc lập")
labelIndependent.pack(fill=X)

textIndependent = Text(frame_wordClass, height=10)
textIndependent.pack(fill=X)
textIndependent.configure(font=myFont)
textIndependent.insert("1.0", independentContent)

buttonIndependent = Button(frame_wordClass, text="Cập nhật thông tin độc lập", command=lambda : updateIndep(textIndependent.get("1.0", 'end-1c')))
buttonIndependent.pack(fill=X)

labelDependent = Label(frame_wordClass, text="Không độc lập")
labelDependent.pack(fill=X)

textDependent = Text(frame_wordClass, height=10)
textDependent.pack(fill=X)
textDependent.configure(font=myFont)
textDependent.insert("1.0", dependentContent)

buttonDependent = Button(frame_wordClass, text="Cập nhật thông tin không độc lập", command=lambda : updateDep(textDependent.get("1.0", 'end-1c')))
buttonDependent.pack(fill=X)

# set position for word type
frame_wordType = Frame(scrollable_frame)
frame_wordType.pack(expand=True, padx=6, pady=4)

listboxOneMorpho = Listbox(frame_wordType, width=25, height=20)
listboxOneMorpho.pack(side=LEFT)
listboxOneMorpho.bind("<<ListboxSelect>>", callbackOneMorpho)

listboxTwoMorpho = Listbox(frame_wordType, width=25, height=20)
listboxTwoMorpho.pack(side=LEFT)
listboxTwoMorpho.bind("<<ListboxSelect>>", callbackTwoMorpho)

listboxTwoReversedMorpho = Listbox(frame_wordType, width=25, height=20)
listboxTwoReversedMorpho.pack(side=LEFT)
listboxTwoReversedMorpho.bind("<<ListboxSelect>>", callbackTwoReversedMorpho)

# set position for word type
frame_wordTypeAddition = Frame(scrollable_frame)
frame_wordTypeAddition.pack(expand=True, padx=6, pady=4)

listboxThreeMorpho = Listbox(frame_wordTypeAddition, width=25, height=20)
listboxThreeMorpho.pack(side=LEFT)
listboxThreeMorpho.bind("<<ListboxSelect>>", callbackThreeMorpho)

listboxFourMorpho = Listbox(frame_wordTypeAddition, width=25, height=20)
listboxFourMorpho.pack(side=LEFT)
listboxFourMorpho.bind("<<ListboxSelect>>", callbackFourMorpho)

listboxOthersMorpho = Listbox(frame_wordTypeAddition, width=25, height=20)
listboxOthersMorpho.pack(side=LEFT)
listboxOthersMorpho.bind("<<ListboxSelect>>", callbackOthersMorpho)

# set position for definition
frame_definition = Frame(scrollable_frame)
frame_definition.pack(expand=True, padx=6, pady=4)

labelDefinition = Label(frame_definition, text="Định ngĩa")
labelDefinition.pack(fill=X)

textDefinition = Text(frame_definition, height=10)
textDefinition.pack(fill=X)
textDefinition.configure(font=myFont)

# buttonDefinition = Button(frame_definition, text="Cập nhật thông tin định nghĩa")
# buttonDefinition.pack(fill=X)

# frame for image & video
frame_ImageVideo = Frame(scrollable_frame)
frame_ImageVideo.pack(expand=True, padx=6, pady=4)

# set position for image
frame_image = Frame(frame_ImageVideo)
frame_image.pack(side=LEFT, padx=10, pady=4)

labelSelectImage = Label(frame_image, text="Chọn hình ảnh cần xem")
labelSelectImage.pack(fill=X)

listboxImage = Listbox(frame_image, height=15)
listboxImage.pack(fill=X)
listboxImage.bind("<<ListboxSelect>>", callbackImage)

buttonImage = Button(frame_image, text="Cập nhật hình ảnh", command=lambda : updateImageKeyword(conn, currentSelectedKeyword))
buttonImage.pack(fill=X)

buttonDeleteImage = Button(frame_image, text="Xoá hình ảnh đang chọn", command=lambda : deleteImageKeyword(conn, currentSelectedKeyword))
buttonDeleteImage.pack(fill=X, pady=8)

# set position for video
frame_video = Frame(frame_ImageVideo)
frame_video.pack(side=LEFT, padx=10, pady=4)

labelSelectVideo = Label(frame_video, text="Chọn video cần xem")
labelSelectVideo.pack(fill=X)

listboxVideo = Listbox(frame_video, height=15)
listboxVideo.pack(fill=X)
listboxVideo.bind("<<ListboxSelect>>", callbackVideo)

buttonVideo = Button(frame_video, text="Cập nhật video", command=lambda : updateVideoKeyword(conn, currentSelectedKeyword))
buttonVideo.pack(fill=X)

buttonDeleteVideo = Button(frame_video, text="Xoá video đang chọn", command=lambda : deleteVideoKeyword(conn, currentSelectedKeyword))
buttonDeleteVideo.pack(fill=X, pady=8)

# set position for notes
frame_note = Frame(scrollable_frame)
frame_note.pack(expand=True, padx=6, pady=4)

labelNote = Label(frame_note, text="Ghi chú")
labelNote.pack(fill=X)

textNote = Text(frame_note, height=10)
textNote.pack(fill=X)

buttonNote = Button(frame_note, text="Cập nhật ghi chú", command=lambda : updateNoteKeyword(conn, currentSelectedKeyword, textNote.get('1.0', 'end-1c')))
buttonNote.pack(fill=X)

# set position for foreign
frame_foreign = Frame(scrollable_frame)
frame_foreign.pack(expand=True, padx=6, pady=6)

labelForeign = Label(frame_foreign, text="Ngôn ngữ khác")
labelForeign.pack(fill=X)

listboxForeign = Listbox(frame_foreign, height=8)
listboxForeign.pack(side=LEFT)

textForeign = Text(frame_foreign, height=10)
textForeign.pack(side=LEFT, padx=6)
textForeign.configure(font=myFont)

buttonForeign = Button(frame_foreign, text="Cập nhật ngôn ngữ")
buttonForeign.pack(fill=X)
####################################################

container.pack(fill=BOTH, expand=True)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=BOTH)

# Start to run window
window.mainloop()

conn.close()
print('Terminate processsing...')

