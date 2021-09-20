#!/usr/bin/python
from __future__ import print_function   # item separators, EOL character
import serial                           # enable serial port      
import datetime                         # time and date functions
from datetime import datetime
import time

from threading import Thread,Event
from subprocess import call

import sched, time

import sqlite3

########################################################

ph_Value = float(0)
temperature_Value = float(0)
moisture_Value = float(0)

#Create a table if there is not a table
def create_sqlite_db():
    conn = sqlite3.connect("Sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tblSensor
                    (Date TEXT,
                    Time TEXT,
                    ph_Value Float,
                    temperature_Value Float,
                    moisture_Value Float)
                    """)
    conn.commit()
    conn.close()

###########################################################

#Delete table
def delete_table():
    connection = sqlite3.connect("Sensor_data.db")
    cursor = connection.cursor()

    cursor.execute("DROP TABLE tblSensor") 
    connection.close()

#####################################################

#Function to receive Arduino sensors' data
#and store to the global variable

def data_change():
    global ph_Value, temperature_Value, moisture_Value 
    
    comport = "/dev/ttyACM0"    # serial port to use
    ser = serial.Serial(comport, baudrate=9600, timeout=20)  
    #ser.open()  # open the serial com port to receive data

    indata = ser.read(15) #receive only 15 bytes 
    print(indata)
    print(type(indata))
    indata = indata.decode('utf-8')
    print(indata)
    if (len(indata) > 0):   # check if there is data
        indata = indata.split(",")  

        ph_Value = indata[0]    
        temperature_Value = indata[1]
        moisture_Value = indata[2]

###########################################################
        
def append_process():
    conn = sqlite3.connect("Sensor_data.db")
    cursor = conn.cursor()

#Create a list type to append to the table
    myRec = []

    #prepare current time 
    now = datetime.now()
    Date_str = now.strftime("%Y-%m-%d")
    Time_str = now.strftime("%H:%M:%S")

    # Append data to list
    myRec.append(Date_str)
    myRec.append(Time_str)
    myRec.append(ph_Value)
    myRec.append(temperature_Value)
    myRec.append(moisture_Value)

#Check for validity and append
    if len(myRec) == 5 and None not in myRec:
        cursor.execute("INSERT INTO tblSensor (Date, Time, ph_Value, temperature_Value, moisture_Value) VALUES (?,?,?,?,?)", myRec)
        print(myRec)
        print("Success")
    else:
        print("Error!")
 
    conn.commit()
    conn.close()

##############################################

#Define function that returns all data in database
def db_all_data():
    con = sqlite3.connect('Sensor_data.db') #dB browser for sqlite needed
    c = con.cursor() #SQLite command, to connect to db so 'execute' method can be called

    c.execute('SELECT * FROM tblSensor') #Select from which ever compound lift is selected

    temp_data = c.fetchall() # Gets the data from the table
    return temp_data

###########################################

#Define function that returns data in database according
#to the user's search criteria

def db_search(column, entry):
    conn = sqlite3.connect("Sensor_data.db")
    cur = conn.cursor()

    if column in {"Date", "Hour"}:
        entry = "'%" + entry + "%'"
    else:
        column = column + "_Value" 
        entry = "'" + entry + "%'"
       
    sql = "SELECT * FROM tblSensor WHERE " + column + " LIKE " + entry
    cur.execute(sql)

    temp_data = cur.fetchall()   
    return temp_data

#########################################

thread1 = None
stop_threads = Event()

def thread_1():
    create_sqlite_db()
    while not stop_threads.is_set():
        global ph_Value, temperature_Value, moisture_Value
        starttime=time.time()
        while True:       
            data_change()
            append_process()
            print(time.time())
            time.sleep(1800.0 - ((time.time() - starttime) % 1800.0))
            starttime+=1800
      
#Run/Stop thread    
def run_thread_1():
    stop_threads.clear()
    thread1 = Thread(target = thread_1)  
    thread1.start()

def stop_thread_1():
    stop_threads.set() 
    thread1 = None

###########################

#Open a new window with instruction
def instruction():
    import tkinter as tk
    root = tk.Tk()
    S = tk.Scrollbar(root)
    S.pack(side=tk.RIGHT, fill=tk.Y)

    text1 = tk.Text(root, height=20, width=60)
    text1.pack(side=tk.LEFT, fill=tk.Y)
    
    S.config(command=text1.yview)
    text1.config(yscrollcommand=S.set)

    #Content of instruction
    quote = """
    This is the Instruction for the program

        1. Intial setup, press the "Delete & Reset" button

        2. To start recording the data, press the "BEGIN record" button to begin serial
           connection and collecting data from the probe

        3. To stop collecting data at any time, press the "STOP record" button

        4. To continue recording data, press the "BEGIN record" button again

        4. The data is saved in a database. To view all, press the "Show All" button

        5. To display data with a specific criteria, refer to the Search bar

        6. With the search bar, choose the criteria from the drop-down list

        7. Type the value in and press the "Search" button

        8. To have a graph, press "Draw graph" button



        For more information, refer to www.myIA.example.com
        """
    text1.insert(tk.END, quote)
    tk.mainloop()




