from tkinter import *
import mysql.connector

root=Tk()                                                                        # Makes Tk window root

sizex = 1000
sizey = 800
root.wm_geometry("%dx%d" % (sizex, sizey))   

contentFrame = Frame(root)
contentFrame.grid(column=0,row=0)

font = ("Helvetica", 20)

SQLport = 8080

SQLdata = ["root","schoolDatabase","10.101.1.140","Project","8080"]
SQLdata = ["PPQD","schoolDatabase","feliximosservers.ddns.net","SigninDatabase","8080"]

SQLinjectionKeyWords = ["DROP TABLE","DROP DATABASE","StudentData","TeacherData","CREATE TABLE","UPDATE TABLE",
                        "AllowSignUp","ClassData","CompletedQuestions","questionData","SetQuestions"
                        ,"StudentsInClass","studentID","classID","SELECT *","'",".",">","<"]

def checkForSQLinjection(string):
    for i in range (0,len(SQLinjectionKeyWords)):
        if SQLinjectionKeyWords[i].upper() in string.upper():
            return("InjectionFound")
    return("InjectionNotFound")

def executeSQLquery(query):
    connection = mysql.connector.connect(user=SQLdata[0], password=SQLdata[1],host=SQLdata[2],database=SQLdata[3],port=int(SQLdata[4]))  
    cursor = connection.cursor()
    cursor.execute(query)
    array = []
    for row in cursor:
        for i in range(0,len(row)):
            array.append(row[i])
    cursor.close()
    connection.close()
    return(array)

def ASKcreateNewPerson(firstName,lastName):
    global startMenuFrame, ASKcreateNewPersonFrame    
    startMenuFrame.destroy()

    ASKcreateNewPersonFrame = Frame(contentFrame)
    ASKcreateNewPersonFrame.grid(row=0,column=0)

    Label(ASKcreateNewPersonFrame,text="You are not currently on the system, would you like to add yourself?", font = ("Helvetica", 20)).grid(row=0,column=0,columnspan=2)

    yes = Button(ASKcreateNewPersonFrame,text="No", font = ("Helvetica", 20),command=ASKcreateNewPersonNO).grid(row=1,column=0)
    no = Button(ASKcreateNewPersonFrame,text="Yes", font = ("Helvetica", 20),command= lambda: ASKcreateNewPersonYES(firstName,lastName)).grid(row=1,column = 1)
    
def ASKcreateNewPersonNO():
    global ASKcreateNewPersonFrame
    ASKcreateNewPersonFrame.destroy()
    createStartMenu()

def ASKcreateNewPersonYES(firstName,lastName):
    global ASKcreateNewPersonFrame
    ASKcreateNewPersonFrame.destroy()    
    createNewPerson(firstName,lastName)

def createNewPerson(pFrame):
    global createNewPersonFrame
    pFrame.destroy()
    
    centeredFrame = Frame(root,highlightbackground="Black", highlightthickness=5)
    centeredFrame.place(relx=.5,rely=.5, anchor="center")    
    createNewPersonFrame = Frame(centeredFrame)
    createNewPersonFrame.grid(row=0,column=0,padx=10,pady=10)

    Label(createNewPersonFrame,text="First Name: ", font = ("Helvetica", 20)).grid(row=1,column=1)
    firstNameEntryBox = Entry(createNewPersonFrame, font = ("Helvetica", 20))
    firstNameEntryBox.grid(row = 1,column = 2)
    
    Label(createNewPersonFrame,text="Second Name: ", font = ("Helvetica", 20)).grid(row=2,column=1)
    lastNameEntryBox = Entry(createNewPersonFrame, font = ("Helvetica", 20))
    lastNameEntryBox.grid(row = 2,column = 2)
    
    Label(createNewPersonFrame,text="PIN: ", font = ("Helvetica", 20)).grid(row=3,column=1)
    pinEntryBox = Entry(createNewPersonFrame, font = ("Helvetica", 20))
    pinEntryBox.grid(row = 3,column = 2)

    Label(createNewPersonFrame,text="RFID: ", font = ("Helvetica", 20)).grid(row=4,column=1)
    RFIDentryBox = Entry(createNewPersonFrame, font = ("Helvetica", 20))
    RFIDentryBox.grid(row = 4,column = 2)

    Button(createNewPersonFrame, text="Enter", font = ("Helvetica", 20),command = lambda:
           addPersonToDatabase(str(firstNameEntryBox.get()),str(lastNameEntryBox.get()),str(pinEntryBox.get()),str(RFIDentryBox.get()),centeredFrame)).grid(row=4,column=3)

def addPersonToDatabase(fn,sn,pin,rfid,pFrame):
    global createNewPersonFrame
    ENDmessage = ""
    if (len(pin) == 4):
        if rfid == "":
            rfid = "0000000000"
            ENDmessage = "No RFID supplied"
            
        connection = mysql.connector.connect(user=SQLdata[0], password=SQLdata[1],host=SQLdata[2],database=SQLdata[3],port=int(SQLdata[4]))  
        cursor = connection.cursor()
        query = ("INSERT INTO studentData "
                "(firstName,lastName,studentPin,studentRFID,totalAttendance,lastAttendedFree,firstSignIn,totalFreePeriodsAvailable,colour,studentMessage)"
                "VALUES ('"+str(fn)+"','"+str(sn)+"','"+str(pin)+"','"+str(rfid)+"""',0,1,0,1,"pink","Have a nice day");""")
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        if ENDmessage == "No RFID supplied":
            pFrame.destroy()
            message("Opperation Successful - No RFID supplied")
        else:
            pFrame.destroy()
            message("Opperation Successful")
    else:
        pFrame.destroy()
        message("Please Enter A 4 Digit Pin")
  
def message(text):    
    messageFrame = Frame(root,highlightbackground="Black", highlightthickness=5)
    messageFrame.place(relx=.5,rely=.5, anchor="center")

    Label(messageFrame,text=text, font = ("Helvetica", 30)).pack()
    root.after(2000,lambda:destroyMessage(messageFrame))
    
def destroyMessage(pFrame):
    pFrame.destroy()
    createStartMenuList()

def ASKeditExistingPerson(data):
    global mainMenuFrame,ASKeditExistingPersonFrame
    mainMenuFrame.destroy()

    editExistingPerson(data)


def editExistingPerson(data,pFrame="Null"):
    global editExistingPersonFrame

    if pFrame != "Null":
        pFrame.destroy()

    centeredFrame = Frame(root,highlightbackground="Black", highlightthickness=5,width=sizex,height=sizey)
    centeredFrame.place(relx=.5,rely=.5, anchor="center")
    
    editExistingPersonFrame = Frame(centeredFrame)
    editExistingPersonFrame.grid(row=0,column=0,padx=10,pady=10)

    changeRFIDFrame = Frame(editExistingPersonFrame)
    changeRFIDFrame.grid(row = 2,column=0,rowspan=4)

    buttonTitlesFrame = Frame(editExistingPersonFrame)
    buttonTitlesFrame.grid(row=1,column=0)

    newRFID = StringVar()
    e = Entry (changeRFIDFrame,textvariable = newRFID,font=font)
    e.grid(row=0,column=1)
    newRFID.set(data[4])

    newColour = StringVar()
    e1 = Entry (changeRFIDFrame,textvariable = newColour,font=font)
    e1.grid(row=1,column=1)
    newColour.set(data[9])

    newPin = StringVar()
    e2 = Entry (changeRFIDFrame,textvariable = newPin,font=font)
    e2.grid(row=2,column=1)
    newPin.set(data[3])

    newMessage = StringVar()
    e3 = Entry (changeRFIDFrame,textvariable = newMessage,font=font)
    e3.grid(row=3,column=1)
    newMessage.set(data[10])

    Label(changeRFIDFrame,font=font,text="Colour Of Name: ").grid(row=1,column=0)
    Label(changeRFIDFrame,font=font,text="RFID Code: ").grid(row=0,column=0)
    Label(changeRFIDFrame,font=font,text="Current PIN: ").grid(row=2,column=0)
    Label(changeRFIDFrame,font=font,text="Personalised Message: ").grid(row=3,column=0)

    buttonFrame = Frame(editExistingPersonFrame,highlightbackground="Black", highlightthickness=2)
    buttonFrame.grid(row = 2, column=1,rowspan=4,padx=5,pady=10)

    Button(buttonFrame,text="Update",font=font,width=18,command = lambda: editExistingPersonFrameUpdate(data,newMessage,newPin,newRFID,newColour,centeredFrame)).grid(row=1,column=1)
    Button(buttonFrame,text="Delete Student",width=18,font=font,command= lambda: askToDeleteStudent(data,centeredFrame)).grid(row=2,column=1)
    Button(buttonFrame,text="Check pin",width=18,font=font,command= lambda: checkPinUnique(data,centeredFrame,newPin.get())).grid(row=3,column=1)

def checkPinUnique(data,pFrame,newPin):
    connection = mysql.connector.connect(user=SQLdata[0], password=SQLdata[1],host=SQLdata[2],database=SQLdata[3],port=int(SQLdata[4]))  
    cursor = connection.cursor()
    query = ("SELECT * FROM studentData WHERE studentPin = '" + str(newPin) + "'")
    cursor.execute(query)
    count = 0
    for row in cursor:
        count=count+1

    if count < 2:
        top = Toplevel()
        top.title("Sucess Message")
        centeredFrameTOP = Frame(top,highlightbackground="Black", highlightthickness=0)
        centeredFrameTOP.place(relx=.5,rely=.5, anchor="center")
        Label(centeredFrameTOP,font=font,text="Pin Is Unique").grid(row=0,column=0)
        Button(centeredFrameTOP,font=font,text="Ok",command=lambda:top.destroy()).grid(row=1,column=0)
    else:
        top = Toplevel()
        top.title("Error Message")
        centeredFrameTOP = Frame(top,highlightbackground="Black", highlightthickness=0)
        centeredFrameTOP.place(relx=.5,rely=.5, anchor="center")
        Label(centeredFrameTOP,font=font,text="Pin NOT Unique").grid(row=0,column=0)
        Button(centeredFrameTOP,font=font,text="Ok",command=lambda:top.destroy()).grid(row=1,column=0)
    


def askToDeleteStudent(data,pFrame):
    pFrame.destroy()
    centeredFrame = Frame(root,highlightbackground="Black", highlightthickness=5)
    centeredFrame.place(relx=.5,rely=.5, anchor="center")
    Label(centeredFrame,font=font,text="Are you sure you want to delete\n"+str(data[1]) + " " + str(data[2]) + "\npermanently?").grid(row=0,columnspan=2,column=0,padx=10,pady=10)
    Button(centeredFrame,font=font,text="No",command=lambda:studentNotDeleted(data,centeredFrame)).grid(row=1,column=0,padx=10,pady=10)
    Button(centeredFrame,font=font,text="Yes",command=lambda:deleteStudent(data,centeredFrame)).grid(row=1,column=1,padx=10,pady=10)

def studentNotDeleted(data,pFrame):
    pFrame.destroy()
    message("Student Not Deleted")

def deleteStudent(data,pFrame):
    pFrame.destroy()
    
    connection = mysql.connector.connect(user=SQLdata[0], password=SQLdata[1],host=SQLdata[2],database=SQLdata[3],port=int(SQLdata[4]))  
    cursor = connection.cursor()
    query = ("DELETE FROM freePeriods WHERE studentID = " + str(data[0]))
    cursor.execute(query)
    connection.commit()
    query = ("DELETE FROM studentData WHERE studentID = " + str(data[0]))
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()        
    message("Student Deleted")

def editExistingPersonFrameUpdate(data,newMessage,newPin,newRFID,newColour,pFrame):
    global editExistingPersonFrame
    pFrame.destroy()

    if (checkForSQLinjection(newMessage.get()) == "InjectionNotFound") and (checkForSQLinjection(newPin.get()) == "InjectionNotFound") and (checkForSQLinjection(newColour.get()) == "InjectionNotFound"):
        
        connection = mysql.connector.connect(user=SQLdata[0], password=SQLdata[1],host=SQLdata[2],database=SQLdata[3],port=int(SQLdata[4]))  
        cursor = connection.cursor()
        query = ("DELETE FROM freePeriods WHERE studentID = " + str(data[0]))
        cursor.execute(query)
        connection.commit()

        messageToSend = "Successfully Updated Database"

        valuesData = []

        if len(str(newRFID.get())) == 10:
            query = ("UPDATE studentData SET studentRFID = " + str(newRFID.get()) + " WHERE studentID = " + str(data[0]))
            cursor.execute(query)
            connection.commit()
        else:
            messageToSend = "WARNING! \nINCORECT RFID CODE SUPPLIED"

        query = ('UPDATE studentData SET colour = "' + str(newColour.get()) + '" WHERE studentID = ' + str(data[0]))
        cursor.execute(query)
        connection.commit()

        query = ('UPDATE studentData SET studentPin = "' + str(newPin.get()) + '" WHERE studentID = ' + str(data[0]))
        cursor.execute(query)
        connection.commit()

        query = ('UPDATE studentData SET studentMessage = "' + str(newMessage.get()) + '" WHERE studentID = ' + str(data[0]))
        cursor.execute(query)
        connection.commit()
        
        cursor.close()
        connection.close()

        editExistingPersonFrame.destroy()

        message(messageToSend)
    else:
        useOnlyCharsMessage(data)

def useOnlyCharsMessage(data):
    errorScreenFrame = Frame(contentFrame,width=sizex,height=sizey)
    errorScreenFrame.pack()
    centeredFrame = Frame(errorScreenFrame,highlightbackground="Black", highlightthickness=5)
    centeredFrame.place(relx=.5,rely=.5, anchor="center")
    Label(centeredFrame,font=(font[0], int(font[1]*2)),text="Error").grid(row=0,column=0,padx=10,pady=10)
    Label(centeredFrame,font=font,text="Please use only characters A-Z\n and the numbers 0-9").grid(row=1,column=0,padx=10,pady=10)
    root.after(2000,lambda: editExistingPerson(data,errorScreenFrame))    


def ASKeditExistingPersonFrameCANCEL():
    global ASKeditExistingPersonFrame
    ASKeditExistingPersonFrame.destroy()
    createStartMenu()

def editScreen(nameOfStudent):
    global firstNameEntryBox, secondNameEntryBox
    name = nameOfStudent.split(" ")
    
    firstName = name[0]
    secondName= name[1]
        
    query = str('SELECT * FROM studentData WHERE firstName = "' + str(firstName) + '" AND lastName = "' + str(secondName) + '"')

    data = (executeSQLquery(query))

    ASKeditExistingPerson(data)   

def askStartQuestion():
    mainMenuFrame2 = Frame(root,highlightbackground="Black", highlightthickness=5)
    mainMenuFrame2.place(relx=.5,rely=.5, anchor="center")
    Label(mainMenuFrame2,font=font,text="Are you at home or school?").grid(row=0,column=0,columnspan=2,padx=10,pady=10)
    Button(mainMenuFrame2,font=font,text="School",command=lambda: setSQL("School",mainMenuFrame2)).grid(row=1,column=0,padx=10,pady=10)
    Button(mainMenuFrame2,font=font,text="Home",command=lambda: setSQL("Home",mainMenuFrame2)).grid(row=1,column=1,padx=10,pady=10)

def setSQL(place,pFrame):
    global SQLdata
    if place == "Home":
        SQLdata = ["PPQD","schoolDatabase","feliximosservers.ddns.net","SigninDatabase","8080"]
    else:
        SQLdata = ["root","schoolDatabase","10.101.1.140","Project","8080"]
    pFrame.destroy()
    createStartMenuList()

def createStartMenuList():
    global contentsFrame, movingCanvas, frame, scrollbar, frame2, mainMenuFrame

    mainMenuFrame = Frame(root,highlightbackground="Black", highlightthickness=5)
    mainMenuFrame.place(relx=.5,rely=.5, anchor="center")    
    
    Label(mainMenuFrame,font=font,text="Manage A Student").grid(row=1,column=1)
    contentsFrame=Frame(mainMenuFrame,relief=GROOVE,width=200,height=400,bd=5)                 #makes frame containing canvas and frame placed on canvas
    contentsFrame.grid(column=1,row=2,rowspan=2,padx=10,pady=10)
    movingCanvas=Canvas(contentsFrame)                                                                               # Makes a canvas on the contents frame
    frame=Frame(movingCanvas)                                                                                        # Makes another frame on that canvas
                                                                                                                     # Items places on this canvas will scroll with the bar
    scrollbar=Scrollbar(contentsFrame,orient="vertical")                                # Places vertical scrollbar on side of contents frame
    movingCanvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.config(command=movingCanvas.yview)                                                             # binds moving the scrollbar to moving the canvas
    scrollbar.pack(side="right",fill="y")                                                                          # packs the scrollbar
    movingCanvas.pack(side="left")                                                                                   # packs the canvas on the left (sticky to scrollbar)
    movingCanvas.create_window((0,0),window=frame,anchor='nw')                                                       # Creates the window
    frame.bind("<Configure>",moveWhenScrolled)                                                                       # Binds any change to the scrollbar to move canvas
    
    frame2 = Frame(frame)                                                                                            #Temporary frame, made to easily delete buttons already made
    frame2.pack()

    updateButtons("active")

    Button(mainMenuFrame,font=font,command= lambda: createNewPerson(mainMenuFrame),text="Create New Student").grid(row=2,column=2,padx=10,pady=10)
    

def moveWhenScrolled(event):
    global SOcontentsFrame, SOmovingCanvas, SOframe, SOscrollbar, SOframe2
    movingCanvas.configure(scrollregion=movingCanvas.bbox("all"),width=400,height=600)

def updateButtons(enabled):
    global frame2,listOfNames
    connection = mysql.connector.connect(user=SQLdata[0], password=SQLdata[1],host=SQLdata[2],database=SQLdata[3],port=int(SQLdata[4]))  
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM studentData WHERE 1 \nORDER BY firstName;")
    listOfNames = []
    for row in cursor:
        listOfNames.append(str(str(row[1]) + " " + str(row[2])))
        
    cursor.close()
    connection.close()
    
    disableScrolling = True
    frame2.destroy()
    frame2=Frame(frame)
    frame2.pack()
    for i in range(0,len(listOfNames)):
       Button(frame2,text=str(listOfNames[i]),font=("Helvetica", 16),command=lambda i=i:editScreen(listOfNames[i])
              ,width=30,state=enabled).grid(row=i,column=1)

askStartQuestion()
root.mainloop()
