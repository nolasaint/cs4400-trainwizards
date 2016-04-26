
'''
  
    managecards_view.py

    author:  Evan Bailey
    date:    2016-04-24
    version: 1.0

    Provides functions to display the "Manage Cards" window and perform
    relevant SQL queries through dbhook.

'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def _setupGlobals(): #{
    global _cardNum
    global _ccv
    global _name
    global _expireM
    global _expireY

    _cardNum = tk.StringVar()
    _ccv     = tk.StringVar()
    _name    = tk.StringVar()
    _expireM = tk.StringVar()
    _expireY = tk.StringVar()
#}

def _addCard(): #{
    import dbhook
    from gui import getUsername

    global addWindow

    # Parse cardNum
    cardNum = _cardNum.get()
    if (len(cardNum) != 16):
        messagebox.showerror("Error", "Card number must be 16 digits")
        return
    try:
        int(cardNum)
    except:
        messagebox.showerror("Error", "Card number must be a number")
        return

    # Parse ccv
    try:
        ccv = int(_ccv.get())
    except:
        messagebox.showerror("Error", "ccv must be a number")
        return

    name = _name.get()
    expireDate = _expireY.get() + "-" + _expireM.get() + "-01"

    # Execute SQL query
    try:
        dbhook.addCard(cardNum, ccv, name, expireDate)
    except:
        # If the card already exists in the database, an exception occurs
        None
    
    try:
        dbhook.setOwnership(getUsername(), cardNum)
    except:
        print("Username is ", getUsername())
        # Shouldn't be reached, since the first try block should ensure card exists
        print("For some reason, an exception was encountered")

    addWindow.destroy()
#}

def _delCard(): #{
    import dbhook
    from gui import getUsername

    global delWindow

    # Parse cardNum
    cardNum = _cardNum.get()
    if (len(cardNum) != 16):
        messagebox.showerror("Error", "Card number must be 16 digits")
        return
    try:
        int(cardNum)
    except:
        messagebox.showerror("Error", "Card number must be a number")
        return

    # Execute SQL query
    try:
        dbhook.deleteCard(getUsername(), cardNum)
    except:
        None

    delWindow.destroy()
#}

def _addCardWindow(): #{
    global addWindow

    addWindow = tk.Toplevel()
    addWindow.title("Add new card")

    cardNumLabel = tk.Label(addWindow, text="Enter card number:")
    cardNumLabel.pack()

    cardNumEntry = tk.Entry(addWindow, textvariable=_cardNum)
    cardNumEntry.pack()

    ccvLabel = tk.Label(addWindow, text="Enter ccv:")
    ccvLabel.pack()

    ccvEntry = tk.Entry(addWindow, textvariable=_ccv)
    ccvEntry.pack()

    nameLabel = tk.Label(addWindow, text="Enter cardholder name:")
    nameLabel.pack()

    nameEntry = tk.Entry(addWindow, textvariable=_name)
    nameEntry.pack()

    # For the Combobox objects
    years = ["2016", "2017", "2018", "2019", "2020"]
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    expireDateLabel = tk.Label(addWindow, text="Expire Month/Year:")
    expireDateLabel.pack()

    expireMCombobox = ttk.Combobox(addWindow, values=months, textvariable=_expireM)
    expireMCombobox.pack()

    expireYCombobox = ttk.Combobox(addWindow, values=years, textvariable=_expireY)
    expireYCombobox.pack()

    addCardButton = tk.Button(addWindow, text="Add card", command=_addCard)
    addCardButton.pack()
#}

def _delCardWindow(): #{
    global delWindow

    delWindow = tk.Toplevel()
    delWindow.title("Delete a card")

    cardNumLabel = tk.Label(delWindow, text="Enter card number:")
    cardNumLabel.pack()

    cardNumEntry = tk.Entry(delWindow, textvariable=_cardNum)
    cardNumEntry.pack()

    deleteCardButton = tk.Button(delWindow, text="Delete card", command=_delCard)
    deleteCardButton.pack()
#}

def toManageCardsWindow(): #{
    # Initialize globals for Entry objects to write to
    _setupGlobals()

    window = tk.Toplevel()
    window.title("Manage Cards")

    titleText = tk.Message(window, text="Manage Cards")
    titleText.pack()

    addCardWindowButton = tk.Button(window, text="Add new card", command=_addCardWindow)
    addCardWindowButton.pack()

    delCardWindowButton = tk.Button(window, text="Delete a card", command=_delCardWindow)
    delCardWindowButton.pack()
#}