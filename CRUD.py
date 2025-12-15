from tkinter import *
from tkinter import messagebox
import mysql.connector

#Insert Data Function
def insertData():
    #Read the data provied by the user
    id=enterId.get()
    name=enterName.get()
    dept=enterDept.get()
    if(id=="" or name=="" or dept==""):
        #If empty data provided by user
        messagebox.showwarning("Cannot Insert","All the fields are required!")
    else:
        #Insert the data in the empDetails table
        myDB=mysql.connector.connect(host="localhost",user="root",passwd="KFI_117",database="employee")
        myCur=myDB.cursor()
        myCur.execute("insert into empDetails values('"+id+"','"+name+"','"+dept+"')")
        myDB.commit()
        #clear out the entries from the fields filled by user
        enterId.delete(0,"end")
        enterName.delete(0,"end")
        enterDept.delete(0,"end")
        show() #Added call to show the data in Listbox
        messagebox.showinfo("Insert Status","Data Inserted Successfully")
        myDB.close()

#Update Data Function
def updateData():
    #Read the data provided by the user
    id=enterId.get()
    name=enterName.get()
    dept=enterDept.get()
    if(id=="" or name=="" or dept==""):
        #If empty data provided by the user
        messagebox.showwarning("Cannot Update","All the fields are required!")
    else:
        #Update empDetails table
        myDB=mysql.connector.connect(host="localhost",user="root",passwd="KFI_117",database="employee")
        myCur=myDB.cursor()
        myCur.execute("update empDetails set empName='"+name+"', empDept='"+dept+"' where empId='"+id+"'")
        myDB.commit()
        #clear out the entries from the fields filled by user
        enterId.delete(0,"end")
        enterName.delete(0,"end")
        enterDept.delete(0,"end")
        show() #Added call to show the data in Listbox
        messagebox.showinfo("Update Status","Data Updated Successfully")
        myDB.close()

#Get Data Function
def getData():
    if(enterId.get()==""):
        #Combined reading and checking for empty data
        messagebox.showwarning("Fetch Status","Please provide the Emp ID to Fetch the data")
    else:
        #Fill the entry fields from database
        myDB=mysql.connector.connect(host="localhost",user="root",passwd="KFI_117",database="employee")
        myCur=myDB.cursor()
        myCur.execute("select * from empDetails where empID='"+enterId.get()+"'")
        rows=myCur.fetchall()
        #No call required to show the dat ain Listbox as no changes happened
        for row in rows:
            enterName.insert(0,row[1])
            enterDept.insert(0,row[2])
        myDB.close()

#Delete Data Function
def deleteData():
    if(enterId.get()==""):
        #Combined reading and checking of empID data
        messagebox.showwarning("Cannot Delete","Please provide the Emp ID to delete the data")
    else:
        #Delete selected record matching the emp ID
        myDB=mysql.connector.connect(host="localhost",user="root",passwd="KFI_117",database="employee")
        myCur=myDB.cursor()
        myCur.execute("delete from empDetails where empID='"+enterId.get()+"'")
        myDB.commit()
         #clear out the entries from the fields filled by user
        enterId.delete(0,"end")
        enterName.delete(0,"end")
        enterDept.delete(0,"end")
        show() #Added call to show the data in Listbox
        messagebox.showinfo("Delete Status","Data Deleted Successfully")
        myDB.close()

#Show Method
def show():
    myDB=mysql.connector.connect(host="localhost",user="root",passwd="KFI_117",database="employee")
    myCur=myDB.cursor()
    myCur.execute("select * from empDetails")
    rows=myCur.fetchall()
    showData.delete(0,showData.size())
    
    for row in rows:
        addData=str(row[0])+' '+row[1]+' '+row[2]
        showData.insert(showData.size()+1,addData)
    myDB.close()

#Reset Fields Method
def resetFields():
    enterId.delete(0,"end")
    enterName.delete(0,"end")
    enterDept.delete(0,"end")

#GUI Part
#creating parent window
window=Tk()
window.geometry("600x270")
window.title("Employee CRUD App")

#creating labels
empId=Label(window,text="Employee ID",font=("Serif",12))
empId.place(x=20,y=30)

empName=Label(window,text="Employee Name",font=("Serif",12))
empName.place(x=20,y=60)

empDept=Label(window,text="Employee Dept",font=("Serif",12))
empDept.place(x=20,y=90)

#creating Entry boxes
enterId=Entry(window)
enterId.place(x=170,y=30)

enterName=Entry(window)
enterName.place(x=170,y=60)

enterDept=Entry(window)
enterDept.place(x=170,y=90)

#creating Buttons
insertBtn=Button(window,text="Insert",font=("Sans",12),bg="white",command=insertData)
insertBtn.place(x=20,y=160)

updateBtn=Button(window,text="Update",font=("Sans",12),bg="white",command=updateData)
updateBtn.place(x=90,y=160)

getBtn=Button(window,text="Fetch",font=("Sans",12),bg="white",command=getData)
getBtn.place(x=170,y=160)

deleteBtn=Button(window,text="Delete",font=("Sans",12),bg="white",command=deleteData)
deleteBtn.place(x=240,y=160)

resetBtn=Button(window,text="Reset",font=("Sans",12),bg="white",command=resetFields)
resetBtn.place(x=360,y=210)

exitBtn = Button(window, text="Exit", font=("Sans", 12), bg="white", command=window.destroy)
exitBtn.place(x=150, y=210)  # Position it next to the Reset button

#creating Listbox
showData=Listbox(window)
showData.place(x=330,y=30)

show() #Added call to show the data in Listbox after the box is created
window.mainloop()