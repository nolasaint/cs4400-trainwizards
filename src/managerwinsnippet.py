    def toManagerWin(self):
        self.loginScreen.destroy()

        self.mgrFuncs=Frame(self.window)

		self.Labelmgr = Label(self.mgrFuncs)
		self.Labelmgr.place(relx=0.18, rely=0.09, height=33, width=283)
		self.Labelmgr.configure(font=font10)
		self.Labelmgr.configure(text='''Manager Functionality''')
	
		self.Button1 = Button(self.mgrFuncs, command=self.revreport)
		self.Button1.place(relx=0.3, rely=0.22, height=26, width=151)
		self.Button1.configure(activebackground="#d9d9d9")
		self.Button1.configure(text='''View revenue Report''')
	
		self.Button2 = Button(self.mgrFuncs, command=self.poproutereport)
		self.Button2.place(relx=0.3, rely=0.33, height=26, width=186)
		self.Button2.configure(activebackground="#d9d9d9")
		self.Button2.configure(text='''View Popular Route Report''')
	
		self.Button3 = Button(self.logout)
		self.Button3.place(relx=0.3, rely=0.44, height=26, width=68)
		self.Button3.configure(activebackground="#d9d9d9")
		self.Button3.configure(text='''Logout''')
