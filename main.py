import tkinter
from tkinter import *

import sqlite3 

str_unbind = ""

def getHalfWindowSize(window):
    return int(window.winfo_screenwidth() / 2), int(window.winfo_screenheight() / 2)

def getCoordinate(window, width, height):
    return int((window.winfo_screenwidth() / 2) - (width / 2)), int((window.winfo_screenheight() / 2) - (height / 2))

def createMenu(window):
    # Menu
    menubar = Menu(window)

    file = Menu(menubar, tearoff=0)  
    file.add_command(label="New")  
    file.add_command(label="Open")  
    file.add_command(label="Save")  
    file.add_command(label="Save as...")  
    file.add_command(label="Close") 
    file.add_separator()  
    file.add_command(label="Exit", command=window.quit)  
    menubar.add_cascade(label="File", menu=file)

    # Adding Help Menu
    help_ = Menu(menubar, tearoff = 0)
    help_.add_command(label='About Tk', command=None)
    menubar.add_cascade(label='Help', menu=help_)

    window.config(menu=menubar)

def deleteText(event, entry):
    entry.delete(0, END)
    entry.unbind('<Button>', str_unbind)

def createSearchBar(window):
    button = Button(window, text="Tìm kiếm")
    button.pack(side=RIGHT)

    entry = Entry(window)
    entry.insert(0, "Nhập từ cần tìm...")
    str_unbind = entry.bind("<Button>", lambda event: deleteText(event, entry))
    entry.pack(fill=X)

def createWordClass(window):
    labelIndependent = Label(window, text="Độc lập")
    labelIndependent.pack(fill=X)

    textIndependent = Text(window, height=10)
    textIndependent.pack(fill=X)

    labelDependent = Label(window, text="Không độc lập")
    labelDependent.pack(fill=X)

    textDependent = Text(window, height=10)
    textDependent.pack(fill=X)

def createWordType(window):
    listboxOneMorpho = Listbox(window, height=20)
    listboxOneMorpho.pack(side=LEFT)

    listboxTwoMorpho = Listbox(window, height=20)
    listboxTwoMorpho.pack(side=LEFT)

    listboxTwoReversedMorpho = Listbox(window, height=20)
    listboxTwoReversedMorpho.pack(side=LEFT)

def createWordTypeAddition(window):
    listboxThreeMorpho = Listbox(window, height=20)
    listboxThreeMorpho.pack(side=LEFT)

    listboxFourMorpho = Listbox(window, height=20)
    listboxFourMorpho.pack(side=LEFT)

def createDefinition(window):
    labelDefinition = Label(window, text="Định ngĩa")
    labelDefinition.pack(fill=X)

    textDefinition = Text(window, height=10)
    textDefinition.pack(fill=X)

def createImage(window):
    labelSelectImage = Label(window, text="Chọn hình ảnh cần xem")
    labelSelectImage.pack(fill=X)

    labelImage = Label(window, text="Image")
    labelImage.pack(fill=X, side=LEFT)

    listboxImage = Listbox(window, height=10)
    listboxImage.pack(side=LEFT)

def createNote(window):
    labelNote = Label(window, text="Ghi chú")
    labelNote.pack(fill=X)

    textNote = Text(window, height=10)
    textNote.pack(fill=X)

def createForeign(window):
    labelForeign = Label(window, text="Ngôn ngữ khác")
    labelForeign.pack(fill=X)

    listboxForeign = Listbox(window, height=8)
    listboxForeign.pack(side=LEFT)

    textForeign = Text(window, height=10)
    textForeign.pack(side=LEFT, padx=6)


def createObjects(window):
    # pack is used to show the object in the window
    tkinter.Label(window, text = "Chào mừng đến với Từ điển Tiếng Việt").pack()

    # Set position for search bar
    frame_searchBar = Frame(window, relief=RAISED)
    frame_searchBar.pack(fill=X, padx=6, pady=4)

    createSearchBar(frame_searchBar)

    # set position for word class
    frame_wordClass = Frame(window)
    frame_wordClass.pack(fill=X, padx=6, pady=4)

    createWordClass(frame_wordClass)

    # set position for word type
    frame_wordType = Frame(window)
    frame_wordType.pack(expand=True, padx=6, pady=4)

    createWordType(frame_wordType)

    # set position for word type
    frame_wordTypeAddition = Frame(window)
    frame_wordTypeAddition.pack(expand=True, padx=6, pady=4)

    createWordTypeAddition(frame_wordTypeAddition)

    # set position for definition
    frame_definition = Frame(window)
    frame_definition.pack(fill=X, padx=6, pady=4)

    createDefinition(frame_definition)

    # set position for image
    frame_image = Frame(window)
    frame_image.pack(expand=True, padx=6, pady=4)

    createImage(frame_image)

    # set position for notes
    frame_note = Frame(window)
    frame_note.pack(expand=True, padx=6, pady=4)

    createNote(frame_note)

    # set position for foreign
    frame_foreign = Frame(window)
    frame_foreign.pack(expand=True, padx=6, pady=6)

    createForeign(frame_foreign)

def main():
    # create a tkinter window
    window = tkinter.Tk()

    width, height = getHalfWindowSize(window)
    x, y = getCoordinate(window, width, height)

    # Open window having dimension 100x100
    window.geometry(f'{width}x{height}+{x}+{y}')

    # to rename the title of the window
    window.title("Từ điển tiếng Việt")

    createMenu(window)

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

    createObjects(scrollable_frame)

    container.pack(fill=BOTH, expand=True)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=BOTH)

    # Start to run window
    window.mainloop()

if __name__ == '__main__':
    print('Starting to pre-processing...')
    main()
    print('Terminate processsing...')
