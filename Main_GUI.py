import tkinter as tk
from tkinter import ttk
import matplotlib

import sqlite3 as sq

import db_and_connect as module_1
import draw_graph as module_2

#########################################

#Full screen options
def toggle_fullscreen(self):
    root.attributes('-fullscreen', True)

def end_fullscreen(self):
    root.attributes('-fullscreen', False)

# Table functions
current_data = []

def show_current_data():
    #Update treeview with data being stored in current_data = []

    global current_data
    my_GUI.tree.delete(*my_GUI.tree.get_children()) #Delete data currently being displayed
    
    for val in current_data:
        my_GUI.tree.insert('', 'end', values = (val[0], val[1], val[2], val[3], val[4]) )
        
def show_all_data():
    #Update the treeview all the data in the database
    
    global current_data
    current_data = []
    
    temp_data = module_1.db_all_data()
    
    for row in temp_data:
        current_data.insert(1,row) #Update list current_data

    show_current_data()
        
def search_criteria():
    #Take the user search criteria and update
    #the tree accordingly
    
    global current_data
    current_data = []
    combobox_1_data = my_GUI.combobox_1.get()
    entry_1_data = my_GUI.entry_1.get() #Register the user's option

    temp_data = module_1.db_search(combobox_1_data, entry_1_data) #Search in database

    for row in temp_data:
        current_data.insert(1,row) #Update list current_data
    show_current_data()

def draw_a_chart():
    module_2.draw_graph(current_data)
    
#Export CSV file

def export_csv():
    with open('csv_test_1.csv', 'w+') as write_file:       
        for row in current_data:
            row = str(row)
            # Removing unnecessary brackets
            temp_row = row.split('(') #Remove (
            temp_row = temp_row[1]
            
            temp_row = temp_row.split(')') #Remove )
            temp_row = temp_row[0]

            row = "\n" + temp_row 
            write_file.write(row)
 
def delete_reset():
    global current_data
    current_data = []
    show_current_data()
     
    module_1.delete_table()
     

############################################

# MAIN GUI

root = tk.Tk()

class GUI:
    def __init__(self, master):
        
# General configure 
        self.master = master
        master.title("NAM'S DAQ: Data Acquisition System ")

        self.label_1 = ttk.Label(master, text="Data Acquisition System!")
        self.label_1.grid(column=0, row=0, sticky="n", pady=5)

        self.button_1 = ttk.Button(master, text="HELP ME", command=module_1.instruction)
        self.button_1.grid(column=2, row=0, padx=10, ipadx=30, ipady = 5)
        
# Config the table display

# frame 1: tk treeview and table
        self.frame_1 = ttk.Frame(master)
        self.frame_1.grid(column=0, row=1, sticky="w")
        
        self.tree = ttk.Treeview(self.frame_1, columns = (1,2,3,4,5), height = 15, selectmode="extended", show = "headings", ) # To choose all data, hold sfhift or ctrl
        self.tree.grid()

        #5 type of value: Date, time, ph_Value, temperature_Value, moisture_Value
        self.tree.column(1, width = 120)
        self.tree.column(2, width = 120)
        self.tree.column(3, width = 120)
        self.tree.column(4, width = 120)
        self.tree.column(5, width = 120)
        
        self.tree.heading(1, text="Date")
        self.tree.heading(2, text="Time")
        self.tree.heading(3, text="pH (0-14)")
        self.tree.heading(4, text="Temp.(C)")
        self.tree.heading(5, text="Moisture (%)")

        self.scroll = ttk.Scrollbar(self.frame_1, orient="vertical", command=self.tree.yview)
        self.scroll.grid(column=1, row=0, sticky='ns')
        
        self.tree.configure(yscrollcommand=self.scroll.set)


# Config the options and buttons

# frame 2: options on the right-hand side 
        self.frame_2 = ttk.Frame(master)
        self.frame_2.grid(column=2, row=1, sticky="n")

        self.button_1 = ttk.Button(self.frame_2, text="Show All", command=show_all_data)
        self.button_1.grid(column=0, row=0, padx=10, ipadx=30)

        self.button_2 = ttk.Button(self.frame_2, text="Draw Graph", command=draw_a_chart)
        self.button_2.grid(column=0, row=1, padx=10, pady=5, ipadx=30)

        self.button_3 = ttk.Button(self.frame_2, text="Export to CSV file", command=export_csv)
        self.button_3.grid(column=0, row=2, padx=10, ipadx=17)

        self.button_4 = ttk.Button(self.frame_2, text="BEGIN record", command=module_1.run_thread_1)
        self.button_4.grid(column=0, row=3, padx=10, pady=20, ipady=10, ipadx=30)

        self.button_5 = ttk.Button(self.frame_2, text="STOP record", command=module_1.stop_thread_1)
        self.button_5.grid(column=0, row=4, padx=10, ipady=10, ipadx=30)

        self.button_5 = ttk.Button(self.frame_2, text="DELETE & RESET record", command=delete_reset)
        self.button_5.grid(column=0, row=5, padx=10, pady=20, ipadx=2, ipady=10)
        
# frame 3: Criteria search bar
        self.frame_3 = ttk.LabelFrame(master, height=150, width=450, text="Search with specific criteria")
        self.frame_3.grid(column=0, row=3, sticky="w", pady=20)
        
        self.label_2 = ttk.Label(self.frame_3, text=" Column ")
        self.label_2.grid(column=0, row=1, pady=5)
       
        self.combobox_1 = ttk.Combobox(self.frame_3, width=10, state="readonly", value=("Date", "Time", "ph", "Temperature", "Moisture")) 
        self.combobox_1.set("Date")
        self.combobox_1.grid(column=1, row=1, pady=5) # Drop-down menu

        self.label_3 = ttk.Label(self.frame_3, text=" Value ")
        self.label_3.grid(column=2, row=1, pady=10)        

        self.entry_1 = ttk.Entry(self.frame_3, width=15)
        self.entry_1.grid(column=3, row=1, pady=10) # Entry data

        self.label_4 = ttk.Label(self.frame_3, text=" : ")
        self.label_4.grid(column=4, row=1, pady=10)

        self.button_2 = ttk.Button(self.frame_3, width=10, text="Search", command=search_criteria) # Show only
        self.button_2.grid(column=5, row=1)
        
#Full-screen mode        
        self.master.bind("<F11>", toggle_fullscreen)
        self.master.bind("<Escape>", end_fullscreen)
        
    
###########################################
        
my_GUI = GUI(root)
root.mainloop()
