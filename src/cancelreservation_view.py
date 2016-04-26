from gui import *
from tkinter import *
import dbhook
import datetime

window=Tk()

def toCancelRes(win):
    global inputRID
    inputRID=Toplevel()
    Label(inputRID, text="CANCEL RESERVATION").pack()
    frame1=Frame(inputRID)
    frame1.pack()
    Label(frame1, text="Reservation ID").grid(row=0, column=0)
    global resID
    resID=Entry(frame1)
    resID.grid(row=0, column=1)

    Button(frame1, text="search", command=findResC).grid(row=0, column=2)
    Button(inputRID, text="Back", command=returnToMain).pack()

def returnToMain():
    global inputRID
    inputRID.withdraw()

def findResC():
    dbhook.setupConnection()
    global ticks
    ticks=dbhook.getTickets(int(resID.get()))
    inputRID.withdraw()
    global currentDisplay
    currentDisplay=Toplevel()
    Label(currentDisplay, text="CANCEL RESERVATION").pack()
    table=Frame(currentDisplay)
    table.pack()
    Label(table, text = "Train Number", bd=2, relief=SOLID).grid(row=0, column=1)
    Label(table, text="Times and Duration", bd=2, relief=SOLID).grid(row=0, column=2, sticky=EW)
    Label(table, text="Departs From", bd=2, relief=SOLID).grid(row=0, column=3, sticky=EW)
    Label(table, text="Arrives At", bd=2, relief=SOLID).grid(row=0, column=4, sticky=EW)
    Label(table, text="Class", bd=2, relief=SOLID).grid(row=0, column=5, sticky=EW)
    Label(table, text="Price", bd=2, relief=SOLID).grid(row=0, column=6, sticky=EW)
    Label(table, text="# of Baggages", bd=2, relief=SOLID).grid(row=0, column=7, sticky=EW)
    Label(table, text="Passenger Name", bd=2, relief=SOLID).grid(row=0, column=8, sticky=EW)        
    Label(table, text="Select", bd=2, relief=SOLID).grid(row=0, column=0)
    global tickSel
    tickSel=IntVar()
    for i in range(len(ticks)):
        Label(table, text = ticks[i]['trainNum'], bd=2, relief=SOLID).grid(row=i+1, column=1, sticky=EW)
        Label(table, text='Date: '+ticks[i]['departDate'] + ' '+ ticks[i]['arriveTime'] + '-'+ticks[i]['departTime']+' duration:'+ticks[i]['travelTime'], bd=2, relief=SOLID).grid(row=i+1, column=2, sticky=EW)
        #Label(table, text=ticks[i]['departStation'], bd=2, relief=SOLID).grid(row=i+1, column=3, sticky=EW)
        #Label(table, text=ticks[i]['arriveStation'], bd=2, relief=SOLID).grid(row=i+1, column=4, sticky=EW)
        Label(table, text=ticks[i]['ticketClass'], bd=2, relief=SOLID).grid(row=i+1, column=5, sticky=EW)
        Label(table, text=ticks[i]['ticketPrice'], bd=2, relief=SOLID).grid(row=i+1, column=6, sticky=EW)
        Label(table, text=ticks[i]['numBags'], bd=2, relief=SOLID).grid(row=i+1, column=7, sticky=EW)
        Label(table, text=ticks[i]['firstName']+' '+ticks[i]['lastName'], bd=2, relief=SOLID).grid(row=i+1, column=8, sticky=EW)        
        Radiobutton(table, variable=tickSel, value=i).grid(row=i+1, column=0)
    frameA=Frame(currentDisplay)
    frameA.pack()
    Label(frameA, text="Total Cost of Reservation").grid(row=0, column=0)
    Label(frameA, text="Date of Cancellation").grid(row=1, column=0)
    Label(frameA, text="Amount to be Refunded").grid(row=2, column=0)
    cost=dbhook.getTotalCost(int(resID.get()))
    Label(frameA, text=str(cost), relief=SUNKEN).grid(row=0, column=1)
    Label(frameA, text=str(datetime.date.today()), relief=SUNKEN).grid(row=1, column=1)
    #need to calculate different costs based on distance from departure date    
    refundCost=.5*cost
    Label(frameA, text=str(refundCost), relief=SUNKEN).grid(row=2, column=1)
    
    
    Button(currentDisplay, text="Back", command=goBack).pack(side=LEFT)
    Button(currentDisplay, text="Submit", command=cancelRes).pack(side=RIGHT)

def goBack():
    currentDisplay.withdraw()

def cancelRes():
    dbhook.setCancelled(resID.get())
    



toCancelRes(window)
window.mainloop()
