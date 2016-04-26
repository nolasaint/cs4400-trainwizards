#make reservation
from tkinter import *
from tkinter import ttk
from gui import *
import dbhook

reservation=[]

def searchTrain():
    global ticket
    ticket = {}
    global searchWin
    searchWin=Toplevel()
    Label(searchWin, text="SEARCH TRAIN").grid(row=0, columnspan=2, sticky=EW)
    Label(searchWin, text="Departs From").grid(row=1, column=0)
    Label(searchWin, text="Arrives At").grid(row=2, column=0)
    Label(searchWin, text="Departure Date").grid(row=3, column=0)

    global departVar
    departVar=StringVar()
    global arriveVar
    arriveVar=StringVar()
    global dDateStr
    global dDateDay
    global dDateMonth
    global dDateYear
    dDateDay=StringVar()
    dDateMonth=StringVar()
    dDateYear=StringVar()

    dayList=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    monthList=['01','02','03','04','05','06','07','08','09','10','11','12']
    yearList=['2016']
    
    stationList=['Cincinnati Union Terminal', 'Utica Union Station', 'Los Angeles Union Station', 'Denver Union Station', 'Amtrak Train Station', 'Chicago Union Station', 'Main Street Station', 'Baltimore Penn Station', '30th Street Station', 'Union Station', 'Grand Central Terminal'] 

    depart=ttk.Combobox(searchWin, textvariable = departVar)
    depart['values']=stationList
    depart.grid(row=1, column=1, sticky=EW)
    arrive=ttk.Combobox(searchWin, textvariable = arriveVar)
    arrive['values']=stationList
    arrive.grid(row=2, column=1, sticky=EW)
    dateFrame=Frame(searchWin)
    dateFrame.grid(row=3, column=1, sticky=EW)
    dDate1=ttk.Combobox(dateFrame, textvariable = dDateDay)
    dDate1['values']=dayList
    dDate1.grid(row=0, column=1)
    dDate2=ttk.Combobox(dateFrame, textvariable = dDateMonth)
    dDate2['values']=monthList
    dDate2.grid(row=0, column=0)
    dDate3=ttk.Combobox(dateFrame, textvariable = dDateYear)
    dDate3['values']=yearList
    dDate3.grid(row=0, column=2)
    Label(dateFrame, text='month').grid(row=2, column=0)
    Label(dateFrame, text='day').grid(row=2, column=1)
    Label(dateFrame, text='year').grid(row=2, column=2)
   
    Button(searchWin, text="Find Trains", command = findTrains).grid(row=4, columnspan=2, sticky=EW)

def findTrains():
    dbhook.setupConnection()
    dDateStr=dDateYear.get()+ '-' + dDateMonth.get() + '-' + dDateDay.get()
    departStn=dbhook.getSID(departVar.get())
    arriveStn=dbhook.getSID(arriveVar.get())
    global departs
    departs = dbhook.getDepartures(departStn, arriveStn)
    searchWin.withdraw()
    ticket['departStation']=departVar.get()
    ticket['dptStn']=departStn
    ticket['arriveStation']=arriveVar.get()
    ticket['arrStn']=arriveStn
    ticket['departDate']=dDateStr
    
    global selectDeparture
    selectDeparture=Toplevel()
    Label(selectDeparture, text="SELECT DEPARTURE").pack()
    routeFrame=Frame(selectDeparture)
    routeFrame.pack()
    Label(routeFrame, text = "Train Number", bd=2, relief=SOLID).grid(row=0, column=0)
    Label(routeFrame, text="Times and Duration", bd=2, relief=SOLID).grid(row=0, column=1, sticky=EW)
    Label(routeFrame, text="1st Class Price", bd=2, relief=SOLID).grid(row=0, column=2)
    Label(routeFrame, text="2nd Class Price", bd=2, relief=SOLID).grid(row=0, column=3)
    global trClass
    trClass=StringVar()
    if len(departs)==0:
        Label(routeFrame, text="NO ROUTES FOUND").grid(row=1, columnspan=4, sticky=EW)
    else:
        for i in range(len(departs)):
            Label(routeFrame, text=departs[i]['trainNum'], bd=1, relief=SOLID).grid(row=i+1, column=0, sticky=EW)
            Label(routeFrame, text=departs[i]['departTime']+'-'+departs[i]['arriveTime']+' total time:'+departs[i]['travelTime'], bd=1, relief=SOLID).grid(row=i+1, column=1, sticky=EW)
            Radiobutton(routeFrame, text = '$'+ str(departs[i]['firstClassPrice'])+'0', variable=trClass, value='1'+str(i), bd=1, relief=SOLID).grid(row=i+1, column=2, sticky=EW)      
            Radiobutton(routeFrame, text = '$'+ str(departs[i]['secondClassPrice'])+'0', variable=trClass, value='2'+str(i), bd=1, relief=SOLID).grid(row=i+1, column=3, sticky=EW)
    Button(selectDeparture, text='Back', command= returnToMain).pack(side=LEFT)
    Button(selectDeparture, text='Next', command=inputInfo).pack(side=RIGHT)
    

def returnToMain():
    selectDeparture.withdraw()

def inputInfo():
    selectDeparture.withdraw()
    ticket['trainNum']=departs[int(trClass.get()[-1:])]['trainNum']
    ticket['arriveTime']=departs[int(trClass.get()[-1:])]['arriveTime']
    ticket['departTime']=departs[int(trClass.get()[-1:])]['departTime']
    ticket['totalTime']=departs[int(trClass.get()[-1:])]['travelTime']
    ticket['trainClass']=int(trClass.get()[0])
    if int(trClass.get()[0])==1:
        ticket['classPrice']=departs[int(trClass.get()[-1:])]['firstClassPrice']
    else:
        ticket['classPrice']=departs[int(trClass.get()[-1:])]['secondClassPrice']
    
    global moreInfo
    moreInfo=Toplevel()
    Label(moreInfo, text='Travel Extras & Passenger Info').grid(row=0, columnspan=3, sticky=EW)
    Label(moreInfo, text="Number of Baggage").grid(row=1, column=0)
    Label(moreInfo, text="Everypassenger can bring up to 4 baggage, 2 free of charge, 2 for $30 per bag").grid(row=2, columnspan=3)
    Label(moreInfo, text='Passenger Name').grid(row=3, column=0)

    global numBags
    numBags=Spinbox(moreInfo, values=(0,1,2,3,4))
    numBags.grid(row=1, column=1)

    global fullName
    fullName=Entry(moreInfo)
    fullName.grid(row=3, column=1)

    
    

    Button(moreInfo, text='Back', command=returnToSelect).grid(row=4, column=0)
    Button(moreInfo, text='Next', command=addFinalInfo).grid(row=4, column=1)

def returnToSelect():
    moreInfo.withdraw()
    selectDeparture.deiconify()

def addFinalInfo():
    moreInfo.withdraw()
    ticket['numBags']=numBags.get()
    nameList=fullName.get().split()
    first=nameList[0]
    ticket['firstName']=first
    last=nameList[1]
    ticket['lastName']=last
    global reservation
    reservation.append(ticket)
    makeReservation()
    
def makeReservation():
    global reservePage
    reservePage=Toplevel()
    Label(reservePage, text="MAKE RESERVATION").pack()
    Label(reservePage, text="Currently Selected").pack()
    
    selection=Frame(reservePage)
    selection.pack()
    Label(selection, text = "Train Number", bd=2, relief=SOLID).grid(row=0, column=0)
    Label(selection, text="Times and Duration", bd=2, relief=SOLID).grid(row=0, column=1, sticky=EW)
    Label(selection, text="Departs From", bd=2, relief=SOLID).grid(row=0, column=2, sticky=EW)
    Label(selection, text="Arrives At", bd=2, relief=SOLID).grid(row=0, column=3, sticky=EW)
    Label(selection, text="Class", bd=2, relief=SOLID).grid(row=0, column=4, sticky=EW)
    Label(selection, text="Price", bd=2, relief=SOLID).grid(row=0, column=5, sticky=EW)
    Label(selection, text="# of Baggages", bd=2, relief=SOLID).grid(row=0, column=6, sticky=EW)
    Label(selection, text="Passenger Name", bd=2, relief=SOLID).grid(row=0, column=7, sticky=EW)        
    Label(selection, text="Remove", bd=2, relief=SOLID).grid(row=0, column=8)
    global i
    for i in range(len(reservation)):
        Label(selection, text = reservation[i]['trainNum'], bd=2, relief=SOLID).grid(row=i+1, column=0, sticky=EW)
        Label(selection, text='Date: '+reservation[i]['departDate'] + ' '+ reservation[i]['arriveTime'] + '-'+reservation[i]['departTime']+' duration:'+reservation[i]['totalTime'], bd=2, relief=SOLID).grid(row=i+1, column=1, sticky=EW)
        Label(selection, text=reservation[i]['departStation'], bd=2, relief=SOLID).grid(row=i+1, column=2, sticky=EW)
        Label(selection, text=reservation[i]['arriveStation'], bd=2, relief=SOLID).grid(row=i+1, column=3, sticky=EW)
        Label(selection, text=reservation[i]['trainClass'], bd=2, relief=SOLID).grid(row=i+1, column=4, sticky=EW)
        Label(selection, text=reservation[i]['classPrice'], bd=2, relief=SOLID).grid(row=i+1, column=5, sticky=EW)
        Label(selection, text=reservation[i]['numBags'], bd=2, relief=SOLID).grid(row=i+1, column=6, sticky=EW)
        Label(selection, text=reservation[i]['firstName']+' '+reservation[i]['lastName'], bd=2, relief=SOLID).grid(row=i+1, column=7, sticky=EW)        
        Button(selection, text="Remove", command = remove).grid(row=i+1, column=8)
    dbhook.setupConnection()
    eduCheck=dbhook.checkStudent(getUsername())
    if eduCheck:
        Label(reservePage, text="Student Discount Applied").pack()
    payment=Frame(reservePage)
    payment.pack()
    Label(payment, text="Total Cost").grid(row=0, column=0)
    global totalCost
    totalCost=1
    Label(payment, text="$"+str(totalCost), relief=SUNKEN).grid(row=0, column=1, columnspan=2, sticky=EW)
    Label(payment, text="Use Card").grid(row=1, column=0)
    cardList=dbhook.getCards(getUsername())
    shortCards=[]
    for card in cardList:
        shortCards.append(card[-4:])
    cards=Spinbox(payment, values=(shortCards))
    cards.grid(row=1, column=1)
    global cardUsed
    cardUsed=cards.get()
    Label(payment, text="(in order to add or delete cards, please see link from main page)").grid(row=1, column=2)
    Button(payment, text="Continue adding a train", command=addAnother).grid(row=2, column=0)

    Button(reservePage, text="Back", command=returnToInfo).pack(side=LEFT)
    Button(reservePage, text="Submit", command=commitReservation).pack(side=RIGHT)
    
def addAnother():
    reservePage.destroy()
    window=Toplevel
    searchTrain(window)
    
def returnToInfo():
    reservePage.withdraw()
    moreInfo.deiconify()

def commitReservation():
    global reservation
    resID=dbhook.addReservation(getUsername(), cardUsed, totalCost)
    for ticket in reservation:
        dbhook.addTicket(resID, ticket['firstName'], ticket['lastName'], ticket['trainClass'], ticket['numBags'], ticket['departDate'], ticket['classPrice'], ticket['dptStn'], ticket['arrStn'], ticket['trainNum'])
    messagebox.showinfo('Success', " the reservation ID for your order is " + str(resID))
    reservePage.destroy()
        
def remove():
    global reservation
    del reservation[i]
    makeReservation()
    
    

