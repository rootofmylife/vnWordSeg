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
    listbox_oneMorpho = Listbox(window, height=20)
    listbox_oneMorpho.pack(side=LEFT)

    listbox_twoMorpho = Listbox(window, height=20)
    listbox_twoMorpho.pack(side=LEFT)

    listbox_twoReversedMorpho = Listbox(window, height=20)
    listbox_twoReversedMorpho.pack(side=LEFT)

def createWordTypeAddition(window):
    listbox_threeMorpho = Listbox(window, height=20)
    listbox_threeMorpho.pack(side=LEFT)

    listbox_fourMorpho = Listbox(window, height=20)
    listbox_fourMorpho.pack(side=LEFT)

def createDefinition(window):
    labelIndependent = Label(window, text="Định ngĩa")
    labelIndependent.pack(fill=X)

    textIndependent = Text(window, height=10)
    textIndependent.pack(fill=X)

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
