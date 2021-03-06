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

def bound_to_mousewheel(event):
    canvas.bind_all("<MouseWheel>", on_mousewheel)

def unbound_to_mousewheel(event):
    canvas.unbind_all("<MouseWheel>")

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

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

def updateCurrentSelectedKeyword(keyword):
    if len(keyword) > 0:
        del listOneMorpho[:]
        del listTwoMorpho[:]
        del listReversedTwoMorpho[:]
        del listThreeMorpho[:]
        del listFourMorpho[:]
        del listOthersMorpho[:]

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

def updateIndep(indepText):
    with open('./resources/doclap.txt', 'w') as fdl:
        fdl.write(indepText)

    messagebox.showinfo("Tr???ng th??i", "???? l??u th??nh c??ng")

def updateDep(depText):
    with open('./resources/khongdoclap.txt', 'w') as fkdl:
        fkdl.write(depText)

    messagebox.showinfo("Tr???ng th??i", "???? l??u th??nh c??ng")

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

                # save to database
                cur = conn.cursor()
                cur.execute(f"""UPDATE dict SET images='{strImagePathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
                conn.commit()
                cur.close()

                # save to UI
                listboxImage.insert(len(lstImagePaths), os.path.basename(filename))

                # save to hard disk
                shutil.copy2(filename, './images')

                # save to selected item
                keyword = list(keyword)
                keyword[3] = json.dumps(lstImagePaths)
                currentSelectedKeyword.set(tuple(keyword))

                updateCurrentSelectedKeyword(userInput.get())

                if cur.rowcount < 1:
                    messagebox.error("Tr???ng th??i", "L??u th???t b???i")
                else:
                    messagebox.showinfo(
                        title='???? l??u th??nh c??ng',
                        message=filename
                    )
                
            else:
                messagebox.showinfo(
                    title='T???p tin ???? t???n t???i',
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

                # save to database
                cur = conn.cursor()
                cur.execute(f"""UPDATE dict SET videos='{strVideoPathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
                conn.commit()
                cur.close()

                # save to UI
                listboxVideo.insert(len(lstVideoPaths), os.path.basename(filename))

                # save to hard disk
                shutil.copy2(filename, './videos')

                # save to selected item
                keyword = list(keyword)
                keyword[3] = json.dumps(lstVideoPaths)
                currentSelectedKeyword.set(tuple(keyword))

                updateCurrentSelectedKeyword(userInput.get())

                if cur.rowcount < 1:
                    messagebox.error("Tr???ng th??i", "L??u th???t b???i")
                else:
                    messagebox.showinfo(
                        title='???? l??u th??nh c??ng',
                        message=filename
                    )
                
            else:
                messagebox.showinfo(
                    title='T???p tin ???? t???n t???i',
                    message='./videos/' + os.path.basename(filename)
                )

def updateAudioKeyword(conn, keyword):
    if keyword is not None and len(keyword.get()) > 0: 
        filetypes = (
            ('Audio files', ('.mp3', '.m4a', '.wav')),
        )

        filename = askopenfilename(
            title='Open a audio',
            initialdir='/',
            filetypes=filetypes
        )

        if filename or len(filename) > 0:
            if os.path.exists('./audios/' + os.path.basename(filename)) is False:
                keyword = literal_eval(keyword.get())

                strAudioPaths = StringVar()

                if keyword[4] == 'None':
                    strAudioPaths.set('[]')
                else:
                    strAudioPaths.set(keyword[4])

                lstAudioPaths = json.loads(strAudioPaths.get())
                lstAudioPaths.append(os.path.basename(filename))
                strAudioPathsToSave = json.dumps(lstAudioPaths)

                # save to database
                cur = conn.cursor()
                cur.execute(f"""UPDATE dict SET audios='{strAudioPathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
                conn.commit()
                cur.close()

                # save to UI
                listboxAudio.insert(len(lstAudioPaths), os.path.basename(filename))

                # save to hard disk
                shutil.copy2(filename, './audios')

                # save to selected item
                keyword = list(keyword)
                keyword[3] = json.dumps(lstAudioPaths)
                currentSelectedKeyword.set(tuple(keyword))

                updateCurrentSelectedKeyword(userInput.get())

                if cur.rowcount < 1:
                    messagebox.error("Tr???ng th??i", "L??u th???t b???i")
                else:
                    messagebox.showinfo(
                        title='???? l??u th??nh c??ng',
                        message=filename
                    )
                
            else:
                messagebox.showinfo(
                    title='T???p tin ???? t???n t???i',
                    message='./audios/' + os.path.basename(filename)
                )

def deleteImageKeyword(conn, keyword):
    if keyword is not None and len(keyword.get()) > 0:
        filename = listboxImage.get(listboxImage.curselection())

        if os.path.exists('./images/' + filename):
            # Remove in hard disk
            os.remove('./images/' + filename)

            # Remove on UI
            idx = listboxImage.get(0, END).index(filename)
            listboxImage.delete(idx)

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

            # save to selected item
            keyword = list(keyword)
            keyword[3] = json.dumps(lstImagePaths)
            currentSelectedKeyword.set(tuple(keyword))

            updateCurrentSelectedKeyword(userInput.get())

            if cur.rowcount < 1:
                messagebox.error("Tr???ng th??i", "Xo?? th???t b???i")
            else:
                messagebox.showinfo(
                    title='???? xo?? th??nh c??ng',
                    message='./images/' + filename
                )

def deleteVideoKeyword(conn, keyword):
    if keyword is not None and len(keyword.get()) > 0:
        filename = listboxVideo.get(listboxVideo.curselection())

        if os.path.exists('./videos/' + filename):
            # Remove in hard disk
            os.remove('./videos/' + filename)

            # Remove on UI
            idx = listboxVideo.get(0, END).index(filename)
            listboxVideo.delete(idx)

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
            cur.execute(f"""UPDATE dict SET videos='{strVideoPathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
            conn.commit()
            cur.close()

            # save to selected item
            keyword = list(keyword)
            keyword[3] = json.dumps(lstVideoPaths)
            currentSelectedKeyword.set(tuple(keyword))

            updateCurrentSelectedKeyword(userInput.get())

            if cur.rowcount < 1:
                messagebox.error("Tr???ng th??i", "Xo?? th???t b???i")
            else:
                messagebox.showinfo(
                    title='???? xo?? th??nh c??ng',
                    message='./videos' + filename
                )

def deleteAudioKeyword(conn, keyword):
    if keyword is not None and len(keyword.get()) > 0:
        filename = listboxAudio.get(listboxAudio.curselection())

        if os.path.exists('./audios/' + filename):
            # Remove in hard disk
            os.remove('./audios/' + filename)

            # Remove on UI
            idx = listboxAudio.get(0, END).index(filename)
            listboxAudio.delete(idx)

            # Remove on database
            keyword = literal_eval(keyword.get())

            strAudioPaths = StringVar()

            if keyword[3] == 'None':
                strAudioPaths.set('[]')
            else:
                strAudioPaths.set(keyword[3])

            lstAudioPaths = json.loads(strAudioPaths.get())
            lstAudioPaths.remove(filename)

            strAudioPathsToSave = json.dumps(lstAudioPaths)

            cur = conn.cursor()
            cur.execute(f"""UPDATE dict SET audios='{strAudioPathsToSave}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
            conn.commit()
            cur.close()

            # save to selected item
            keyword = list(keyword)
            keyword[3] = json.dumps(lstAudioPaths)
            currentSelectedKeyword.set(tuple(keyword))

            updateCurrentSelectedKeyword(userInput.get())

            if cur.rowcount < 1:
                messagebox.error("Tr???ng th??i", "Xo?? th???t b???i")
            else:
                messagebox.showinfo(
                    title='???? xo?? th??nh c??ng',
                    message='./audios' + filename
                )

def updateNoteKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET notes='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        updateCurrentSelectedKeyword(userInput.get())

        if cur.rowcount < 1:
            messagebox.error("Tr???ng th??i", "L??u th???t b???i")
        else:
            messagebox.showinfo("Tr???ng th??i", "???? l??u th??nh c??ng")

def updateEnglishKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET english='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        updateCurrentSelectedKeyword(userInput.get())

        if cur.rowcount < 1:
            messagebox.error("Tr???ng th??i", "L??u th???t b???i")
        else:
            messagebox.showinfo("Tr???ng th??i", "???? l??u ti???ng Anh th??nh c??ng")

def updateFranceKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET france='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        updateCurrentSelectedKeyword(userInput.get())

        if cur.rowcount < 1:
            messagebox.error("Tr???ng th??i", "L??u th???t b???i")
        else:
            messagebox.showinfo("Tr???ng th??i", "???? l??u ti???ng Ph??p th??nh c??ng")

def updateRussiaKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET russia='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        updateCurrentSelectedKeyword(userInput.get())

        if cur.rowcount < 1:
            messagebox.error("Tr???ng th??i", "L??u th???t b???i")
        else:
            messagebox.showinfo("Tr???ng th??i", "???? l??u ti???ng Nga th??nh c??ng")

def updateChineseKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET chinese='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        updateCurrentSelectedKeyword(userInput.get())

        if cur.rowcount < 1:
            messagebox.error("Tr???ng th??i", "L??u th???t b???i")
        else:
            messagebox.showinfo("Tr???ng th??i", "???? l??u ti???ng Trung th??nh c??ng")

def updateJapanKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET japan='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        updateCurrentSelectedKeyword(userInput.get())

        if cur.rowcount < 1:
            messagebox.error("Tr???ng th??i", "L??u th???t b???i")
        else:
            messagebox.showinfo("Tr???ng th??i", "???? l??u ti???ng Nh???t th??nh c??ng")

def updateKoreaKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET korea='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        updateCurrentSelectedKeyword(userInput.get())

        if cur.rowcount < 1:
            messagebox.error("Tr???ng th??i", "L??u th???t b???i")
        else:
            messagebox.showinfo("Tr???ng th??i", "???? l??u ti???ng H??n th??nh c??ng")

def updateSpainKeyword(conn, keyword, newText):
    if keyword is not None and len(keyword.get()) > 0:
        keyword = literal_eval(keyword.get())
        cur = conn.cursor()
        cur.execute(f"""UPDATE dict SET spain='{newText}' WHERE word='{keyword[0]}' AND POS='{keyword[1]}' AND definition='{keyword[2]}' """)
        conn.commit()
        cur.close()

        updateCurrentSelectedKeyword(userInput.get())

        if cur.rowcount < 1:
            messagebox.error("Tr???ng th??i", "L??u th???t b???i")
        else:
            messagebox.showinfo("Tr???ng th??i", "???? l??u ti???ng T??y Ban Nha th??nh c??ng")

def callbackOneMorpho(event):
    selection = event.widget.curselection()
    if selection:
        # clear
        listboxImage.delete(0, END)
        listboxVideo.delete(0, END)
        listboxAudio.delete(0, END)

        textNote.delete('1.0', END)
        textEnglish.delete('1.0', END)
        textFrance.delete('1.0', END)
        textRussia.delete('1.0', END)
        textChinese.delete('1.0', END)
        textJapan.delete('1.0', END)
        textKorea.delete('1.0', END)
        textSpain.delete('1.0', END)

        # end clear
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

        # audio
        if data[5] is not None:
            aud_list = json.loads(data[5])

            for audIndex, audItem in enumerate(aud_list):
                listboxAudio.insert(audIndex + 1, audItem)

        # note
        if data[6] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[6])

        # english
        if data[7] is not None:
            textEnglish.delete('1.0', END)
            textEnglish.insert('1.0', data[7])

        # france
        if data[8] is not None:
            textFrance.delete('1.0', END)
            textFrance.insert('1.0', data[8])

        # russia
        if data[9] is not None:
            textRussia.delete('1.0', END)
            textRussia.insert('1.0', data[9])

        # chinese
        if data[10] is not None:
            textChinese.delete('1.0', END)
            textChinese.insert('1.0', data[10])

        # japan
        if data[11] is not None:
            textJapan.delete('1.0', END)
            textJapan.insert('1.0', data[11])

        # korea
        if data[12] is not None:
            textKorea.delete('1.0', END)
            textKorea.insert('1.0', data[12])

        # spain
        if data[13] is not None:
            textSpain.delete('1.0', END)
            textSpain.insert('1.0', data[13])

        return data

def callbackTwoMorpho(event):
    selection = event.widget.curselection()
    if selection:
        # clear
        listboxImage.delete(0, END)
        listboxVideo.delete(0, END)
        listboxAudio.delete(0, END)

        textNote.delete('1.0', END)
        textEnglish.delete('1.0', END)
        textFrance.delete('1.0', END)
        textRussia.delete('1.0', END)
        textChinese.delete('1.0', END)
        textJapan.delete('1.0', END)
        textKorea.delete('1.0', END)
        textSpain.delete('1.0', END)
        
        # end clear
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

        # audio
        if data[5] is not None:
            aud_list = json.loads(data[5])

            for audIndex, audItem in enumerate(aud_list):
                listboxAudio.insert(audIndex + 1, audItem)

        # note
        if data[6] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[6])

        # english
        if data[7] is not None:
            textEnglish.delete('1.0', END)
            textEnglish.insert('1.0', data[7])

        # france
        if data[8] is not None:
            textFrance.delete('1.0', END)
            textFrance.insert('1.0', data[8])

        # russia
        if data[9] is not None:
            textRussia.delete('1.0', END)
            textRussia.insert('1.0', data[9])

        # chinese
        if data[10] is not None:
            textChinese.delete('1.0', END)
            textChinese.insert('1.0', data[10])

        # japan
        if data[11] is not None:
            textJapan.delete('1.0', END)
            textJapan.insert('1.0', data[11])

        # korea
        if data[12] is not None:
            textKorea.delete('1.0', END)
            textKorea.insert('1.0', data[12])

        # spain
        if data[13] is not None:
            textSpain.delete('1.0', END)
            textSpain.insert('1.0', data[13])

def callbackTwoReversedMorpho(event):
    selection = event.widget.curselection()
    if selection:
        # clear
        listboxImage.delete(0, END)
        listboxVideo.delete(0, END)
        listboxAudio.delete(0, END)

        textNote.delete('1.0', END)
        textEnglish.delete('1.0', END)
        textFrance.delete('1.0', END)
        textRussia.delete('1.0', END)
        textChinese.delete('1.0', END)
        textJapan.delete('1.0', END)
        textKorea.delete('1.0', END)
        textSpain.delete('1.0', END)
        
        # end clear
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

        # audio
        if data[5] is not None:
            aud_list = json.loads(data[5])

            for audIndex, audItem in enumerate(aud_list):
                listboxAudio.insert(audIndex + 1, audItem)

        # note
        if data[6] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[6])

        # english
        if data[7] is not None:
            textEnglish.delete('1.0', END)
            textEnglish.insert('1.0', data[7])

        # france
        if data[8] is not None:
            textFrance.delete('1.0', END)
            textFrance.insert('1.0', data[8])

        # russia
        if data[9] is not None:
            textRussia.delete('1.0', END)
            textRussia.insert('1.0', data[9])

        # chinese
        if data[10] is not None:
            textChinese.delete('1.0', END)
            textChinese.insert('1.0', data[10])

        # japan
        if data[11] is not None:
            textJapan.delete('1.0', END)
            textJapan.insert('1.0', data[11])

        # korea
        if data[12] is not None:
            textKorea.delete('1.0', END)
            textKorea.insert('1.0', data[12])

        # spain
        if data[13] is not None:
            textSpain.delete('1.0', END)
            textSpain.insert('1.0', data[13])

def callbackThreeMorpho(event):
    selection = event.widget.curselection()
    if selection:
        # clear
        listboxImage.delete(0, END)
        listboxVideo.delete(0, END)
        listboxAudio.delete(0, END)

        textNote.delete('1.0', END)
        textEnglish.delete('1.0', END)
        textFrance.delete('1.0', END)
        textRussia.delete('1.0', END)
        textChinese.delete('1.0', END)
        textJapan.delete('1.0', END)
        textKorea.delete('1.0', END)
        textSpain.delete('1.0', END)
        
        # end clear
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

        # audio
        if data[5] is not None:
            aud_list = json.loads(data[5])

            for audIndex, audItem in enumerate(aud_list):
                listboxAudio.insert(audIndex + 1, audItem)

        # note
        if data[6] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[6])

        # english
        if data[7] is not None:
            textEnglish.delete('1.0', END)
            textEnglish.insert('1.0', data[7])

        # france
        if data[8] is not None:
            textFrance.delete('1.0', END)
            textFrance.insert('1.0', data[8])

        # russia
        if data[9] is not None:
            textRussia.delete('1.0', END)
            textRussia.insert('1.0', data[9])

        # chinese
        if data[10] is not None:
            textChinese.delete('1.0', END)
            textChinese.insert('1.0', data[10])

        # japan
        if data[11] is not None:
            textJapan.delete('1.0', END)
            textJapan.insert('1.0', data[11])

        # korea
        if data[12] is not None:
            textKorea.delete('1.0', END)
            textKorea.insert('1.0', data[12])

        # spain
        if data[13] is not None:
            textSpain.delete('1.0', END)
            textSpain.insert('1.0', data[13])

def callbackFourMorpho(event):
    selection = event.widget.curselection()
    if selection:
        # clear
        listboxImage.delete(0, END)
        listboxVideo.delete(0, END)
        listboxAudio.delete(0, END)

        textNote.delete('1.0', END)
        textEnglish.delete('1.0', END)
        textFrance.delete('1.0', END)
        textRussia.delete('1.0', END)
        textChinese.delete('1.0', END)
        textJapan.delete('1.0', END)
        textKorea.delete('1.0', END)
        textSpain.delete('1.0', END)
        
        # end clear
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

        # audio
        if data[5] is not None:
            aud_list = json.loads(data[5])

            for audIndex, audItem in enumerate(aud_list):
                listboxAudio.insert(audIndex + 1, audItem)

        # note
        if data[6] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[6])

        # english
        if data[7] is not None:
            textEnglish.delete('1.0', END)
            textEnglish.insert('1.0', data[7])

        # france
        if data[8] is not None:
            textFrance.delete('1.0', END)
            textFrance.insert('1.0', data[8])

        # russia
        if data[9] is not None:
            textRussia.delete('1.0', END)
            textRussia.insert('1.0', data[9])

        # chinese
        if data[10] is not None:
            textChinese.delete('1.0', END)
            textChinese.insert('1.0', data[10])

        # japan
        if data[11] is not None:
            textJapan.delete('1.0', END)
            textJapan.insert('1.0', data[11])

        # korea
        if data[12] is not None:
            textKorea.delete('1.0', END)
            textKorea.insert('1.0', data[12])

        # spain
        if data[13] is not None:
            textSpain.delete('1.0', END)
            textSpain.insert('1.0', data[13])

def callbackOthersMorpho(event):
    selection = event.widget.curselection()
    if selection:
        # clear
        listboxImage.delete(0, END)
        listboxVideo.delete(0, END)
        listboxAudio.delete(0, END)

        textNote.delete('1.0', END)
        textEnglish.delete('1.0', END)
        textFrance.delete('1.0', END)
        textRussia.delete('1.0', END)
        textChinese.delete('1.0', END)
        textJapan.delete('1.0', END)
        textKorea.delete('1.0', END)
        textSpain.delete('1.0', END)
        
        # end clear
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

        # audio
        if data[5] is not None:
            aud_list = json.loads(data[5])

            for audIndex, audItem in enumerate(aud_list):
                listboxAudio.insert(audIndex + 1, audItem)

        # note
        if data[6] is not None:
            textNote.delete('1.0', END)
            textNote.insert('1.0', data[6])

        # english
        if data[7] is not None:
            textEnglish.delete('1.0', END)
            textEnglish.insert('1.0', data[7])

        # france
        if data[8] is not None:
            textFrance.delete('1.0', END)
            textFrance.insert('1.0', data[8])

        # russia
        if data[9] is not None:
            textRussia.delete('1.0', END)
            textRussia.insert('1.0', data[9])

        # chinese
        if data[10] is not None:
            textChinese.delete('1.0', END)
            textChinese.insert('1.0', data[10])

        # japan
        if data[11] is not None:
            textJapan.delete('1.0', END)
            textJapan.insert('1.0', data[11])

        # korea
        if data[12] is not None:
            textKorea.delete('1.0', END)
            textKorea.insert('1.0', data[12])

        # spain
        if data[13] is not None:
            textSpain.delete('1.0', END)
            textSpain.insert('1.0', data[13])

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

def callbackAudio(event):
    selection = event.widget.curselection()
    if selection:
        value = event.widget.get(selection[0])
        os.startfile(os.path.normpath(os.path.join('./audios/' + value)))

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
window.title("T??? ??i???n ti???ng Vi???t")

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
scrollable_frame.bind('<Enter>', bound_to_mousewheel)
scrollable_frame.bind('<Leave>', unbound_to_mousewheel)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="my_tag")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.bind(
    "<Configure>", 
    lambda e: canvas.itemconfig(
        "my_tag", width=e.width
    )
)
canvas.bind_all("<MouseWheel>", on_mousewheel)

####################################################
# pack is used to show the object in the window
tkinter.Label(scrollable_frame, text = "Ch??o m???ng ?????n v???i T??? ??i???n Ti???ng Vi???t").pack()

if os.path.isdir('./videos') is False:
    os.makedirs('./videos')

if os.path.isdir('./images') is False:
    os.makedirs('./images')

if os.path.isdir('./audios') is False:
    os.makedirs('./audios')

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

button = Button(frame_searchBar, text="T??m ki???m", command=lambda : queryKeyword(conn, userInput.get()))
button.pack(side=RIGHT)

myFont = Font(family="Times New Roman", size=14)

entry = Entry(frame_searchBar, textvariable=userInput)
entry.insert(0, "Nh???p t??? c???n t??m...")
entry.configure(font=myFont)
str_unbind = entry.bind("<Button>", lambda event: deleteText(event, entry))
entry.pack(fill=X)

# set position for word class
frame_wordClass = Frame(scrollable_frame)
frame_wordClass.pack(expand=True, padx=6, pady=4)

labelIndependent = Label(frame_wordClass, text="?????c l???p")
labelIndependent.pack(fill=X)

textIndependent = Text(frame_wordClass, height=10)
textIndependent.pack(fill=X)
textIndependent.configure(font=myFont)
textIndependent.insert("1.0", independentContent)

buttonIndependent = Button(frame_wordClass, text="C???p nh???t th??ng tin ?????c l???p", command=lambda : updateIndep(textIndependent.get("1.0", 'end-1c')))
buttonIndependent.pack(fill=X)

labelDependent = Label(frame_wordClass, text="Kh??ng ?????c l???p")
labelDependent.pack(fill=X)

textDependent = Text(frame_wordClass, height=10)
textDependent.pack(fill=X)
textDependent.configure(font=myFont)
textDependent.insert("1.0", dependentContent)

buttonDependent = Button(frame_wordClass, text="C???p nh???t th??ng tin kh??ng ?????c l???p", command=lambda : updateDep(textDependent.get("1.0", 'end-1c')))
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

labelDefinition = Label(frame_definition, text="?????nh ng??a")
labelDefinition.pack(fill=X)

textDefinition = Text(frame_definition, height=10)
textDefinition.pack(fill=X)
textDefinition.configure(font=myFont)

# buttonDefinition = Button(frame_definition, text="C???p nh???t th??ng tin ?????nh ngh??a")
# buttonDefinition.pack(fill=X)

# set position for foreign
frame_foreign = Frame(scrollable_frame)
frame_foreign.pack(fill=X, padx=6, pady=10)

labelForeign = Label(frame_foreign, text="D???ch sang ti???ng ngo???i")
labelForeign.pack(fill=X)

frame_LayoutForeignOne = Frame(frame_foreign)
frame_LayoutForeignOne.pack(expand=True, padx=6, pady=6)

# english
frame_english = Frame(frame_LayoutForeignOne)
frame_english.pack(side=LEFT, padx=10, pady=4)

labelEnglish = Label(frame_english, text="ti???ng Anh")
labelEnglish.pack(fill=X)

textEnglish = Text(frame_english, width=20, height=10)
textEnglish.pack()
textEnglish.configure(font=myFont)

buttonEnglish = Button(frame_english, text="C???p nh???t ng??n ng??? Anh", command=lambda : updateEnglishKeyword(conn, currentSelectedKeyword, textEnglish.get('1.0', 'end-1c')))
buttonEnglish.pack(fill=X)

# france
frame_france = Frame(frame_LayoutForeignOne)
frame_france.pack(side=LEFT, padx=10, pady=4)

labelFrance = Label(frame_france, text="ti???ng Ph??p")
labelFrance.pack(fill=X)

textFrance = Text(frame_france, width=20, height=10)
textFrance.pack()
textFrance.configure(font=myFont)

buttonFrance = Button(frame_france, text="C???p nh???t ng??n ng??? Ph??p", command=lambda : updateFranceKeyword(conn, currentSelectedKeyword, textFrance.get('1.0', 'end-1c')))
buttonFrance.pack(fill=X)

# russia
frame_russia = Frame(frame_LayoutForeignOne)
frame_russia.pack(side=LEFT, padx=10, pady=4)

labelRussia = Label(frame_russia, text="ti???ng Nga")
labelRussia.pack(fill=X)

textRussia = Text(frame_russia,  width=20, height=10)
textRussia.pack()
textRussia.configure(font=myFont)

buttonRussia = Button(frame_russia, text="C???p nh???t ng??n ng??? Nga", command=lambda : updateRussiaKeyword(conn, currentSelectedKeyword, textRussia.get('1.0', 'end-1c')))
buttonRussia.pack(fill=X)

# chinese
frame_chinese = Frame(frame_LayoutForeignOne)
frame_chinese.pack(side=LEFT, padx=10, pady=4)

labelChinese = Label(frame_chinese, text="ti???ng Trung")
labelChinese.pack(fill=X)

textChinese = Text(frame_chinese, width=20, height=10)
textChinese.pack()
textChinese.configure(font=myFont)

buttonChinese = Button(frame_chinese, text="C???p nh???t ng??n ng??? Trung", command=lambda : updateChineseKeyword(conn, currentSelectedKeyword, textChinese.get('1.0', 'end-1c')))
buttonChinese.pack(fill=X)

frame_LayoutForeignTwo = Frame(frame_foreign)
frame_LayoutForeignTwo.pack(expand=True, padx=6, pady=6)

# japan
frame_japan = Frame(frame_LayoutForeignTwo)
frame_japan.pack(side=LEFT, padx=10, pady=4)

labelJapan = Label(frame_japan, text="ti???ng Nh???t")
labelJapan.pack(fill=X)

textJapan = Text(frame_japan, width=20, height=10)
textJapan.pack()
textJapan.configure(font=myFont)

buttonJapan = Button(frame_japan, text="C???p nh???t ng??n ng??? Nh???t", command=lambda : updateJapanKeyword(conn, currentSelectedKeyword, textJapan.get('1.0', 'end-1c')))
buttonJapan.pack(fill=X)

# korea
frame_korea = Frame(frame_LayoutForeignTwo)
frame_korea.pack(side=LEFT, padx=10, pady=4)

labelKorea = Label(frame_korea, text="ti???ng H??n")
labelKorea.pack(fill=X)

textKorea = Text(frame_korea, width=20, height=10)
textKorea.pack()
textKorea.configure(font=myFont)

buttonKorea = Button(frame_korea, text="C???p nh???t ng??n ng??? H??n", command=lambda : updateKoreaKeyword(conn, currentSelectedKeyword, textKorea.get('1.0', 'end-1c')))
buttonKorea.pack(fill=X)

# spain
frame_spain = Frame(frame_LayoutForeignTwo)
frame_spain.pack(side=LEFT, padx=10, pady=4)

labelSpain = Label(frame_spain, text="ti???ng T??y Ban Nha")
labelSpain.pack(fill=X)

textSpain = Text(frame_spain, width=20, height=10)
textSpain.pack()
textSpain.configure(font=myFont)

buttonSpain = Button(frame_spain, text="C???p nh???t ng??n ng??? T??y Ban Nha", command=lambda : updateSpainKeyword(conn, currentSelectedKeyword, textSpain.get('1.0', 'end-1c')))
buttonSpain.pack(fill=X)

# frame for image & video
frame_ImageVideo = Frame(scrollable_frame)
frame_ImageVideo.pack(expand=True, padx=6, pady=4)

# set position for image
frame_image = Frame(frame_ImageVideo)
frame_image.pack(side=LEFT, padx=10, pady=4)

labelSelectImage = Label(frame_image, text="Ch???n h??nh ???nh c???n xem")
labelSelectImage.pack(fill=X)

listboxImage = Listbox(frame_image, height=15)
listboxImage.pack(fill=X)
listboxImage.bind("<<ListboxSelect>>", callbackImage)

buttonImage = Button(frame_image, text="C???p nh???t h??nh ???nh", command=lambda : updateImageKeyword(conn, currentSelectedKeyword))
buttonImage.pack(fill=X)

buttonDeleteImage = Button(frame_image, text="Xo?? h??nh ???nh ??ang ch???n", command=lambda : deleteImageKeyword(conn, currentSelectedKeyword))
buttonDeleteImage.pack(fill=X, pady=8)

# set position for video
frame_video = Frame(frame_ImageVideo)
frame_video.pack(side=LEFT, padx=10, pady=4)

labelSelectVideo = Label(frame_video, text="Ch???n video c???n xem")
labelSelectVideo.pack(fill=X)

listboxVideo = Listbox(frame_video, height=15)
listboxVideo.pack(fill=X)
listboxVideo.bind("<<ListboxSelect>>", callbackVideo)

buttonVideo = Button(frame_video, text="C???p nh???t video", command=lambda : updateVideoKeyword(conn, currentSelectedKeyword))
buttonVideo.pack(fill=X)

buttonDeleteVideo = Button(frame_video, text="Xo?? video ??ang ch???n", command=lambda : deleteVideoKeyword(conn, currentSelectedKeyword))
buttonDeleteVideo.pack(fill=X, pady=8)

# set position for audio
frame_audio = Frame(frame_ImageVideo)
frame_audio.pack(side=LEFT, padx=10, pady=4)

labelSelectAudio = Label(frame_audio, text="Ch???n ??m thanh c???n nghe")
labelSelectAudio.pack(fill=X)

listboxAudio = Listbox(frame_audio, height=15)
listboxAudio.pack(fill=X)
listboxAudio.bind("<<ListboxSelect>>", callbackAudio)

buttonAudio = Button(frame_audio, text="C???p nh???t ??m thanh", command=lambda : updateAudioKeyword(conn, currentSelectedKeyword))
buttonAudio.pack(fill=X)

buttonDeleteAudio = Button(frame_audio, text="Xo?? ??m thanh ??ang ch???n", command=lambda : deleteAudioKeyword(conn, currentSelectedKeyword))
buttonDeleteAudio.pack(fill=X, pady=8)

# set position for notes
frame_note = Frame(scrollable_frame)
frame_note.pack(expand=True, padx=6, pady=4)

labelNote = Label(frame_note, text="Ghi ch??")
labelNote.pack(fill=X)

textNote = Text(frame_note, height=10)
textNote.pack(fill=X)

buttonNote = Button(frame_note, text="C???p nh???t ghi ch??", command=lambda : updateNoteKeyword(conn, currentSelectedKeyword, textNote.get('1.0', 'end-1c')))
buttonNote.pack(fill=X)
####################################################

container.pack(fill=BOTH, expand=True)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=BOTH)

# Start to run window
window.mainloop()

conn.close()
print('Terminate processsing...')

