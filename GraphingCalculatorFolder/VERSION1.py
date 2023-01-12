from tkinter import *
from tkinter import ttk
import math
import numpy as np
from numpy import *
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.pyplot import ylim
from datetime import datetime
import time
from datetime import date
import collections

conn = sqlite3.connect("GRAPHINGDATABASEFINAL.db")
cursor = conn.cursor()

Xax = -10
Yax = 10
numbers = ["1","2","3","4","5","6","7","8","9","0",1,2,3,4,5,6,7,8,9,0]

class window():
	def __init__(self,master):
		self.master = master
		self.master.geometry("330x250")
		self.master.title("Graphing calculator")
	
		menu = Menu(self.master)
		self.master.config(menu=menu)

		settings = Menu(menu)
		file = Menu(menu)
		assistance = Menu(menu)
		
		menu.add_cascade(label="Settings",menu=settings)
		settings.add_command(label="Delete account",command=self.delete_user)
		settings.add_command(label="Exit",command=self.client_Exit)
		menu.add_cascade(label="Help",menu=assistance)
		assistance.add_command(label="Input help",command=self.HELP)

		self.USername= Label(self.master,text ="Username:")
		self.USername.pack()
		self.USername.place(x=0,y=0)
		self.password = Label(self.master,text = "Password:")
		self.password.pack()
		self.password.place(x=0,y=30)

		self.UsernameInput = Entry(self.master,bd=3)
		self.UsernameInput.pack()
		self.UsernameInput.place(x=60,y=0)
		self.Passwordinput = Entry(self.master,bd=3,show="*")
		self.Passwordinput.pack()
		self.Passwordinput.place(x=60,y=30)
			
		self.NewAccount = Label(self.master,text = "Create a new account:")
		self.NewAccount.pack()
		self.NewAccount.place(x=60,y=70)
		self.Name = Label(self.master,text = "Full Name:")
		self.Name.pack()
		self.Name.place(x=0,y=90)
		self.NewUsername = Label(self.master,text = "Username:")
		self.NewUsername.pack()
		self.NewUsername.place(x=0,y=120)
		self.NewPassword = Label(self.master,text = "Password:")
		self.NewPassword.pack()
		self.NewPassword.place(x=0,y=150)
		self.NewPassword2 = Label(self.master,text = "Password:")
		self.NewPassword2.pack()
		self.NewPassword2.place(x=0,y=180)

		self.Nameinput = Entry(self.master,bd=3)
		self.Nameinput.pack()
		self.Nameinput.place(x=60,y=90)
		self.NewUsernameinput = StringVar()
		self.myNewUsername = Entry(self.master,textvariable=self.NewUsernameinput, bd=3)
		self.myNewUsername.pack()
		self.myNewUsername.place(x=60,y=120)
		self.NewPasswordinput = StringVar()
		self.myPasswordinput= Entry(self.master,textvariable=self.NewPasswordinput, bd=3,show="*")
		self.myPasswordinput.pack()
		self.myPasswordinput.place(x=60,y=150)
		self.NewPassword2input = Entry(self.master,bd=3,show="*")
		self.NewPassword2input.pack()
		self.NewPassword2input.place(x=60,y=180)

		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=200,y=210)

		def sign_in():
			global Allow
			Allow = False
			print("signing in")
			global Username
			Username = self.UsernameInput.get()
			Password = self.Passwordinput.get()
			print(Username,Password)
			cursor = conn.cursor()
			sql_query = ("""SELECT
						Username,
						Password
						FROM UserTable
					""")
			cursor.execute(sql_query) 
			data = cursor.fetchall()
			print(data)
		
			UsernameAllow = False
			PasswordAllow = False
			for i in range(len(data)):
				password_database = data[i][1]
				username_database = data[i][0]
				if username_database == Username:
					print("Username is correct")
					UsernameAllow = True
					if password_database == Password:
						print("Passsword is correct")
						PasswordAllow = True
					else:
						print("password is incorrect")
						ErrorLabel = Label(self.master, text="Password details not recognised",fg="red")
						ErrorLabel.pack()
						ErrorLabel.place(x=60,y=50)

			if UsernameAllow == False:
				print("username is not correct")
				ErrorLabel = Label(self.master, text="Login details not recognised",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=60,y=50)
			
			if UsernameAllow == True and PasswordAllow == True:
				Allow = True
				print("in")
				ErrorLabel = Label(self.master, text="Login details correct",fg="green")
				ErrorLabel.pack()
				ErrorLabel.place(x=60,y=50)
				root2 = Toplevel(self.master)
				SignIn(root2)
							
		self.Sign_in = Button(self.master,text="  Sign in  ",command=sign_in)
		self.Sign_in.place(x=200,y=10)

		def get_entry():
			enter = False
			copyCheck = False
			getNameinput = self.Nameinput.get()
			getNewUsernameinput = self.NewUsernameinput.get()
			getNewPassword = self.NewPasswordinput.get()
			getNewPassword2 = self.NewPassword2input.get()
			cursor = conn.cursor()
			sql_query = ("""SELECT
						Username,
						FullName
						FROM UserTable
					""")
			cursor.execute(sql_query)
			data = cursor.fetchall()

			if getNameinput == "":
				self.allowIn = Label(self.master,text="Please enter a Name",fg="red",borderwidth=3)
				self.allowIn.pack()
				self.allowIn.place(x=190,y=90)
				enter = False

			if getNewUsernameinput == "":
				self.allowIn = Label(self.master,text="Please enter a Username",fg="red")
				self.allowIn.pack()
				self.allowIn.place(x=190,y=120)
				enter = False

			if getNewPassword == "":
				self.allowIn = Label(self.master,text="Please enter a Password",fg="red")
				self.allowIn.pack()
				self.allowIn.place(x=190,y=150)
				enter = False

			if getNewPassword2 == "":
				self.allowIn = Label(self.master,text="Please enter a Password",fg="red")
				self.allowIn.pack()
				self.allowIn.place(x=190,y=180)
				enter = False

			if getNewPassword != getNewPassword2:
				self.ErrorLabel = Label(self.master, text="The passwords do not match\n Try again",fg="red")
				self.ErrorLabel.pack()
				self.ErrorLabel.place(x=60,y=50)
				enter = False

			for i in range(len(data)):
				Username_database = data[i][0]
				FullName_database = data[i][1]

				if Username_database == getNewUsernameinput:
					copyCheck = True
					print("this check is working")
					self.UsernameError = Label(self.master, text="The Username already has an account in the database",fg="red")
					self.UsernameError.pack()
					self.UsernameError.place(x=40,y=50)

				if FullName_database == getNameinput:
					copyCheck = True
					print("this check is working")
					self.NameError = Label(self.master, text="This Name already has an account in the database",fg="red")
					self.NameError.pack()
					self.NameError.place(x=40,y=50)
						
			if getNameinput != "" and getNewUsernameinput != "" and  getNewPassword != "" and  getNewPassword2 != "" and copyCheck == False:
				enter = True

			if getNewPassword == getNewPassword2 and enter == True :
				def insert(values):
					self.allowIn = Label(self.master,text="Account added to the database",fg="green")
					self.allowIn.pack()
					self.allowIn.place(x=60,y=50)
					sql = "insert into UserTable (Username,Fullname,Password) values (?,?,?)"
					cursor.execute(sql,values)
					conn.commit()
					cursor.close()

				if __name__ == "__main__":
					Product =  getNewUsernameinput
					Fullname = getNameinput
					Password = getNewPassword
					product = (Product,Fullname,Password)
					insert(product)
									
		self.Create_Account = Button(self.master,text="Create new account",command=get_entry)
		self.Create_Account.place(x=60,y=210)
	
	def client_Exit(self):
		self.master.destroy()

	def HELP(self):
		print("help menu")
		help = Toplevel(self.master)
		HelpGUI = Help(help)

	def delete_user(self):
		print("delete user")
		delete = Toplevel(self.master)
		deleteGUI = Delete_user(delete)

class Delete_user():
	def __init__(self,master):
		self.master = master
		self.master.geometry("250x150")	
		self.master.title("Delete user")

		self.close_window = Button(self.master,text="close window",command=self.master.destroy,fg="red")
		self.close_window.pack()
		self.close_window.place(x=120,y=100)

		self.enter_label = Label(self.master,text="Enter the Administrator password\n to go to the delete tab window")
		self.enter_label.pack()
		self.enter_label.place()

		self.Admin_passwordinput = Entry(self.master,bd=3,show="*")
		self.Admin_passwordinput.pack()
		self.Admin_passwordinput.place(x=100,y=35)

		self.Admin_passwordlabel = Label(self.master,text="Admin password:")
		self.Admin_passwordlabel.pack()
		self.Admin_passwordlabel.place(x=0,y=30)

		def check_if_true():
			AdminPassword = self.Admin_passwordinput.get()
			print("got input")
			if AdminPassword == "1234":
				print("input is correct")
				delete = Toplevel(self.master)
				deleteGUI = Delete(delete)
			else:
				ErrorLabel = Label(self.master, text="Details not recognised",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=0,y=130)

		self.GoToCheck = Button(self.master,text="go to delete Tab",command=check_if_true)
		self.GoToCheck.pack()
		self.GoToCheck.place(x=120,y=70)

class Delete():
	def __init__(self,master):
		self.master = master
		self.master.geometry("250x150")
		self.master.title("Delete User")
		
		self.UsernametoDeleteInput = Entry(self.master,bd=3)
		self.UsernametoDeleteInput.pack()
		self.UsernametoDeleteInput.place(x=80,y=40)

		self.Warning = Label(self.master, text ="WARNING YOU ARE ABOUT TO DELETE A USER",fg="red")
		self.Warning.pack()

		self.viewAll = Button(self.master,text="View all users",command=self.ViewAll)
		self.viewAll.pack()
		self.viewAll.place(x=5,y=70)

		self.UsernametoDeletelabel = Label(self.master,text="Username:")
		self.UsernametoDeletelabel.pack()
		self.UsernametoDeletelabel.place(x=10,y=40)

		self.Delete = Button(self.master, text="Delete User from database",command=self.delete_Accounthalf)
		self.Delete.pack()
		self.Delete.place(x=100,y=70)

		self.close_window = Button(self.master,text="close window",command=self.master.destroy,fg="red")
		self.close_window.pack()
		self.close_window.place(x=90,y=100)

	def ViewAll(self):
		view = Toplevel(self.master)
		viewGUI = DsiplayUsers(view)

	def delete_Accounthalf(self):
		Username_databaseArray = []
		Username = self.UsernametoDeleteInput.get()
		cursor = conn.cursor()
		 
		sql_query = ("""SELECT
					Username,
					FullName
					FROM UserTable
				""")
		cursor.execute(sql_query)
		data = cursor.fetchall()
		print(data)

		for i in range(len(data)):
			Username_databaseArray.append(data[i][0])
			
		if Username in Username_databaseArray:
			self.Done = Label(self.master,text="User deleted successfully    ",fg="green")
			self.Done.pack()
			self.Done.place(x=0,y=130)
			def delete_Account():
				print(Username)
				print("connected to sqlite3")
				cursor.execute("SELECT UserID FROM UserTable WHERE Username=?",(Username))
				UserID_2 = cursor.fetchone()
				cursor.execute("""DELETE FROM OccurancesTable WHERE UserID_2=?""",(UserID_2))
				sql_query_delete = """DELETE FROM UserTable WHERE Username=?  """
				cursor.execute(sql_query_delete,(Username,))
				query = """DELETE FROM EquationTable WHERE Username=?"""
				cursor.execute(query,(Username,))
				conn.commit()
				print("record deleted")
				cursor.close()
			delete_Account()
		else:
			ErrorLabel = Label(self.master, text="User details not recognised",fg="red")
			ErrorLabel.pack()
			ErrorLabel.place(x=0,y=130)

class Help():
	def __init__(self,master):
		self.master = master
		self.master.geometry("800x170")

		self.Input = Label(self.master,text="If you have a variable to a power, input it like this: x^n where n is any real number\nyou can also graph multiple equations by entering each equation individually and then selecting the graph button\nIf using trigonometric functions input them normally\n1. choose the polynomial degree\n2. enter equation in descending powers of x\n3. even if positive enter the plus sign before the digit\n4. only place negative sign if first variable is negative\n5. otherwise place positve/ negative on each position other than first")
		self.Input.pack()
		self.Input.config(font=("Calibri",13))

		self.Quit = Button(self.master,text="Quit",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=700,y=130)

class SignIn():
	def __init__(self,master):
	
		self.master = master
		self.master.geometry("200x180")

		self.choices = Label(self.master,text="Choose and option:")
		self.choices.pack()

		self.KnownValuesGraphing = Button(self.master,text="Known values graphing",command=self.knownValuesGraphing)
		self.KnownValuesGraphing.pack()
		
		self.UnknownValuesGraphing = Button(self.master,text="Unknown values graphing", command=self.unknownValuesGraphing)
		self.UnknownValuesGraphing.pack()
		
		self.Previous_Equtaions = Button(self.master,text="load previous equtaions",command=self.Load_previous_Equations)
		self.Previous_Equtaions.pack()
		
		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=50,y=130)
		print(Username)

		if Username == "Admin" and Allow == True:
			self.AdminButton = Button(self.master,text="Display users",command=self.display)
			self.AdminButton.pack()
			self.AdminButton.place(x=60,y=100)

	def display(self):
		Display = Toplevel(self.master)
		DsiplayGUI = DsiplayUsers(Display)

		def select_product():
			getUsername = Usernameinput.get()
			getPassword = Passwordinput.get()
			with sqlite3.connect("GRAPHINGDATABASEFINAL.db") as db:
				cursor = db.cursor()
				cursor.execute("SELECT Username from UserTable where Username=?",(getUsername,))
				usernameProduct = cursor.fetchone()
				cursor.execute("SELECT Password from UserTable where Password=?",(getPassword,))
				passwordProduct = cursor.fetchone()
				print(usernameProduct,passwordProduct)
				cursor.close()
			
	def knownValuesGraphing(self):
		print("knownValuesGraphing")
		knownroot = Toplevel(self.master)
		KnownvaluesGUI = KnownValuesGraphing(knownroot)


	def unknownValuesGraphing(self):
		print("unknownValuesGraphing")
		unknownroot = Toplevel(self.master)
		unknownvaluesGUI = UnknownValuesGraphing(unknownroot)

	def Load_previous_Equations(self):
		print("Load_previous_Equations")
		loadPrevious = Toplevel(self.master)
		loadPreviousGUI = load_previous_equations(loadPrevious)

class GraphMultiple():
	def __init__(self,master):

		self.master = master
		self.master.geometry("250x200")
		self.master.title("Graph Multiple Equations")

		self.Label = Label(self.master,text="enter equations to graph")
		self.Label.pack()
		self.Label.place(x=0,y=0)

		self.equation1 = Label(self.master,text="equation 1:")
		self.equation1.pack()
		self.equation1.place(x=0,y=30)
		self.entry1 = Entry(self.master)
		self.entry1.pack()
		self.entry1.place(x=65,y=30)

		self.equation2 = Label(self.master,text="equation 2:")
		self.equation2.pack()
		self.equation2.place(x=0,y=60)
		self.entry2 = Entry(self.master)
		self.entry2.pack()
		self.entry2.place(x=65,y=60)

		self.xrangelabel = Label(self.master,text="X limits:")
		self.xrangelabel.pack()
		self.xrangelabel.place(x=0,y=90)
		self.yrangelabel = Label(self.master,text="Y limits:")
		self.yrangelabel.pack()
		self.yrangelabel.place(x=0,y=120)

		self.xrangeEntry = Entry(self.master,width=10)
		self.xrangeEntry.pack()
		self.xrangeEntry.place(x=50,y=90)
		self.yrangeEntry = Entry(self.master,width=10)
		self.yrangeEntry.pack()
		self.yrangeEntry.place(x=50,y=120)

		self.graphbutton = Button(self.master,text="graph",command=lambda:self.graph())
		self.graphbutton.pack()
		self.graphbutton.place(x=150,y=90)
		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=0,y=150)
		
	def graph(self):
		xlim = self.xrangeEntry.get()
		ylim = self.yrangeEntry.get()
		equation1 = self.entry1.get()
		equation2 = self.entry2.get()
		equation = ""
		GRAPH.graphactual(xlim,ylim,equation,equation1,equation2)

class DsiplayUsers():
	def __init__(self,master):
		self.master = master
		self.master.geometry("810x120")
		self.master.title("Users")

		fr2 = LabelFrame(self.master, text= 'User Details')
		fr2.pack()

		tree = ttk.Treeview(fr2, height=2, columns=("#0","#1","#2"))
		tree.grid(row=2, column=3, columnspan=1, sticky=S)

		tree.heading('#0', text='User_ID', anchor=W)
		tree.heading('#1', text='Full Name', anchor=W)
		tree.heading('#2',text= 'Username',anchor=W)
		tree.heading('#3', text='Password', anchor=W)
		cursor = conn.cursor()
		List = cursor.execute("SELECT * FROM UserTable ORDER BY UserID DESC")
		for row in List:
			tree.insert("",0,text=row[0],values=(row[1],row[2],row[3]))
		cursor.close()
		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=700,y=90)

class load_previous_equations():
	def __init__ (self,master):
		print(Username)
		equationArray = []
		equationArraytocmp = []
		equationtoremove = []
		self.master = master
		self.master.geometry("210x150")
		self.master.title("previous equtaions")
		fr2 = LabelFrame(self.master, text= 'Previous equations')
		fr2.pack()

		tree = ttk.Treeview(fr2, height=5)
		tree.grid(row=1, column=1, columnspan=1, sticky=S)
		
		tree.heading('#0', text='Equations', anchor=W)

		cursor.execute("SELECT UserID FROM UserTable WHERE Username=?",(Username,))
		UserID = cursor.fetchone()

		UserID = str(UserID)
		UserID = UserID.replace(',','')
		UserID = UserID.replace('(','')
		UserID = UserID.replace(')','')
		UserID = int(UserID)
		UserID_1 = UserID
		
		cursor.execute("SELECT Equation FROM EquationTable WHERE UserID_1=?",(UserID_1,))
		A = cursor.fetchall()

		for i in range(len(A)):
			equationArray.append(A[i])
		cursor.execute("SELECT ID_2 FROM OccurancesTable WHERE UserID_2=?",(UserID_1,))
		B = cursor.fetchall()

		for i in range(len(B)):
			cursor.execute("SELECT Equation FROM EquationTable WHERE ID=?",(B[i]))
			a = cursor.fetchone()

			equationArraytocmp.append(a)

		for i in range(len(equationArray)):
			for x in range(len(equationArraytocmp)):
				if equationArray[i] == equationArraytocmp[x]:
					equationtoremove.append(equationArraytocmp[x])
				
		a = (list(set(equationArraytocmp)-set(equationtoremove)))

		equationArray.append(a)
		for row in equationArray:
			tree.insert("",0,text=row[0])
				
		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=500,y=149)

class polynomial2():
	def __init__(self,master):
		self.master = master
		self.master.geometry("170x150")
		self.master.title("polynomial degree two")
		
		self.example = Label(self.master,text="ax^2+bx+c")
		self.example.pack()
		self.example.place(x=30,y=0)
		self.onep2 = Entry(self.master,bd=3,width=4)
		self.onep2.pack()
		self.onep2.place(x=5,y=30)
		self.twop2 = Entry(self.master,bd=3,width=4)
		self.twop2.pack()
		self.twop2.place(x=5,y=60)
		self.threep2 = Entry(self.master,bd=3,width=4)
		self.threep2.pack()
		self.threep2.place(x=5,y=90)

		self.one = Label(self.master,text="x^2")
		self.one.pack()
		self.one.place(x=35,y=30)
		self.two = Label(self.master,text="x")
		self.two.pack()
		self.two.place(x=35,y=60)

		self.ylimlabel = Label(self.master,text="Y limits")
		self.ylimlabel.pack()
		self.ylimlabel.place(x=60,y=30)
		self.ylim = Entry(self.master,bd=3,width=6)
		self.ylim.pack()
		self.ylim.place(x=120,y=30)
		self.xlimlabel = Label(self.master,text="X limits")
		self.xlimlabel.pack()
		self.xlimlabel.place(x=60,y=60)
		self.xlim = Entry(self.master,bd=3,width=6)
		self.xlim.pack()
		self.xlim.place(x=120,y=60)

		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=20,y=120)

		self.graph = Button(self.master,text="graph",command=lambda:self.graphbutton())
		self.graph.pack()
		self.graph.place(x=120,y=90)
			
	def graphbutton(self):
		part1skip = False
		part2skip = False
		part3skip = False
		allowedtopass = True
		equation1 = ""
		equation2 = ""

		Usernametopass = Username
		part1 = self.onep2.get()
		part2 = self.twop2.get()
		part3 = self.threep2.get()
		ylim = self.ylim.get()
		xlim = self.xlim.get()
		print(part1,part2,part3)
		
		if part1 == "":
			part1skip = True
			part1 = "0"

		if part2 == "":
			part2skip = True
			part2 = "+0"

		if part3 == "":
			part3skip = True
			part3 = "+0"
		
		if part2skip == False:
			if part2[0] == "+" or part2[0] == "-" and part2[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator 2",part2[0])
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=90)
			
		if part3skip == False:
			if part3[0] == "+" or part3[0] == "-" and part3[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator 3")
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=90)

		if part1 == " " and part2 == " " and part3 == " ":
			allowedtopass = False
			print(allowedtopass)

		if allowedtopass == True:
			equation = part1 +"x^2"+ part2 + "x"+ part3
			GRAPH.graphactual(xlim,ylim,equation,equation1,equation2)
			EquationToPlace = equation
			UnknownValuesGraphing.PlaceInDatabase(self,Username,EquationToPlace)

class polynomial3():
	def __init__(self,master):
		self.master = master
		self.master.geometry("210x150")
		self.master.title("polynomial degree three")
		
		self.example = Label(self.master,text="ax^3+bx^2+cx+d")
		self.example.pack()
		
		self.onep3 = Entry(self.master,bd=3,width = 4)
		self.onep3.pack()
		self.onep3.place(x=5,y=20)
		self.twop3 = Entry(self.master,bd=3,width = 4)
		self.twop3.pack()
		self.twop3.place(x=5,y=50)
		self.threep3 = Entry(self.master,bd=3,width = 4)
		self.threep3.pack()
		self.threep3.place(x=5,y=80)
		self.fourp3 = Entry(self.master,bd=3,width = 4)
		self.fourp3.pack()
		self.fourp3.place(x=5,y=110)

		self.one = Label(self.master,text="x^3")
		self.one.pack()
		self.one.place(x=35,y=20)
		self.two = Label(self.master,text="x^2")
		self.two.pack()
		self.two.place(x=35,y=50)
		self.three = Label(self.master,text="x")
		self.three.pack()
		self.three.place(x=35,y=80)

		self.ylimlabel = Label(self.master,text="Y limits")
		self.ylimlabel.pack()
		self.ylimlabel.place(x=65,y=30)
		self.ylim = Entry(self.master,bd=3,width=6)
		self.ylim.pack()
		self.ylim.place(x=120,y=30)
		self.xlimlabel = Label(self.master,text="X limits")
		self.xlimlabel.pack()
		self.xlimlabel.place(x=65,y=60)
		self.xlim = Entry(self.master,bd=3,width=6)
		self.xlim.pack()
		self.xlim.place(x=120,y=60)

		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=40,y=120)

		self.graph = Button(self.master,text="graph",command=lambda:self.graphbutton())
		self.graph.pack()
		self.graph.place(x=120,y=90)

	def graphbutton(self):
		part1skip = False
		part2skip = False
		part3skip = False
		part4skip = False
		allowedtopass = True

		equation1 = ""
		equation2 = ""

		Usernametopass = Username
		part1 = self.onep3.get()
		part2 = self.twop3.get()
		part3 = self.threep3.get()
		part4 = self.fourp3.get()
		ylim = self.ylim.get()
		xlim = self.xlim.get()

		if part1 == "" :
			part1skip = True
			part1 = "0"

		if part2 == "":
			part2skip = True
			part2 = "+0"

		if part3 == "":
			part3skip = True
			part3 = "+0"

		if part4 == "":
			part4skip = True
			part4 = "+0"

		if part2skip == False:
			if part2[0] == "+" or part2[0] == "-" and part2[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator")
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=90)

		if part3skip == False:
			if part3[0] == "+" or part3[0] == "-" and part3[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator")
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=90)

		if part4skip == False:
			if part4[0] == "+" or part4[0] == "-" and part4[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator")
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=90)

		if part1 == "" and part2 == "" and part3 == "" and part4 == "":
			allowedtopass = False
			print(allowedtopass)

		if allowedtopass == True:
			equation = part1  +"x^3" + part2 + "x^2"  + part3 + "x"  + part4
			EquationToPlace = equation
			UnknownValuesGraphing.PlaceInDatabase(self,Username,EquationToPlace)
			GRAPH.graphactual(xlim,ylim,equation,equation1,equation2)

class polynomial4():
	def __init__(self,master):
		self.master = master
		self.master.geometry("210x180")
		self.master.title("polynomial degree four")
	
		self.example = Label(self.master,text="ax^4+bx^3+cx^2+dx+e")
		self.example.pack()

		self.onep4 = Entry(self.master,bd=3,width = 4)
		self.onep4.pack()
		self.onep4.place(x=5,y=20)
		self.twop4 = Entry(self.master,bd=3,width = 4)
		self.twop4.pack()
		self.twop4.place(x=5,y=50)
		self.threep4 = Entry(self.master,bd=3,width = 4)
		self.threep4.pack()
		self.threep4.place(x=5,y=80)
		self.fourp4 = Entry(self.master,bd=3,width = 4)
		self.fourp4.pack()
		self.fourp4.place(x=5,y=110)
		self.fivep4 = Entry(self.master,bd=3,width = 4)
		self.fivep4.pack()
		self.fivep4.place(x=5,y=140)

		self.one = Label(self.master,text="x^4")
		self.one.pack()
		self.one.place(x=35,y=20)
		self.two = Label(self.master,text="x^3")
		self.two.pack()
		self.two.place(x=35,y=50)
		self.three = Label(self.master,text="x^2")
		self.three.pack()
		self.three.place(x=35,y=80)
		self.four = Label(self.master,text="x")
		self.four.pack()
		self.four.place(x=35,y=110)

		self.ylimlabel = Label(self.master,text="Y limits")
		self.ylimlabel.pack()
		self.ylimlabel.place(x=65,y=30)
		self.ylim = Entry(self.master,bd=3,width=6)
		self.ylim.pack()
		self.ylim.place(x=120,y=30)
		self.xlimlabel = Label(self.master,text="X limits")
		self.xlimlabel.pack()
		self.xlimlabel.place(x=65,y=60)
		self.xlim = Entry(self.master,bd=3,width=6)
		self.xlim.pack()
		self.xlim.place(x=120,y=60)

		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=40,y=150)

		self.graph = Button(self.master,text="graph",command=lambda:self.graphbutton())
		self.graph.pack()
		self.graph.place(x=120,y=95)

	def graphbutton(self):
		part1skip = False
		part2skip = False
		part3skip = False
		part4skip = False
		part5skip = False
		allowedtopass = True

		equation1 = ""
		equation2 = ""

		Usernametopass = Username
		part1 = self.onep4.get()
		part2 = self.twop4.get()
		part3 = self.threep4.get()
		part4 = self.fourp4.get()
		part5 = self.fivep4.get()
		ylim = self.ylim.get()
		xlim = self.xlim.get()

		if part1 == "":
			part1skip = True
			part1 = "0"

		if part2 == "":
			part2skip = True
			part2 = "+0"

		if part3 == "":
			part3skip = True
			part3 = "+0"

		if part4 == "":
			part4skip = True
			part4 = "+0"

		if part5 == "":
			part5skip = True
			part5 = "+0"

		if part2skip == False:
			if part2[0] == "+" or part2[0] == "-" and part2[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator")
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=95)

		if part3skip == False:
			if part3[0] == "+" or part3[0] == "-" and part3[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator")
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=95)

		if part4skip == False:
			if part4[0] == "+" or part4[0] == "-" and part4[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator")
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=95)

		if part5skip == False:
			if part5[0] == "+" or part5[0] == "-" and part5[0] != "":
				allowedtopass = True
			else:
				print("you must include an indicator")
				allowedtopass = False
				ErrorLabel = Label(self.master, text="ERROR",fg="red")
				ErrorLabel.pack()
				ErrorLabel.place(x=70,y=95)

		if part1 == "" and part2 == "" and part3 == "" and part4 == "" and part5 == "":
			allowedtopass = False
			print(allowedtopass)

		if allowedtopass == True:
			print(allowedtopass)
			equation = part1 +"x^4"+ part2 +"x^3" + part3 +"x^2" + part4 +"x" + part5
			EquationToPlace = equation
			UnknownValuesGraphing.PlaceInDatabase(self,Username,EquationToPlace)
			GRAPH.graphactual(xlim,ylim,equation,equation1,equation2)

class UnknownValuesGraphing():
	def __init__(self,master):
		self.master = master
		self.master.geometry("360x120")
		self.master.title("Unknown values graphing")
		passed = Username
		

		def two():
			print("two")
			TWO = Toplevel(self.master)
			TwoGUI = polynomial2(TWO)
		
		def three():
			print("three")
			THREE = Toplevel(self.master)
			threeGUI = polynomial3(THREE)

		def four():
			print("four")
			FOUR = Toplevel(self.master)
			fourGUI = polynomial4(FOUR)
			
		self.two = Button(self.master,text="two  ",bd=3,command=two)
		self.two.pack()
		self.two.place(x=0,y=0)
		self.three = Button(self.master,text="three",bd=3,command=three)
		self.three.pack()
		self.three.place(x=0,y=30)
		self.four = Button(self.master,text="four ",bd=3,command=four)
		self.four.pack()
		self.four.place(x=0,y=60)

		
		self.anyEquation = Entry(self.master,width=20)
		self.anyEquation.pack()
		self.anyEquation.place(x=60,y=30)
		self.anyEquationlabel = Label(self.master,text="any polinomial degree")
		self.anyEquationlabel.pack()
		self.anyEquationlabel.place(x=60,y=0)

		self.graphmultiple = Button(self.master,text="Graph multiple",command=self.graphmultiple)
		self.graphmultiple.pack()
		self.graphmultiple.place(x=190,y=60)		

		self.Quit = Button(self.master,text="Quit",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=0,y=90)
		self.SubmitEquation = Button(self.master,text="Graph",command=lambda:[self.PlaceInDatabase(passed,self.anyEquation.get()),self.getequation()])
		self.SubmitEquation.pack()
		self.SubmitEquation.place(x=190,y=30)
		self.decideyRangeEntry = Entry(self.master,width=10)
		self.decideyRangeEntry.pack()
		self.decideyRangeEntry.place(x=120,y=60)
		self.decideyrangelabel = Label(self.master,text="enter Y limits")
		self.decideyrangelabel.pack()
		self.decideyrangelabel.place(x=40,y=60)
		self.decidexrangelabel = Label(self.master,text="enter X limits")
		self.decidexrangelabel.pack()
		self.decidexrangelabel.place(x=40,y=90)
		self.decidexRangeEntry = Entry(self.master,width=10)
		self.decidexRangeEntry.pack()
		self.decidexRangeEntry.place(x=120,y=90)

	def getequation(self):
		equation1 = ""
		equation2 = ""
		equation = self.anyEquation.get()
		ylim = self.decideyRangeEntry.get()
		xlim = self.decidexRangeEntry.get()
		GRAPH.graphactual(xlim,ylim,equation,equation1,equation2)

	def graphmultiple(self):
		print("graph multiple")
		multipleroot = Toplevel(self.master)
		graphmultipleGUI = GraphMultiple(multipleroot)
		
	def PlaceInDatabase(self,Username,EquationToPlace):
		Equationarray = []
		count = 0
		cursor = conn.cursor()
		print(EquationToPlace,"this is the equation to place")
		if EquationToPlace not in numbers and "x" not in EquationToPlace:
			ErrorLabel = Label(self.master, text="ERROR",fg="red")
			ErrorLabel.pack()
			ErrorLabel.place(x=200,y=0)
			return
					
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		todayDate = date.today()
		Username = Username
		equation = EquationToPlace
		Date = todayDate
		Time = current_time
		values = (Username,equation,Date,Time)
		print(values)

		if EquationToPlace !=  "":
			sqlcommand1 = cursor.execute("""SELECT Equation FROM EquationTable""")
			data = cursor.fetchall()

			cursor.execute("SELECT UserID FROM UserTable WHERE Username=?",(Username,))
			UserIDGot = cursor.fetchone()
			
			for i in range(len(data)):
				Equationarray.append(data[i])

			def insertintoOccurances(Equationtouse):
				count2 = 0
				cursor.execute("SELECT ID FROM EquationTable WHERE Equation=?",(Equationtouse,))
				data2 = cursor.fetchall()
				cursor.execute("SELECT UserID FROM UserTable WHERE Username=?",(Username,))
				data3 = cursor.fetchall()
				EquationID = str(data2[0])
				UserID = str(data3[0])
				
				EquationID = EquationID.replace('(','')
				EquationID = EquationID.replace(')','')
				EquationID = EquationID.replace(',','')
				EquationID = EquationID.replace("'","")
				EquationID = int(EquationID)
				UserID = UserID.replace('(','')
				UserID = UserID.replace(')','')
				UserID = UserID.replace(',','')
				UserID = UserID.replace("'","")
				UserID = int(UserID)
				UserID_2 = UserID
				EquationID_2 = EquationID

				cursor.execute("SELECT UserID_2,ID_2 FROM OccurancesTable")
				select = cursor.fetchall()

				datatoinsert = (UserID_2,EquationID_2)
				print(datatoinsert)

				for i in range(len(select)):
					if select[i] == datatoinsert:
						print("this user has already placed this equation in the Occurances table")
						count2 += 1
						break
				if count2 == 0:
					cursor.execute("INSERT INTO OccurancesTable (ID_2,UserID_2) VALUES (?,?)",(EquationID_2,UserID_2))
					conn.commit()

			for i in range(len(data)):
				print(Equationarray)
				if EquationToPlace == Equationarray[i][0]:
					print("equation already in databse\nmoving to Occurances table")
					Equationtopass = EquationToPlace
					print(Equationtopass)
					insertintoOccurances(Equationtopass)
					count += 1
					break
				
			if count == 0:
				UserID_1 = UserIDGot[0]
				print(UserID_1,"this is the UserID")
				print("Adding equation to database")
				cursor.execute("INSERT INTO EquationTable (Username,Equation,Date,Time,UserID_1) VALUES (?,?,?,?,?)",(Username,equation,Date,Time,UserID_1))
				conn.commit()
		
class GRAPH():
	def separateXlim1(xlim):
		if xlim	 != "":
			count = 0 
			xlimhalf1 = ""
			for i in range(0,len(xlim)):
				if xlim[i] != ",":
					count += 1
				if xlim[i] == ",":
					for x in range(0,count):
						xlimhalf1 += xlim[x]
			if "." in xlim:
				Xax = float(xlimhalf1)
				return Xax
			else:
				Xax = int(xlimhalf1)
				return Xax
	def separateXlim2(xlim):
		if xlim	 != "":
			count = 0 
			xlimhalf2 = ""
			for i in range(0,len(xlim)):
				if xlim[i] != ",":
					count += 1
				if xlim[i] == ",":
					for y in range(count+1,len(xlim)):
						xlimhalf2 += xlim[y]
			if "." in xlim:
				Yax = float(xlimhalf2)
				return Yax
			else:
				Yax = int(xlimhalf2)
				print(Yax)
				return Yax
	def separateYlim1(ylim):
		if ylim != "":
			count = 0 
			ylimhalf1 = ""
			for i in range(0,len(ylim)):
				if ylim[i] != ",":
					count += 1
				if ylim[i] == ",":
					for x in range(0,count):
						ylimhalf1 += ylim[x]
			if "." in ylim:
				X = float(ylimhalf1)
				return X
			else:
				X = int(ylimhalf1)
				return X
	def separateYlim2(ylim):
		if ylim != "":
	 		count = 0 
	 		ylimhalf2 = ""
	 		for i in range(0,len(ylim)):
	 			if ylim[i] != ",":
	 				count += 1
	 			if ylim[i] == ",":
	 				for y in range(count+1,len(ylim)):
	 					ylimhalf2 += ylim[y]
	 		if "." in ylim:
	 			Y = float(ylimhalf2)
	 			return Y 
	 		else:
	 			Y = int(ylimhalf2)
	 			return Y
	def evaluatesingleEquation(equation):
		try:
			for i in range(0,len(equation)):
				if equation[i] in numbers and equation[i+1] == "x":
					equation = equation.replace(equation[i+1],'*x')
		except:
			print("string done")
		equation = equation.replace('^','**')
		return equation		 
	def evaluateEquation1(equation1):
		try:
			for i in range(0,len(equation1)):
				if equation1[i] in numbers and equation1[i+1] == "x":
					equation1 = equation1.replace(equation1[i+1],'*x')
		except:
			print("string done")
		equation1 = equation1.replace('^','**')
		print(equation1 ,"this is the first equation")
		return equation1
	def evaluateEquation2(equation2):
		try:
			for i in range(0,len(equation2)):
				if equation2[i] in numbers and equation2[i+1] == "x":
					equation2 = equation2.replace(equation2[i+1],'*x')
		except:
			print("string done")
		equation2 = equation2.replace('^','**')
		print(equation2,"this is the second equation")
		return equation2
	def plotIntersection(Xarray,Yarray,X1array,Y1array):
		intersect = []
		print("plotting point(s) of intersection")
		print(Xarray)
		for i in range(len(Xarray)):
			if len(X1array) == 0:
				if int(Xarray[i]) == 0:
					Xcoord = 0
					Ycoord = int(Yarray[i])
					return Xcoord,Ycoord
				if int(Yarray[i]) == 0:
					Xcoord = Xarray[i]
					Ycoord = 0
					return Xcoord,Ycoord
			
			if len(X1array) != 0:
				if Xarray[i] == X1array[i] and Yarray[i] == Y1array[i]:
					print("graphs intersect at point(s):",Xarray[i],Yarray[i])
					Xcoord = Xarray[i]
					Ycoord = Yarray[i]
					point = (Xcoord,Ycoord)
					intersect.append(point)
				if int(Xarray[i]) == 0 and int(X1array[i]) == 0:
					print("1")
					Xcoord = 0
					Ycoord = float(Yarray[i])
					point = (Xcoord,Ycoord)
					print(point)
					intersect.append(point)
				if int(Yarray[i]) == 0 and int(Y1array[i]) == 0:
					print("1")
					Xcoord = float(Xarray[i])
					Ycoord = 0
					point = (Xcoord,Ycoord)
					print(point)
					intersect.append(point)
		return intersect	
	def graphSingle(equation,Xax,Yax):
		singleequation = ""
		singleequation = equation
		Xarray = []
		Yarray = []
		X1array = []
		Y1array = []
		for i in np.arange(Xax,Yax,1):
				x = i
				y = eval(equation)
				Xarray.append(x)
				Yarray.append(y)
		Xcoord, Ycoord = GRAPH.plotIntersection(Xarray,Yarray,X1array,Y1array)
		Coordinate = (Xcoord,Ycoord)
		plt.scatter(Xcoord,Ycoord,s=50,label=Coordinate)
		plt.plot(Xarray,Yarray,label=singleequation)
		plt.legend()
	def graphMultiple(equation1,equation2,Xax,Yax):
		Xarray = []
		Yarray = []
		X1array = []
		Y1array = []
		singleequation1 = equation1
		singleequation2 = equation2
		for i in np.arange(Xax,Yax,1):
				x = i
				y = eval(equation1)
				X1array.append(x)
				Y1array.append(y)
		for axis in np.arange(Xax,Yax,1):
				x = axis
				y = eval(equation2)
				Xarray.append(x)
				Yarray.append(y)
		intersect = GRAPH.plotIntersection(Xarray,Yarray,X1array,Y1array)
		print(intersect,"are the points of intersection")
		print(intersect[0][0])
		if len(intersect) == 1:
			print("in")
			Xcoord = intersect[0][0]
			Ycoord = intersect[0][1]
			plt.scatter(Xcoord,Ycoord,s=50,label=intersect)
		else:
			for i in range(len(intersect)):
				Xcoord = intersect[i][0]
				Ycoord = intersect[i][1]
				print(Xcoord,Ycoord,"Coordinates")
				plt.scatter(Xcoord,Ycoord,s=50,label=intersect[i])
		plt.plot(X1array,Y1array,label=singleequation1)
		plt.plot(Xarray,Yarray,label=singleequation2)
		plt.legend()
	def plottrigonometry(equation):
		sine = "sin"
		cosine = "cos"
		tangent = "tan"
		if sine in equation:
			time = np.arange(0,10,0.1)
			amplitude = np.sin(time)
			plt.plot(time,amplitude)
			plt.grid(True,which='both')
			plt.axhline(y=0,color='k')
			plt.axvline(x=0,color='k')
			plt.show()
			doOther = False
			print("in equation")

		if cosine in equation:
			time = np.arange(-60,60,0.1)
			amplitude = np.cos(time)
			plt.plot(time,amplitude)
			plt.plot(time,amplitude)
			plt.grid(True,which='both')
			plt.axhline(y=0,color='k')
			plt.axvline(x=0,color='k')
			plt.show()
			doOther = False
			print("in equation")
	
		if tangent in equation:
			time = np.arange(0,10,0.1)
			amplitude = np.tan(time)
			plt.plot(time,amplitude)
			plt.grid(True,which='both')
			plt.axhline(y=0,color='k')
			plt.axvline(x=0,color='k')
			plt.show()
			doOther = False
			print("in equation")
	def graphactual(xlim,ylim,equation,equation1,equation2):
		x = 0
		trigonometric = "sin","cos","tan"
		if xlim != "":
			Xax = GRAPH.separateXlim1(xlim)
			Yax = GRAPH.separateXlim2(xlim)
		else:
			Xax = -10
			Yax = 10
		if ylim != "":
			X = GRAPH.separateYlim1(ylim)
			Y = GRAPH.separateYlim2(ylim)
		else:
			X = -10
			Y = 10	
		equation1 = GRAPH.evaluateEquation1(equation1)
		equation2 = GRAPH.evaluateEquation2(equation2)
		equation = GRAPH.evaluatesingleEquation(equation)
		if equation in trigonometric:
			GRAPH.plottrigonometry(equation)

		X = GRAPH.separateYlim1(ylim)
		Y = GRAPH.separateYlim2(ylim)
		
		if equation1 == "" and equation2 == "":
			GRAPH.graphSingle(equation,Xax,Yax)
		else:
			GRAPH.graphMultiple(equation1,equation2,Xax,Yax)
		if ylim != "":
			plt.ylim([X,Y])
		if xlim != "":
			plt.xlim([Xax,Yax])

		plt.grid(True,which='both')
		plt.axhline(y=0,color='k')
		plt.axvline(x=0,color='k')
		plt.show()

class KnownValuesGraphing():
	def __init__(self,master):
		allowtograph = True
		self.master = master
		self.master.geometry("280x200")


		self.Greeting = Label(self.master,text="Welcome to: Graphing",relief=GROOVE)
		self.Greeting.pack()

		self.enter_label = Label(self.master,text="Enter the values below followed by a comma\nnumber of points have to be the same for each entry",relief=GROOVE)
		self.enter_label.pack()
		self.enter_label.place(x=0,y=0)

		self.EquationX = Entry(self.master,bd=3)
		self.EquationX.pack()
		self.EquationX.place(x=15,y=60)

		self.EquationY = Entry(self.master,bd=3)
		self.EquationY.pack()
		self.EquationY.place(x=15,y=90)

		self.EquationXLabel = Label(self.master,text="X:")
		self.EquationXLabel.pack()
		self.EquationXLabel.place(x=0,y=60)

		self.EquationYLabel = Label(self.master,text="Y:")
		self.EquationYLabel.pack()
		self.EquationYLabel.place(x=0,y=90)

		self.GoToGraphing = Button(self.master,text="Graph",command=self.matplotcanvas)
		self.GoToGraphing.pack()
		self.GoToGraphing.place(x=130,y=120)


		self.Quit = Button(self.master,text="Quit application",fg="red",command=self.master.destroy)
		self.Quit.pack()
		self.Quit.place(x=20,y=120)




	def matplotcanvas(self):
		xArray = []
		yArray =[]
		xValues = self.EquationX.get()
		yValues = self.EquationY.get()

		print(xValues,"before")
		

		if len(xValues) != len(yValues):
			ErrorLabel = Label(self.master, text="ERROR, number of values must be matching",fg="red")
			ErrorLabel.pack()
			ErrorLabel.place(x=0,y=150)
			allowtograph = False
		else:
			allowtograph = True

		if xValues != " ":
			for i in range(0,len(xValues)):
				if xValues[i] != (","):
					xArray.append(xValues[i])
			print(xArray)
			for i in range(0,len(xArray)):
				xArray[i] = int(xArray[i])
			print(xArray)

		if yValues != " ":
			for i in range(0,len(yValues)):
				if yValues[i] != (","):
					yArray.append(yValues[i])
			print(yArray)
			for i in range(0,len(yArray)):
				yArray[i] = int(yArray[i])
			print(yArray)

		if allowtograph == True:
			plt.plot(xArray,yArray)
			plt.grid(True,which='both')
			plt.axhline(y=0,color='k')
			plt.axvline(x=0,color='k')
			plt.show()

def main():
	root = Tk()
	app = window(root)
	root.mainloop()
if __name__ == "__main__":
	main()