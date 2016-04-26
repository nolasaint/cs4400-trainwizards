from tkinter import *
import pymysql
import givereview_view
import managecards_view
import dbhook

userName=""
    

class GTtrain:
    def __init__(self, window):
        self.window = window
        dbhook.setupConnection()
        self.toLoginWin()
        
    

    def toLoginWin(self):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font10 = "-family {DejaVu Sans} -size 20 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"

        self.window.geometry("640x451+334+213")
        self.window.title("GT Train")
        self.window.configure(highlightcolor="black")



        self.loginScreen = Frame(self.window)
        self.loginScreen.place(relx=0.02, rely=0.0, relheight=0.94
                , relwidth=0.96)
        self.loginScreen.configure(relief=GROOVE)
        self.loginScreen.configure(borderwidth="2")
        self.loginScreen.configure(relief=GROOVE)
        self.loginScreen.configure(width=615)

        Label(self.loginScreen, text="LOGIN").pack()

        self.loginbutton = Button(self.loginScreen, command = self.checkLogin)
        self.loginbutton.place(relx=0.36, rely=0.54, height=26, width=59)
        self.loginbutton.configure(activebackground="#d9d9d9")
        self.loginbutton.configure(text='''Login''')

        self.regbutton = Button(self.loginScreen, command = self.toRegisterWin)
        self.regbutton.place(relx=0.54, rely=0.54, height=26, width=75)
        self.regbutton.configure(activebackground="#d9d9d9")
        self.regbutton.configure(text='''Register''')

        self.Entryusr = Entry(self.loginScreen)
        self.Entryusr.place(relx=0.36, rely=0.28, relheight=0.06, relwidth=0.33)
        self.Entryusr.configure(background="white")
        self.Entryusr.configure(font="TkFixedFont")
        self.Entryusr.configure(selectbackground="#c4c4c4")

        self.Entrypwd = Entry(self.loginScreen)
        self.Entrypwd.place(relx=0.36, rely=0.4, relheight=0.06, relwidth=0.33)
        self.Entrypwd.configure(background="white")
        self.Entrypwd.configure(font="TkFixedFont")
        self.Entrypwd.configure(selectbackground="#c4c4c4")

        self.Label1 = Label(self.loginScreen)
        self.Label1.place(relx=0.24, rely=0.28, height=18, width=65)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Username''')

        self.Label2 = Label(self.loginScreen)
        self.Label2.place(relx=0.24, rely=0.41, height=18, width=60)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''Password''')
        dbhook.setupConnection()
        
    def checkLogin(self):
        self.user=self.Entryusr.get()
        global userName
        userName=self.Entryusr.get()
        pswd=self.Entrypwd.get()
        if dbhook.checkLogin(self.user, pswd):
            if dbhook.checkManager(self.user):
                pass
            else:
                self.toCustWin()
        else:
            messagebox.showerror('Error', 'Invalid Username and/or Password')


    def toCustWin(self):
        self.loginScreen.destroy()

        self.customerFuncs = Frame(self.window)
        self.customerFuncs.place(relx=0.05, rely=0.02, relheight=0.88
                , relwidth=0.88)
        self.customerFuncs.configure(relief=GROOVE)
        self.customerFuncs.configure(borderwidth="2")
        self.customerFuncs.configure(relief=GROOVE)
        self.customerFuncs.configure(width=565)

        self.Button1 = Button(self.customerFuncs)
        self.Button1.place(relx=0.32, rely=0.13, height=26, width=152)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''View train Schedules''')

        self.Button2 = Button(self.customerFuncs)
        self.Button2.place(relx=0.32, rely=0.23, height=26, width=172)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(text='''Make a New Reservation''')

        self.Button5 = Button(self.customerFuncs)
        self.Button5.place(relx=0.32, rely=0.33, height=26, width=155)
        self.Button5.configure(activebackground="#d9d9d9")
        self.Button5.configure(text='''Update a Reservation''')

        self.Button6 = Button(self.customerFuncs)
        self.Button6.place(relx=0.32, rely=0.43, height=26, width=152)
        self.Button6.configure(activebackground="#d9d9d9")
        self.Button6.configure(text='''Cancel A Reservation''')

        self.Button7 = Button(self.customerFuncs, command = givereview_view.toGiveReviewWindow)
        self.Button7.place(relx=0.32, rely=0.53, height=26, width=98)
        self.Button7.configure(activebackground="#d9d9d9")
        self.Button7.configure(text='''Give Review''')

        self.Button8 = Button(self.customerFuncs, command=self.addStudent)
        self.Button8.place(relx=0.32, rely=0.63, height=26, width=130)
        self.Button8.configure(activebackground="#d9d9d9")
        self.Button8.configure(text='''Add Student Info''')
        
        self.Button9 = Button(self.customerFuncs, command=managecards_view.toManageCardsWindow)
        self.Button9.place(relx=0.32, rely=0.63, height=26, width=130)
        self.Button9.configure(activebackground="#d9d9d9")
        self.Button9.configure(text='''Manage Cards''')

        self.logoutbutton = Button(self.customerFuncs, command = self.logout)
        self.logoutbutton.place(relx=0.67, rely=0.81, height=26, width=68)
        self.logoutbutton.configure(activebackground="#d9d9d9")
        self.logoutbutton.configure(text='''Logout''')
        
        

    def addStudent(self):
        self.window.withdraw()

        self.add=Toplevel()
        Label(self.add, text="ADD SCHOOL INFO").grid(row=0, columnspan=2, sticky=EW)
        Label(self.add, text="School Email Address").grid(row=1, column=0)
        Label(self.add, text="your school email address ends with .edu").grid(row=2, columnspan=2, sticky=E)
        self.schoolE=Entry(self.add)
        self.schoolE.grid(row=1, column=1)

        Button(self.add, text = "Back", command=self.transitionOut).grid(row=3, column=0)
        Button(self.add, text = "Submit", comman=self.insertStudent).grid(row=3, column=1)

    def transitionOut(self):
        self.add.destroy()
        self.gotoMain()

    def insertStudent(self):
        if self.schoolE.get()[-3:]=="edu":
            dbhook.setStudent(self.user)
            self.add.destroy()
            self.gotoMain()
        else:
            messagebox.showerror('Error', 'School email must end in .edu')
    
    def gotoMain(self):
        self.window.deiconify()
        
    def toRegisterWin(self):
        self.loginScreen.destroy()
        self.window.withdraw()

        self.register=Toplevel()

        Label(self.register, text = "NEW USER REGISTRATION").grid(row=0, columnspan =2, sticky=EW)
        Label(self.register, text = "Username").grid(row=1, column=0)
        Label(self.register, text = "Email Address").grid(row=2, column=0)
        Label(self.register, text = "Password").grid(row=3, column=0)
        Label(self.register, text = "Confirm Password").grid(row=4, column=0)

        self.user = Entry(self.register)
        self.user.grid(row=1, column=1)
        self.email = Entry(self.register)
        self.email.grid(row=2, column=1)
        self.pswd = Entry(self.register)
        self.pswd.grid(row=3, column=1)
        self.cpswd = Entry(self.register)
        self.cpswd.grid(row=4, column=1)

        Button(self.register, text="Create", command = self.createUser).grid(row=5, columnspan=2, sticky=EW)
        
        
    def createUser(self):
        if self.pswd.get()==self.cpswd.get():
            try:
                dbhook.addCustomer(self.user.get(), self.pswd.get(), self.email.get())
                self.window.deiconify()
                self.register.withdraw()
                self.toLoginWin()
            except:
                messagebox.showerror('Error', 'That Username is already taken')
        else:
            messagebox.showerror('Error', 'Passwords do not match')

    def logout(self):
        self.window.destroy()
        
        

def getUsername():
    return userName
def setUsername(_userName):
    global userName
    userName= _userName

        

