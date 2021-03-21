import tkinter

def getHalfWindowSize(window):
    return int(window.winfo_screenwidth() / 2), int(window.winfo_screenheight() / 2)

def getCoordinate(window, width, height):
    return int((window.winfo_screenwidth() / 2) - (width / 2)), int((window.winfo_screenheight() / 2) - (height / 2))

def createObjects(window):
    # pack is used to show the object in the window
    label = tkinter.Label(window, text = "Welcome to DataCamp's Tutorial on Tkinter!").pack()


def main():
    # create a tkinter window
    window = tkinter.Tk()

    width, height = getHalfWindowSize(window)
    x, y = getCoordinate(window, width, height)
    print(x)
    print(y)

    # Open window having dimension 100x100
    window.geometry(f'{width}x{height}+{x}+{y}')

    # to rename the title of the window
    window.title("Tách từ")

    createObjects(window)

    # Start to run window
    window.mainloop()

if __name__ == '__main__':
    print('Starting to pre-processing...')
    main()
    print('Terminate processsing...')
