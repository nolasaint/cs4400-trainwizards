
'''

    givereview_view.py

    author:  Evan Bailey
    date:    2016-04-25
    version: 1.0

    Provides functions to display the "Give Review" window and perform
    relevant SQL queries through dbhook.

'''

import tkinter as tk
from tkinter import messagebox

def _setupGlobals(): #{
    global trainNum
    global rating
    global comment

    trainNum = tk.StringVar()
    rating   = tk.StringVar()
    comment  = tk.StringVar()
#}

def _giveReview(): #{
    import dbhook
    from gui import getUsername

    global window

    # Parse trainNum
    try:
        trainNum = int(trainNum.get())
    except:
        messagebox.showerror("Error", "Train number must be a number")
        return

    # Parse rating
    try:
        rating = float(rating.get())
    except:
        messagebox.showerror("Error", "Rating must be a number")
        return

    comment = comment.get()

    # Execute SQL query
    try:
        dbhook.addReview(trainNum, getUsername(), rating, comment)
    except:
        messagebox.showerror("Error", "Please enter a valid train number")
    
    window.destroy()
#}

def toGiveReviewWindow(): #{
    # Initialize globals for Entry objects to write to
    _setupGlobals()

    global window

    window = tk.Toplevel()
    window.title("Give Review")
    # window.geometry("640x451+334+213")

    titleText = tk.Message(window, text="Give Review")
    titleText.pack()

    trainNumLabel = tk.Label(window, text="Enter train number:")
    trainNumLabel.pack()

    trainNumEntry = tk.Entry(window, textvariable=trainNum)
    trainNumEntry.pack()

    ratingLabel = tk.Label(window, text="Rating (0-10):")
    ratingLabel.pack()

    ratingEntry = tk.Entry(window, textvariable=rating)
    ratingEntry.pack()

    commentLabel = tk.Label(window, text="Comments:")
    commentLabel.pack()

    commentEntry = tk.Entry(window, textvariable=comment)
    commentEntry.pack()

    submitButton = tk.Button(window, text="Submit", command=_giveReview)
    submitButton.pack()
#}