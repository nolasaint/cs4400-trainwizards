
'''
train_view.py

pulls up train schedule

'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dbhook import *

def _setupGlobals(): #{
    global _trainnum


    _trainnum = tk.StringVar()
#}

#trainview: generates window to enter find trains
#must have global vars
def trainview(): #{
	_setupGlobals()
	
	addWindow = tk.Toplevel()
	
	addWindow.title("View Trains")
	
	Label1 = tk.Label(addWindow, text="Search Train#")
	Label1.pack()
	
	trainEntry = tk.Entry(addWindow, textvariable=_trainnum)
	trainEntry.pack()
	
	searchbutton = tk.Button(addWindow, text="Find", command=findtrain)
	searchbutton.pack()

def findtrain():
	train=_trainnum.get()
	setupConnection()
	sch=getSchedule(train)
	
	global found
	found=tk.Toplevel()
	routeFrame=tk.Frame(found)
	routeFrame.pack()
	tk.Label(routeFrame, text="Train #").grid(row=0, column=0)
	tk.Label(routeFrame, text="Arrive time").grid(row=0, column=1)
	tk.Label(routeFrame, text="Depart time").grid(row=0, column=2)
	tk.Label(routeFrame, text="Station").grid(row=0, column=3)

	for i in range(len(sch)):
            tk.Label(routeFrame, text=sch[i]['trainNum']).grid(row=i+1, column=0)
            tk.Label(routeFrame, text=sch[i]['arriveTime']).grid(row=i+1, column=1)
            tk.Label(routeFrame, text=sch[i]['departTime']).grid(row=i+1, column=2)
            tk.Label(routeFrame, text=sch[i]['stationName']).grid(row=i+1, column=3)
			
	
	
#[{'arriveTime': '10:45:00', 'stationName': 'Cincinnati Union Terminal', 'trainNum': 1111, 'departTime': '08:30:00'}, {'arriveTime': '14:00:00', 'stationName': 'Union Station', 'trainNum': 1111, 'departTime': '11:00:00'}]


    



#root = tk.Tk()
#mainwindow = trainview()
#root.mainloop()
