from tkinter import *
from tkinter import ttk
import sqlite3
import random

conn = sqlite3.connect("QandA.db")
cursor = conn.cursor()

class window:
	def __init__(self,master):
		self.master = master
		self.master.geometry("")
		self.master.title("Start Up Page")

		SignInFrame = LabelFrame(self.master,text="Sign In")
		SignInFrame.grid(row=0,column=0,sticky="W")
		CreateAccountFrame = LabelFrame(self.master,text="Create Account")
		CreateAccountFrame.grid(row=2,column=0,sticky="W")

		self.LabelUsername = Label(SignInFrame,text="Username:")
		self.LabelUsername.grid(row=2,column=0)
		self.UsernameEntry = Entry(SignInFrame)
		self.UsernameEntry.grid(row=2,column=1)
		self.LabelPassword = Label(SignInFrame,text="Password:").grid(row=3,column=0)
		self.PasswordEntry = Entry(SignInFrame,show="*")
		self.PasswordEntry.grid(row=3,column=1)
		self.SignInButton = Button(SignInFrame,text="Sign in",command=lambda:self.getvalues(SignInFrame)).grid(row=3,column=5)
		
		self.LabelFullNameCreate = Label(CreateAccountFrame,text="FullName:").grid(row=0,column=0)
		self.EntryFullNameCreate = Entry(CreateAccountFrame)
		self.EntryFullNameCreate.grid(row=0,column=1)
		self.LabelUsernameCreate = Label(CreateAccountFrame,text="Username:").grid(row=3,column=0)
		self.EntryUsernameCreate = Entry(CreateAccountFrame)
		self.EntryUsernameCreate.grid(row=3,column=1)
		self.LabelPassword1Create = Label(CreateAccountFrame,text="Password:").grid(row=6,column=0)
		self.EntryPassword1Create = Entry(CreateAccountFrame,show="*")
		self.EntryPassword1Create.grid(row=6,column=1)
		self.LabelPassword2Create = Label(CreateAccountFrame,text="Re-enter Password:").grid(row=9,column=0)
		self.EntryPassword2Create = Entry(CreateAccountFrame,show="*")
		self.EntryPassword2Create.grid(row=9,column=1)
		self.CreateButton = Button(CreateAccountFrame,text="Create Account",command=lambda:self.CreateAccount(CreateAccountFrame)).grid(row=9,column=2)

	def CreateAccount(self,CreateAccountFrame):
		checkArray = []
		Topics = ['Maths','Biology','Chemistry','Physics','Computer Science','English Lit','English Lang','Geography','History']

		canplace = False
		copycheck = False

		FullNameCreate = self.EntryFullNameCreate.get()
		UsernameCreate = self.EntryUsernameCreate.get()
		Password1Create = self.EntryPassword1Create.get()
		Password2Create = self.EntryPassword2Create.get()

		checkArray.append(FullNameCreate)
		checkArray.append(UsernameCreate)
		checkArray.append(Password1Create)
		checkArray.append(Password2Create)

		cursor.execute("""SELECT Username FROM UserTable""")
		data = cursor.fetchall()

		for i in range(len(data)):
			Username_Database = data[i][0]
			if Username_Database == UsernameCreate:
				copycheck = True
				self.ErrorLabel = Label(CreateAccountFrame,text="ERROR-Username taken",fg="red").grid(row=10,column=1)

		for i in range(len(checkArray)):
			if checkArray[i] == "":
				self.ErrorLabel = Label(CreateAccountFrame,text="ERROR",fg="red").grid(row=10,column=1)
				canplace = False
			else:
				canplace = True

		if Password1Create != Password2Create:
			canplace = False
			self.ErrorLabel = Label(CreateAccountFrame,text="ERROR, passwords do not match",fg="red").grid(row=10,column=1)

		if canplace and not copycheck: 
			cursor.execute("""INSERT INTO UserTable (Name,Username,Password) VALUES(?,?,?)""",(FullNameCreate,UsernameCreate,Password1Create))
			conn.commit()
			cursor.execute("""SELECT UserID FROM UserTable WHERE Username=?""",(UsernameCreate,))
			UserID = cursor.fetchone()
			UserID = str(UserID)
			UserID = UserID.replace(',','')
			UserID = UserID.replace('(','')
			UserID = UserID.replace(')','')
			for i in range(len(Topics)):
				cursor.execute("""INSERT INTO TopicTable (TopicName,UserID_Topics) VALUES(?,?)""",(Topics[i],UserID))
				conn.commit()
		
	def getvalues(self,SignInFrame):
		global Username
		Username = self.UsernameEntry.get()
		Password = self.PasswordEntry.get()
		canEnter = False
		UsernameEnter = False
		PasswordEnter = False
		cursor.execute("""SELECT Username,Password FROM UserTable""")
		data = cursor.fetchall()
		for i in range(len(data)):
			usernamedata = data[i][0]
			passworddata = data[i][1]
			if Username == usernamedata:
				UsernameEnter = True
			if Password == passworddata:
				PasswordEnter = True
		if not PasswordEnter or not UsernameEnter:
			self.ErrorLabel = Label(SignInFrame,text="ERROR",fg="red").grid(row=10,column=1)
		else:
			canEnter = True
			self.master.destroy()
			questions = Tk()
			questionsGUI = QandA(questions)

class QandA:
	def __init__(self,master):
		self.master = master
		self.master.geometry("")
		self.master.title("Questions Page")

		self.QuestionArray = []
		self.AnswerArray = []

		cursor.execute("""SELECT UserID FROM UserTable WHERE Username=?""",(Username,))
		UserID = cursor.fetchone()
		cursor.execute("""SELECT TopicName FROM TopicTable WHERE UserID_Topics=?""",(UserID))
		data = cursor.fetchall()

		YearData = ['Year 7','Year 8','Year 9','Year 10','Year 11','Year 12','Year 13']
		self.variable = StringVar()
		self.variable.set("Select Topic")
		self.YearVal = StringVar()
		self.YearVal.set("Select Year")

		StartFrame = LabelFrame(self.master,text="Enter number of flashcards")
		StartFrame.grid(row=0,column=20,sticky="N")
		QuestionsFrame = LabelFrame(self.master,text="Questions")
		QuestionsFrame.grid(row=0,column=0,sticky="N")
		AnswerFrame = LabelFrame(self.master,text="Answers")
		AnswerFrame.grid(row=0,column=1,sticky="N")
		TreeFrame = LabelFrame(self.master,text="All Flashcards")
		TreeFrame.grid(row=0,column=26,sticky="N")
		TopicFrame = LabelFrame(self.master,text="Create a topic")
		TopicFrame.grid(row=0,column=27,sticky="N")
		ClutterFrame = LabelFrame(self.master,text="Options")
		ClutterFrame.grid(row=0,column=25,sticky="N")
		
		self.NumberOfFlashCards = Entry(StartFrame,width=4)
		self.NumberOfFlashCards.grid(row=0,column=0)
		self.SubmitButton = Button(StartFrame,text="Create Flash Cards",command=lambda:self.MakeFlashCards(self.AnswerArray,QuestionsFrame,AnswerFrame)).grid(row=1,column=0)
		self.MakeMore = Button(StartFrame,text="Add Another",command=lambda:self.MakeMoreSub(self.QuestionArray,self.AnswerArray,QuestionsFrame,AnswerFrame)).grid(row=2,column=0)
		self.ChooseTopicToSaveTo = OptionMenu(StartFrame,self.variable,*data).grid(row=0,column=1) 
		self.ChooseYearGroup = OptionMenu(StartFrame,self.YearVal,*YearData).grid(row=0,column=2)
		self.RefreshButton = Button(StartFrame,text="Refresh",command=self.RefreshSub).grid(row=1,column=1)
		self.SaveButton = Button(StartFrame,text="Save",command=lambda:self.SaveFunction(self.QuestionArray,self.AnswerArray,StartFrame)).grid(row=3,column=0)
		self.Test = Button(ClutterFrame,text="Test Yourself",command=lambda:self.TestYourself(self.QuestionArray)).grid(row=0,column=0)
		self.ViewAll = Button(ClutterFrame,text="View All",command=lambda:self.TreeViewSub(TreeFrame)).grid(row=3,column=0)
		self.ReturnButton = Button(ClutterFrame,text="Previous Page",command=self.goback).grid(row=6,column=0)
		self.TopicEntry = Entry(TopicFrame)
		self.TopicEntry.grid(row=0,column=0)
		self.SaveTopicButton = Button(TopicFrame,text="Save Topic",command=self.TopicSaveSub).grid(row=1,column=0)

	def RefreshSub(self):
		self.master.destroy()
		Window = Tk()
		QandAGUI = QandA(Window)

	def TopicSaveSub(self):
		canPlace = True
		TopicName = self.TopicEntry.get()
		cursor.execute("""SELECT UserID FROM UserTable WHERE Username=?""",(Username,))
		UserID = cursor.fetchone()
		cursor.execute("""SELECT TopicName FROM TopicTable WHERE UserID_Topics=?""",(UserID))
		Topics = cursor.fetchall()
		UserID = str(UserID)
		UserID = UserID.replace(',','')
		UserID = UserID.replace('(','')
		UserID = UserID.replace(')','')
		for i in range(len(Topics)):
			if TopicName in Topics[i]:
				canPlace = False
		if canPlace:
			cursor.execute("""INSERT INTO TopicTable(TopicName,UserID_Topics) VALUES(?,?)""",(TopicName,UserID))
			conn.commit()
			
	def TestYourself(self,QuestionArray):
		self.master.destroy()
		Testing = Tk()
		TestingGUI = Test(Testing)

	def TreeViewSub(self,TreeFrame):
		Topics = []
		DataToInput = []

		cursor.execute("""SELECT UserID FROM UserTable WHERE Username=?""",(Username,))
		UserID = cursor.fetchone()
		UserID = str(UserID)
		UserID = UserID.replace(',','')
		UserID = UserID.replace('(','')
		UserID = UserID.replace(')','')

		cursor.execute("""SELECT Question,Answer,TopicID_Questions FROM FlashCardTable WHERE UserID_Questions=? ORDER BY TopicID_Questions DESC""",(UserID))
		AllQuestions = cursor.fetchall()
		print(AllQuestions)

		for i in range(len(AllQuestions)):
			cursor.execute("""SELECT TopicName FROM TopicTable WHERE UserID_Topics=? AND TopicID=?""",(UserID,AllQuestions[i][2]))
			TopicNames = cursor.fetchone()
			print(TopicNames)
			TopicNames = str(TopicNames)
			TopicNames = TopicNames.replace(',','')
			TopicNames = TopicNames.replace('(','')
			TopicNames = TopicNames.replace(')','')
			TopicNames = TopicNames.replace("'","")
			Topics.append(TopicNames)

		for i in range(len(AllQuestions)):
			data = str(AllQuestions[i][0]) , str(AllQuestions[i][1]) , str(Topics[i])
			DataToInput.append(data)

		tree = ttk.Treeview(TreeFrame,height=7,columns=('#0','#1'))
		tree.grid(row=1,column=1,columnspan=1,sticky="N")
		tree.heading('#0',text="Questions",anchor="w")
		tree.heading('#1',text="Answers",anchor="w")
		tree.heading('#2',text="Topics",anchor="w")
		for i in DataToInput:
			tree.insert("",0,text=i[0],values=(i[1],i[2]))

	def MakeFlashCards(self,AnswerArray,QuestionsFrame,AnswerFrame):
		NumberToMake = int(self.NumberOfFlashCards.get()) 
		for i in range(NumberToMake):
			self.QuestionArray.append(Text(QuestionsFrame,width=30,height=5))
			self.QuestionArray[i].grid(row=i,column=0)
			self.AnswerArray.append(Text(AnswerFrame,width=30,height=5))
			self.AnswerArray[i].grid(row=i,column=1)
		
	def MakeMoreSub(self,QuestionArray,AnswerArray,QuestionsFrame,AnswerFrame):
		ROWQ = len(QuestionArray)
		ROWA = len(AnswerArray)
		self.QuestionArray.append(Text(QuestionsFrame,width=30,height=5))
		self.QuestionArray[-1].grid(row=ROWQ,column=0)
		self.AnswerArray.append(Text(AnswerFrame,width=30,height=5))
		self.AnswerArray[-1].grid(row=ROWA,column=1)

	def SaveFunction(self,QuestionArray,AnswerArray,StartFrame):
		Topic = self.variable.get()
		YearGroup = self.YearVal.get()
		GetID = True
		cursor.execute("""SELECT UserID FROM UserTable WHERE Username=?""",(Username,))
		UserID = cursor.fetchone()
		UserID = str(UserID)
		UserID = UserID.replace(',','')
		UserID = UserID.replace('(','')
		UserID = UserID.replace(')','')
		if Topic == "Select Topic":
			self.ErrorLabel = Label(StartFrame,text="ERROR-Choose a topic to save to",fg="red").grid(row=2,column=1)
		if GetID:
			Topic = str(Topic)
			Topic = Topic.replace('(','')
			Topic = Topic.replace(')','')
			Topic = Topic.replace(',','')
			Topic = Topic.replace("'","")
			cursor.execute("""SELECT TopicID FROM TopicTable WHERE TopicName=? AND UserID_Topics=?""",(Topic,UserID))
			TopicID = cursor.fetchone()
			TopicID = str(TopicID)
			TopicID = TopicID.replace(',','')
			TopicID = TopicID.replace('(','')
			TopicID = TopicID.replace(')','')

		for i in range(len(QuestionArray)):
			dataQ = str(self.QuestionArray[i].get('1.0','end-1c'))
			dataA = str(self.AnswerArray[i].get('1.0','end-1c'))
			if dataQ == "" or dataA == "":
				pass
			else:
				cursor.execute("""INSERT INTO FlashCardTable (Question,Answer,TopicID_Questions,UserID_Questions,YearGroup) VALUES(?,?,?,?,?)""",(dataQ,dataA,TopicID,UserID,YearGroup))
				conn.commit()
		
	def goback(self):
		self.master.destroy()
		login = Tk()
		loginGUI = window(login)

class Test:
	def __init__(self,master):
		self.master = master
		self.master.geometry("")
		self.Hints = []

		OptionsFrame = LabelFrame(self.master,text="Options")
		OptionsFrame.grid(row=0,column=20,sticky="N")
		QuestionsFrame = LabelFrame(self.master,text="Questions")
		QuestionsFrame.grid(row=0,column=0,sticky="N")
		AnswerFrame = LabelFrame(self.master,text="Answer")
		AnswerFrame.grid(row=8,column=0,sticky="N")
		HintFrame = LabelFrame(self.master,text="Hints")
		HintFrame.grid(row=0,column=25,sticky="N")

		cursor.execute("""SELECT UserID FROM UserTable WHERE Username=?""",(Username,))
		UserID = cursor.fetchone()
		cursor.execute("""SELECT TopicName FROM TopicTable WHERE UserID_Topics=?""",(UserID))
		data = cursor.fetchall()

		self.TestVariable = StringVar()
		self.TestVariable.set("Select Topic")
		self.TopicSet = OptionMenu(OptionsFrame,self.TestVariable,*data).grid(row=0,column=0)
		self.SetButton = Button(OptionsFrame,text="Set Topic",command=lambda:self.SetTopicSub()).grid(row=0,column=1)
		self.CheckButton = Button(OptionsFrame,text="Check",command=lambda:self.checkAnswer(self.QuestionsGot,self.AnswersGot,OptionsFrame,QuestionsFrame)).grid(row=1,column=0)
		self.HintButton = Button(OptionsFrame,text="Hint",command=lambda:self.HintSub(self.AnswersGot,HintFrame)).grid(row=2,column=0)
		self.ReturnButton = Button(OptionsFrame,text="Previous Page",command=self.goback).grid(row=3,column=0)
		self.Questions = Text(QuestionsFrame,width=30,height=5)
		self.Questions.grid(row=0,column=0)
		self.Answer = Entry(AnswerFrame,width=40)
		self.Answer.grid(row=0,column=0)

	def SetTopicSub(self):
		self.Hints = []
		self.Questions.delete('1.0',END)
		Topic = self.TestVariable.get()
		Topic = str(Topic)
		Topic = Topic.replace('(','')
		Topic = Topic.replace(')','')
		Topic = Topic.replace(',','')
		Topic = Topic.replace("'","")
		cursor.execute("""SELECT TopicID FROM TopicTable WHERE TopicName=?""",(Topic,))
		TopicID = cursor.fetchone()
		TopicID = str(TopicID)
		TopicID = TopicID.replace(',','')
		TopicID = TopicID.replace('(','')
		TopicID = TopicID.replace(')','')
		cursor.execute("""SELECT UserID FROM UserTable WHERE Username=?""",(Username,))
		UserID = cursor.fetchone()
		UserID = str(UserID)
		UserID = UserID.replace(',','')
		UserID = UserID.replace('(','')
		UserID = UserID.replace(')','')
		cursor.execute("""SELECT Question FROM FlashCardTable WHERE UserID_Questions=? AND TopicID_Questions=? """,(UserID,TopicID,))
		self.QuestionsGot = cursor.fetchall()
		cursor.execute("""SELECT Answer FROM FlashCardTable WHERE UserID_Questions=? AND TopicID_Questions=?""",(UserID,TopicID,))
		self.AnswersGot = cursor.fetchall()
		if len(self.QuestionsGot) == 0:
			self.Questions.insert(END,"No questions for this topic")
		else:
			DataToInsert = self.QuestionsGot[0]
			self.Questions.insert(END,DataToInsert)
		
	def HintSub(self,AnswersGot,HintFrame):
		AnswerToShow = self.AnswersGot[0]
		AnswerToShow = AnswerToShow[0]
		count = 0
		if len(AnswerToShow) != 1:
			randomNumber = random.randrange(0,len(AnswerToShow)-1)
			if len(self.Hints) != len(AnswerToShow):
				for i in range(len(AnswerToShow)):
					self.Hints.append("_")
				while self.Hints[randomNumber] != "_":
					randomNumber = random.randrange(len(AnswerToShow))
				self.Hints[randomNumber] = AnswerToShow[randomNumber]
			elif len(self.Hints) == len(AnswerToShow):
				for i in range(len(AnswerToShow)):
					if self.Hints[i] != "_":
						count += 1
				if count != len(AnswerToShow):
					while self.Hints[randomNumber] != "_":
						randomNumber = random.randrange(len(AnswerToShow))
					self.Hints[randomNumber] = AnswerToShow[randomNumber]
			self.ShowList = Label(HintFrame,text=self.Hints)
			self.ShowList.grid(row=0,column=0)
		else:
			pass

	def checkAnswer(self,QuestionsGot,AnswersGot,OptionsFrame,QuestionsFrame):
		correct = False
		InputtedAnswer = self.Answer.get()
		AnswerTest = str(self.AnswersGot[0])
		AnswerTest = AnswerTest.replace('(','')
		AnswerTest = AnswerTest.replace(',','')
		AnswerTest = AnswerTest.replace(')','')
		AnswerTest = AnswerTest.replace("'","")
		try:
			if str(InputtedAnswer) == AnswerTest:
				self.Questions.delete('1.0',END)
				self.Answer.delete(0,END)
				self.QuestionsGot.pop(0)
				self.AnswersGot.pop(0)
				DataToInsert = self.QuestionsGot[0]
				self.Questions.insert(END,DataToInsert)
				self.ErrorLabel = Label(QuestionsFrame,text="Correct",fg="green").grid(row=1,column=0)
				correct = True	
				self.Hints = []
			else:
				self.ErrorLabel = Label(QuestionsFrame,text="Incorrect",fg="red").grid(row=1,column=0)

		except:
			self.Hints = []
			self.Questions.insert(END,"End of questions")
			self.NoButton = Button(OptionsFrame,text="Exit",command=self.master.destroy,fg="red").grid(row=5,column=0)
			self.YesButton = Button(OptionsFrame,text="Try again",command=self.Repeat).grid(row=4,column=0)
			
	def Repeat(self):
		self.master.destroy()
		Testing = Tk()
		TestingGUI = Test(Testing)

	def goback(self):
		self.master.destroy()
		Window = Tk()
		QandAGUI = QandA(Window)

def main():
	root = Tk()
	app = window(root)
	root.mainloop()

if __name__ == "__main__":
	main()