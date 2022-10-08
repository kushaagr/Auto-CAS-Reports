# Import Module
from tkinter import *

# import filedialog module
from tkinter import filedialog

#import submit
 
# create root window
root = Tk()
list =[]
# root window title and dimension
root.title("AcroCare")
# Set geometry (widthxheight)
root.geometry('450x400')

# all widgets will be here

#adding a label to the root window
#lb1=Input Form 


lbl = Label(root, text = "  Input Form ", background = "white", foreground ="black", 
          font = ("Times New Roman", 15),borderwidth=3, relief="solid")
lbl.grid(column =0, row =0, sticky=W)

#lb2=Surrvey Name
lb2 = Label(root, text = "Survey Name",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))
lb2.grid(column=0, row=1,padx = 5, pady = 10,sticky=W) 
#lb2=survey name
lb2.grid(column=0, row=2,padx = 5, pady = 10,sticky=W)
lb2 = Label(root, text = "Survey Name",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))

 # adding Entry Field 
txt = Entry(root, width=50)
txt.grid(column =0, row =3, sticky=W)

def xyz():
    submit = Tk()


    # root window title and dimension
    submit.title("AcroCare")
    # Set geometry (widthxheight)
    submit.geometry('450x400')
    print(list[0])
    lb1 = Label(submit, text = "You have submitted the information",background = "white", foreground ="black", 
                font = ("Times New Roman", 15))
    lb1.grid(column=0, row=4,padx = 5, pady = 10,sticky=W) 

    submit.mainloop()
          


#lb3=Surrvey Name
lb3 = Label(root, text = "Survey Date / Time",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))
lb3.grid(column=0, row=4,padx = 5, pady = 10,sticky=W) 
#lb3=survey name
lb3.grid(column=0, row=5,padx = 5, pady = 10,sticky=W)
lb3 = Label(root, text = "Survey Date / Time",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))

    # adding Entry Field 
txt = Entry(root, width=50)
txt.grid(column =0, row =6, sticky=W)


#lb4=Institute
lb4 = Label(root, text = "Institute",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))
lb4.grid(column=0, row=7,padx = 5, pady = 10,sticky=W) 
#lb4=Institute
lb4.grid(column=0, row=8,padx = 5, pady = 10,sticky=W)
lb4 = Label(root, text = "Survey Date / Time",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))

 #adding Entry Field 
#txt = Entry(root, width=50)
#txt.grid(column =0, row =9, sticky=W)

#Combobox creation
from tkinter.ttk import *
combo = Combobox(root)
combo['values']= ('AITR', 'AIMSR', 'AIPER', 'AIFMR')
combo.current(3)
combo.grid(column=0, row=9,sticky=W)


#lb5=Department
lb5 = Label(root, text = "Department",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))
lb5.grid(column=0, row=10,padx = 5, pady = 10,sticky=W) 
#lb5=Department
lb5.grid(column=0, row=11,padx = 5, pady = 10,sticky=W)
lb5 = Label(root, text = "Department",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))

          # adding Entry Field 
txt = Entry(root, width=50)
txt.grid(column =0, row =13, sticky=W)


#lb6=Survey File
lb6 = Label(root, text = "Survey File",background = "white", foreground ="black", 
          font = ("Times New Roman", 15))
lb6.grid(column=0, row=14,padx = 5, pady = 10,sticky=W) 

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt"),
                                                       ("all files",
                                                        "*.*")))
    Durva.append(filename)
    filepath.configure(state=NORMAL)
    filepath.delete(0, END)
    filepath.insert(0, filename)
    filepath.configure(state='readonly')
    return filename


filepath = Entry(root, width=50)
filepath.grid(column =0, row =16)
filepath.insert(0, "default text")
filepath.configure(state='readonly')

button_explore = Button(root,
                        text = "Browse Files",
                        command = browseFiles)

                        #adding button to survey file      
button_explore = Button(root,
                        text = "Browse Files", 
                        command = browseFiles)
  

#setting position of browse button
#button_explore.grid(column = 0, row = 16)
  
button_explore.grid(column = 1, row = 16, sticky=W) 




#adding button to survey file      
button_explore = Button(root,
                        text = "Browse Files", 
                        command = browseFiles)

#addding submit button
button = Button(root, text = 'Submit', command=xyz) 
 
button.grid (column=0, row=17, padx = 5, pady = 10 , sticky=W)

#adding check report button
button = Button(root, 
                text = 'Check reports') 
 
button.grid (column=0, row=18, padx = 5, pady = 10,sticky=W)

#adding cancle button
button = Button(root, 
                text = 'Cancle', command=root.destroy) 
 
button.grid (column=0, row=19, padx = 5, pady = 10,sticky=W)
# Execute Tkinter
root.mainloop()