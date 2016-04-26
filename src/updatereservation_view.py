from gui import *
from tkinter import *
from tkinter import ttk
import dbhook

window=Tk()

def toUpdateRes(win):
    global inputScreen
    inputScreen=Toplevel()
    Label(inputScreen, text="UPDATE RESERVATION").pack()
    frame1=Frame(inputScreen)
    frame1.pack()
    Label(frame1, text="Reservation ID").grid(row=0, column=0)
    global resID
    resID=Entry(frame1)
    resID.grid(row=0, column=1)

    Button(frame1, text="search", command=findRes).grid(row=0, column=2)
    Button(inputScreen, text="Back", command=returnToMain).pack()

def returnToMain():
    global inputScreen
    inputScreen.withdraw()

def findRes():
    dbhook.setupConnection()
    global ticks
    ticks=dbhook.getTickets(int(resID.get()))
    inputScreen.withdraw()
    global currentDisplay
    currentDisplay=Toplevel()
    Label(currentDisplay, text="UPDATE RESERVATION").pack()
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
    Button(currentDisplay, text="Back", command=goBack).pack(side=LEFT)
    Button(currentDisplay, text="Next", command=furtherUpdate).pack(side=RIGHT)
def goBack():
    global currentDisplay
    currentDisplay.withdraw()

def furtherUpdate():
    global updateView
    updateView=Toplevel()
    Label(updateView, text="UPDATE RESERVATION").pack()
    Label(updateView, text="Current Train Ticket").pack(side=LEFT)
    table1=Frame(updateView)
    table1.pack()
    Label(table1, text = "Train Number", bd=2, relief=SOLID).grid(row=0, column=1)
    Label(table1, text="Times and Duration", bd=2, relief=SOLID).grid(row=0, column=2, sticky=EW)
    Label(table1, text="Departs From", bd=2, relief=SOLID).grid(row=0, column=3, sticky=EW)
    Label(table1, text="Arrives At", bd=2, relief=SOLID).grid(row=0, column=4, sticky=EW)
    Label(table1, text="Class", bd=2, relief=SOLID).grid(row=0, column=5, sticky=EW)
    Label(table1, text="Price", bd=2, relief=SOLID).grid(row=0, column=6, sticky=EW)
    Label(table1, text="# of Baggages", bd=2, relief=SOLID).grid(row=0, column=7, sticky=EW)
    Label(table1, text="Passenger Name", bd=2, relief=SOLID).grid(row=0, column=8, sticky=EW)        
    global tickSel
    Label(table1, text = ticks[tickSel.get()]['trainNum'], bd=2, relief=SOLID).grid(row=1, column=1, sticky=EW)
    Label(table1, text='Date: '+ticks[tickSel.get()]['departDate'] + ' '+ ticks[tickSel.get()]['arriveTime'] + '-'+ticks[tickSel.get()]['departTime']+' duration:'+ticks[tickSel.get()]['travelTime'], bd=2, relief=SOLID).grid(row=1, column=2, sticky=EW)
    #Label(table1, text=ticks[tickSel.get()]['departStation'], bd=2, relief=SOLID).grid(row=1, column=3, sticky=EW)
    #Label(table1, text=ticks[tickSel.get()]['arriveStation'], bd=2, relief=SOLID).grid(row=1, column=4, sticky=EW)
    Label(table1, text=ticks[tickSel.get()]['ticketClass'], bd=2, relief=SOLID).grid(row=1, column=5, sticky=EW)
    Label(table1, text=ticks[tickSel.get()]['ticketPrice'], bd=2, relief=SOLID).grid(row=1, column=6, sticky=EW)
    Label(table1, text=ticks[tickSel.get()]['numBags'], bd=2, relief=SOLID).grid(row=1, column=7, sticky=EW)
    Label(table1, text=ticks[tickSel.get()]['firstName']+' '+ticks[tickSel.get()]['lastName'], bd=2, relief=SOLID).grid(row=1, column=8, sticky=EW)        
    global origDate
    origDate=ticks[tickSel.get()]['departDate']
    dayList=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    monthList=['01','02','03','04','05','06','07','08','09','10','11','12']
    yearList=['2016']
    dDateDay=StringVar()
    dDateMonth=StringVar()
    dDateYear=StringVar()
    pickDate=Frame(updateView)
    pickDate.pack()
    Label(pickDate, text="New Departure Date: pick MM-DD-YYYY").grid(row=0, column=0)
    dDate1=ttk.Combobox(pickDate, textvariable = dDateDay)
    dDate1['values']=dayList
    dDate1.grid(row=0, column=2)
    dDate2=ttk.Combobox(pickDate, textvariable = dDateMonth)
    dDate2['values']=monthList
    dDate2.grid(row=0, column=1)
    dDate3=ttk.Combobox(pickDate, textvariable = dDateYear)
    dDate3['values']=yearList
    dDate3.grid(row=0, column=3)
    global dDateStr
    dDateStr=dDate3.get()+ '-' + dDateMonth.get() + '-' + dDateDay.get()
    Button(pickDate, text="search availability", command=checkNewDate).grid(row=0, column=4)
    
def checkNewDate():
    
    global updateView
    Label(updateView, text="Updated Train Ticket").pack()
    table2=Frame(updateView)
    table2.pack()
    Label(table2, text = "Train Number", bd=2, relief=SOLID).grid(row=0, column=1)
    Label(table2, text="Times and Duration", bd=2, relief=SOLID).grid(row=0, column=2, sticky=EW)
    Label(table2, text="Departs From", bd=2, relief=SOLID).grid(row=0, column=3, sticky=EW)
    Label(table2, text="Arrives At", bd=2, relief=SOLID).grid(row=0, column=4, sticky=EW)
    Label(table2, text="Class", bd=2, relief=SOLID).grid(row=0, column=5, sticky=EW)
    Label(table2, text="Price", bd=2, relief=SOLID).grid(row=0, column=6, sticky=EW)
    Label(table2, text="# of Baggages", bd=2, relief=SOLID).grid(row=0, column=7, sticky=EW)
    Label(table2, text="Passenger Name", bd=2, relief=SOLID).grid(row=0, column=8, sticky=EW)
    global tickSel
    global dDateStr
    Label(table2, text = ticks[tickSel.get()]['trainNum'], bd=2, relief=SOLID).grid(row=1, column=1, sticky=EW)
    Label(table2, text='Date: '+dDateStr + ' '+ ticks[tickSel.get()]['arriveTime'] + '-'+ticks[tickSel.get()]['departTime']+' duration:'+ticks[tickSel.get()]['travelTime'], bd=2, relief=SOLID).grid(row=1, column=2, sticky=EW)
    #Label(table2, text=ticks[tickSel.get()]['departStation'], bd=2, relief=SOLID).grid(row=1, column=3, sticky=EW)
    #Label(table2, text=ticks[tickSel.get()]['arriveStation'], bd=2, relief=SOLID).grid(row=1, column=4, sticky=EW)
    Label(table2, text=ticks[tickSel.get()]['ticketClass'], bd=2, relief=SOLID).grid(row=1, column=5, sticky=EW)
    Label(table2, text=ticks[tickSel.get()]['ticketPrice'], bd=2, relief=SOLID).grid(row=1, column=6, sticky=EW)
    Label(table2, text=ticks[tickSel.get()]['numBags'], bd=2, relief=SOLID).grid(row=1, column=7, sticky=EW)
    Label(table2, text=ticks[tickSel.get()]['firstName']+' '+ticks[tickSel.get()]['lastName'], bd=2, relief=SOLID).grid(row=1, column=8, sticky=EW)

    pricingF=Frame(updateView)
    Label(pricingF, text="Change Fee").grid(row=0, column=0)
    Label(pricingF, text="50", relief=SUNKEN).grid(row=0, column=1)
    Label(pricingF, text="updated cost").grid(row=1, column=0)
    dbhook.setupConnection()
    global resID
    totalCost=dbhook.getTotalCost(int(resID.get()))
    Label(pricingF, text="updated cost").grid(row=1, column=1)

    Button(updateView, text="back", command = retireWin).pack(side=LEFT)
    Button(updateView, text="submit", command=commitUpdate).pack(side=RIGHT)

def retireWin():
    global updateView
    updateView.withdraw()

def commitUpdate():
    global resID
    global dDateStr
    #ticketID has to come from SQL, need statement
    dbhook.setTicketDate(resID.get(), ticketID, dDateStr)
    
    
    
        
    
    

toUpdateRes(window)
window.mainloop()
