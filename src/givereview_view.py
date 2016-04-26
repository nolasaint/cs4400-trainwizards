
'''

    givereview_view.py


'''

import tkinter as tk
import dbhook

def toGiveReviewWindow(): #{
    '''
        toGiveReviewWindow()

        TODO documentation
    '''

    window = tk.Toplevel()
    window.title("Give Review")

    text = tk.Message(window, text="This is some random text")
    text.pack()
#}

# Testing area
mainWindow = tk.Tk()
toGiveReviewWindow()
