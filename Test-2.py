import tkinter as tk
from tables import Table


from tkinter import ttk
import sqlite3


LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, ReceivedMessages, SentMessages,Groups,Settings,Account):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Groups)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
def Database():
    global conn, cursor
    NEW_USERNAME = 'admin'
    NEW_PASSWORD = 'admin'
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `users` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `groups` (group_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, group_name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `sent_messages` (message_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,contact INTEGER, message VARCHAR(250) NOT NULL,  status VARCHAR(50) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `received_messages` (message_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,contact INTEGER, message VARCHAR(250) NOT NULL,  status VARCHAR(50) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'profiles' (profile_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  profile_name VARCHAR(50) NOT NULL, received_from VARCHAR(50) NOT NULL, amount INTEGER NOT NULL, profile_group VARCHAR(50) NOT NULL, profile_message VARCHAR(50) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'user_credentials' (credential_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  credential_group VARCHAR(50) NOT NULL, user_name VARCHAR(50) NOT NULL, password TEXT NOT NULL, FOREIGN KEY(credential_id) REFERENCES groups(group_id))")
    cursor.close()
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM users")
    
    print(cursor.fetchone())
    if cursor.fetchone() is None:
       print("does not exist")
       print(cursor.fetchall())
       cursor.execute("INSERT INTO `users` (username, password) VALUES(?, ?)", (NEW_USERNAME,NEW_PASSWORD,))
       conn.commit() 
    else:
        print("exists")

    cursor.close()
    cursor = conn.cursor()
    
class LoginPage(tk.Frame):
    Database()
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.USERNAME = tk.StringVar()
        self.PASSWORD = tk.StringVar()
        self.lbl_text = tk.Label(self)
        self.lbl_text.place(x=400, y=80)
        
        label_0 = tk.Label(self,  text="User login",width=20,font=("bold", 20))
        label_0.place(x=400,y=50)
  
  
        label_1 = tk.Label(self, text="User name",width=20,font=("bold", 10))
        label_1.place(x=400, y=100)
  
        entry_1 = tk.Entry(self, textvariable=self.USERNAME)
        entry_1.place(x=400,y=150)
  
        label_2 = tk.Label(self,  text="Password",width=20,font=("bold", 10))
        label_2.place(x=400,y=200)
  
        entry_2 = tk.Entry(self, textvariable=self.PASSWORD, show = "*")
        entry_2.place(x=400,y=250)
        button2 = tk.Button(self, text="Login",
                            command=self.Login)
        button2.place(x=400, y=300)

    def Login(self, event=None):
            Database()
            print(self.USERNAME.get())
            if self.USERNAME.get() == "" or self.PASSWORD.get() == "":
                self.lbl_text.config(text="Please complete the required field!", fg="red")
            else:
                row = cursor.execute("SELECT * FROM `users` WHERE `username` = ? AND `password` = ?", (self.USERNAME.get(), self.PASSWORD.get()))
                
                if cursor.fetchone() is None: 
                   self.lbl_text.config(text="Invalid username and password for initial use,contact developer", fg="red")
                   self.USERNAME.set("")
                   self.PASSWORD.set("")
                else:
                    print("data")
                    logged_in()
           

                    
                     
                  

       

class ReceivedMessages(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

  
        self.tree = ttk.Treeview(self, columns=("Contact", "Message", "Status"), selectmode="extended", height=15)
        self.tree.place(x=300,y=50)
        
        self.tree.heading('Contact', text="Contact", anchor=tk.W)
        self.tree.heading('Message', text="Message", anchor=tk.W)
        self.tree.heading('Status', text="Status", anchor=tk.W)
        self.tree.column('#0',  minwidth=0, width=0)
        self.tree.column('#1',  minwidth=0, width=100)
        self.tree.column('#2',  minwidth=0, width=400)
        self.tree.column('#3',  minwidth=0, width=100)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        cursor.execute("SELECT * FROM `received_messages` ")
        
        check = cursor.fetchone()
        cursor.execute("SELECT * FROM `received_messages` ")
        fetch = cursor.fetchall()
        
        if check is None:
           print("nothing")
           message_canvas = tk.Canvas(self, width=600, height=320)
           message_canvas.place(x=300,y=50)
           message_canvas.create_rectangle(10, 10, 1000, 5000, fill='')
           mycanvas_label = message_canvas.create_text((250, 180), text="(Received Messages will display here)")
           
        else:
            print("some messages availablejd")
            #print(fetch)
            for data in fetch:
               #print("sda") 
               #print(data)
               #print("sda2") 
               #print(data[2][0:100])
               self.tree.insert('', 'end', values=(data[1], data[2][0:52] + '........', data[3]), )
               
   

        self.canvas = tk.Canvas(self, width=600, height=120)
        self.canvas.place(x=300,y=350)
        self.canvas.create_rectangle(10, 10, 1000, 5000, fill='')
   
        self.mylabel = self.canvas.create_text((250, 80), text="(Selected contact received message displays here)")

        refresh_button = tk.Button(self,width=18,height=2, text="Refresh",
                            command=lambda: controller.show_frame(PageOne))
        refresh_button.place(x=450, y=500)

        resend_button = tk.Button(self,width=18,height=2, text="Resend",
                            command=lambda: controller.show_frame(PageOne))
        resend_button.place(x=630, y=500)

        delete_button = tk.Button(self,width=18,height=2, text="Delete",
                            command=lambda: controller.show_frame(PageOne))
        delete_button.place(x=800, y=500)
        
        receivedmessages_button = tk.Button(self,width=25,height=3, bg="#FF5733", text="Received Messages",
                            command=lambda: controller.show_frame(ReceivedMessages))
        receivedmessages_button.place(x=30, y=50)

        sentmessages_button = tk.Button(self,width=25,height=3, bg="#737271", text="Sent Messages",
                            command=lambda: controller.show_frame(SentMessages))
        sentmessages_button.place(x=30, y=130)
         
        groups_button = tk.Button(self,width=25,height=3, bg="#737271", text="Groups",
                            command=lambda: controller.show_frame(Groups))
        groups_button.place(x=30, y=200)

        
        settings_button = tk.Button(self,width=25,height=3, bg="#737271", text="Settings",
                            command=lambda: controller.show_frame(Settings))
        settings_button.place(x=30, y=270)

       
       
        logout_button = tk.Button(self,width=7,height=1,text="logut"
                            )
        logout_button.place(x=10, y=500)

        mainsetting_button = tk.Button(self,width=7,height=1, text="Security", command=lambda: controller.show_frame(Account)
                            )
        mainsetting_button.place(x=100, y=500)
        
        
    def on_select(self, event):
              self.canvas.delete(tk.ALL)
              self.canvas.create_rectangle(10, 10, 1000, 5000, fill='')
              curItem = self.tree.focus()
              
              #print(self.tree.item(curItem)['values'][1])
              keyword = self.tree.item(curItem)['values'][1][0:10]
              cursor.execute("SELECT message FROM `received_messages` WHERE message LIKE ?", (keyword+'%',))
        
              selected_message = cursor.fetchone()
              
              mylabel = self.canvas.create_text((250, 80), text=selected_message[0])
              


              
              
class SentMessages(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        self.group_name = tk.StringVar()
        self.tree = ttk.Treeview(self, columns=("Contact", "Message", "Status"), selectmode="extended", height=15)
        self.tree.place(x=300,y=50)
        
        self.tree.heading('Contact', text="Contact", anchor=tk.W)
        self.tree.heading('Message', text="Message", anchor=tk.W)
        self.tree.heading('Status', text="Status", anchor=tk.W)
        self.tree.column('#0',  minwidth=0, width=0)
        self.tree.column('#1',  minwidth=0, width=100)
        self.tree.column('#2',  minwidth=0, width=400)
        self.tree.column('#3',  minwidth=0, width=100)
        cursor.execute("SELECT * FROM `received_messages` ")
        
        
        fetch = cursor.fetchall()
        
        for messages in fetch:
          
          
           test_string = messages[2]
 
           # initializing split word which is ksh 
           spl_word = 'ksh'
  
           # printing original string  
           #print("The original string : " + str(test_string)) 
  
           # printing split string  
           #print("The split string : " + str(spl_word)) 
  
           # using partition() 
           # Get String after substring occurrence 
           res = test_string.partition(spl_word)[2]
           print(res)

           if res.split()[5].isnumeric():
                print("my friend this is a phone number")
                amount = res.split()[0]
                sender_name = res.split()[2] + ' ' + res.split()[3] + ' ' + res.split()[4]
                sender_number = res.split()[5]
                date = res.split()[7]
                time = res.split()[9]

           else:
                print("contains only two names")
                amount = res.split()[0]
                sender_name = res.split()[2] + ' ' + res.split()[3]
                sender_number = res.split()[4]
                date = res.split()[6]
                time = res.split()[8] 
           print (amount)
           print (sender_name)
           print (sender_number)
           print (date)
           print (time)
           sender = "M-pesa"
           

           cursor.execute("SELECT profile_group, profile_message FROM `profiles` WHERE received_from = ? AND amount = ?", (sender, amount))
           fetch = cursor.fetchall()
           print("jkv")
           print(fetch)
        
        check = cursor.fetchone()
        fetch = cursor.fetchall()
        if check is None:
           print("nothing")
        else:
            print("some messages available")
        for data in fetch:
         
          self.tree.insert('', 'end', values=(data[2], data[3]))

        canvas = tk.Canvas(self, width=600, height=120)
        canvas.place(x=300,y=350)
        canvas.create_rectangle(10, 10, 1000, 5000, fill='')
   
        mylabel = canvas.create_text((250, 80), text="(Selected contact sent message displays here)")

        refresh_button = tk.Button(self,width=18,height=2, text="Refresh")
        refresh_button.place(x=450, y=500)

        resend_button = tk.Button(self,width=18,height=2, text="Resend"
                           )
        resend_button.place(x=630, y=500)

        delete_button = tk.Button(self,width=18,height=2, text="Delete"
                            )
        delete_button.place(x=800, y=500)
        
        receivedmessages_button = tk.Button(self,width=25,height=3,  bg="#737271", text="Received Messages",
                            command=lambda: controller.show_frame(ReceivedMessages))
        receivedmessages_button.place(x=30, y=50)

        sentmessages_button = tk.Button(self,width=25,height=3,bg="#FF5733", text="Sent Messages",
                            command=lambda: controller.show_frame(SentMessages))
        sentmessages_button.place(x=30, y=130)
         
        groups_button = tk.Button(self,width=25,height=3, bg="#737271", text="Groups",
                            command=lambda: controller.show_frame(Groups))
        groups_button.place(x=30, y=200)

        
        settings_button = tk.Button(self,width=25,height=3, bg="#737271", text="Settings",
                            command=lambda: controller.show_frame(Settings))
        settings_button.place(x=30, y=270)

        
        logout_button = tk.Button(self,width=7,height=1,text="logut"
                            )
        logout_button.place(x=10, y=500)

        mainsetting_button = tk.Button(self,width=7,height=1, text="Security", command=lambda: controller.show_frame(Account)
                            )
        mainsetting_button.place(x=100, y=500)

class Groups(tk.Frame):
    Database()
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
       
        self.GROUP_NAME = tk.StringVar()
        self.USER_NAME = tk.StringVar()
        self.PASSWORD = tk.StringVar()
        self.lbl_text = tk.Label(self)
        self.lbl_text.place(x=300, y=160)
        
        sentmessages_button = tk.Button(self,width=25,height=3, bg="#737271", text="Received Messages",
                             command=lambda: controller.show_frame(ReceivedMessages))
        sentmessages_button.place(x=30, y=50)
        
        receivedmessages_button = tk.Button(self,width=25,height=3, bg="#737271", text="Sent Messages",
                            command=lambda: controller.show_frame(SentMessages))
        receivedmessages_button.place(x=30, y=130)

         
        groups_button = tk.Button(self,width=25,height=3, bg="#FF5733", text="Groups",
                            command=lambda: controller.show_frame(Groups))
        groups_button.place(x=30, y=200)

        
        settings_button = tk.Button(self,width=25,height=3, bg="#737271", text="Settings",
                            command=lambda: controller.show_frame(Settings))
        settings_button.place(x=30, y=270)
  
        groupadd_entry = tk.Entry(self, textvariable = self.GROUP_NAME, width=20, font=("bold", 13))
        groupadd_entry.place(x=250,y=70)

        add_button = tk.Button(self,width=10,height=1, bg="#737271", text="ADD",
                            command = self.add_group)
        add_button.place(x=450, y=70)

        label_0 = tk.Label(self, text="Available groups",width=20,font="Verdana 15 underline")
        label_0.place(x=300,y=130)

        remove_button = tk.Button(self,width=13,height=1, bg="#737271", text="Remove",
                            command=self.del_group )
        remove_button.place(x=450, y=500)

        self.group_name = tk.Label(self, text="(Selected Group name here)",font="Verdana 10 underline")
        self.group_name.place(x=650,y=90)

        """self.table = Table(self, ["Username", "Password", "Status"],height = 250, column_minwidths=[150, 150, 70])"""
       
        
        """"table.set_data([[1,4,3],[4,5,6], [7,8,9], [10,11,12]])
        table.cell(0,0, "First message")
        table.cell(1,0, "Second message")
        table.cell(1,1, " message")"""
        self.listbox = tk.Listbox(self, width =30, font=("", 13))
        self.listbox.place(x=270, y=230)
        self.listbox.bind('<<ListboxSelect>>',self.CurSelet)

        
        

       
        self.tree = ttk.Treeview(self, columns=("Username", "Password", "Status"), selectmode="extended", height=100)
        self.tree.place(x=580,y=150)
        
        self.tree.heading('Username', text="Username", anchor=tk.W)
        self.tree.heading('Password', text="Password", anchor=tk.W)
        self.tree.heading('Status', text="Status", anchor=tk.W)
        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=tk.NO, minwidth=0, width=130)
        self.tree.column('#2', stretch=tk.NO, minwidth=0, width=100)
        self.tree.column('#3', stretch=tk.NO, minwidth=0, width=100)
       
        username_entry = tk.Entry(self, textvariable = self.USER_NAME, font=("", 10))
        username_entry.place(x=600,y=440)

        password_entry = tk.Entry(self, textvariable = self.PASSWORD, font=("", 10))
        password_entry.place(x=750,y=440)

        warning_label = tk.Label(self, text = "Enter Password and username here")
        warning_label.place(x = 750, y=470)
        upload_button = tk.Button(self,width=13,height=1, bg="#737271", text="Upload"
                            )
        upload_button.place(x=700, y=500)

        update_button = tk.Button(self,width=13,height=1, bg="#737271", text="Update",
                           command=self.add_credentials )
        update_button.place(x=850, y=500)

        
        logout_button = tk.Button(self,width=7,height=1,text="logout"
                            )
        logout_button.place(x=10, y=500)

        mainsetting_button = tk.Button(self,width=7,height=1, text="Security", command=lambda: controller.show_frame(Account)
                            )
        mainsetting_button.place(x=100, y=500)

        self.listbox = tk.Listbox(self, width =30, font=("", 13))
        self.listbox.place(x=270, y=230)
        self.listbox.bind('<<ListboxSelect>>',self.CurSelet)

        rows = 0
        group_list = []
        cursor = conn.cursor()
        row = cursor.execute("SELECT group_name FROM groups")
        groups = row.fetchall()
        
        print(groups)
        rows = 0
        for users in groups:
             print(rows)
             self.listbox.insert(tk.END, groups[rows])
             rows= rows+1
    def CurSelet(self, event):
       widget = event.widget
       selection=widget.curselection()
       self.picked = widget.get(selection[0])
       self.group_name.config(text=self.picked)
       print("picked")
       print(self.picked)
       """
       self.table.clear()
       highlighted = 'montly'
       cursor = conn.cursor()
       row = cursor.execute("SELECT user_name, password FROM user_credentials WHERE credential_group = ?", (highlighted,))
       #print(row.fetchall())
       rows = row.fetchall()
       for details in rows:
          print(details)
          self.table.insert_row([details[0],details[1]])"""
       highlighted = self.listbox.get(tk.ANCHOR)
       self.tree.delete(*self.tree.get_children())
       print(highlighted)
    
       cursor.execute("SELECT * FROM `user_credentials` WHERE credential_group = ?", (highlighted[0],))
       fetch = cursor.fetchall()
       for data in fetch:
          print("sda") 
          print(data)
          self.tree.insert('', 'end', values=(data[2], data[3]))
        
    def add_group(self):
         highlighted = self.listbox.get(tk.ANCHOR)
         
         cursor2 = conn.cursor()
         cursor2.execute("SELECT * FROM groups WHERE group_name = ? GROUP BY group_name", (self.GROUP_NAME.get(),))
         
        
         if self.GROUP_NAME.get() == "":
           self.lbl_text.config(text="Please complete the required fields !!!", fg="red")
         else:
            if cursor2.fetchone() is None:
              cursor2.close()
              cursor = conn.cursor()
              cursor.execute("INSERT INTO `groups` (group_name) VALUES(?)", (self.GROUP_NAME.get(),))
              conn.commit()
              self.lbl_text.config(text="Added group successfully", fg="green")
              
              self.listbox.insert(tk.END, self.GROUP_NAME.get())
              
            else:
              self.lbl_text.config(text="A group with same name already exists", fg="red")
    
    def del_group(self):
        highlighted_group = self.listbox.get(tk.ANCHOR)
        selected_items = self.tree.selection()        
        print(highlighted_group[0])         
        #self.tree.delete(highlighted_group[0])
        cursor.execute( "DELETE FROM groups WHERE group_name=?", (highlighted_group[0],) )
        cursor.execute( "DELETE FROM user_credentials WHERE credential_group = ?", (highlighted_group[0],) )
        conn.commit()

    def add_credentials(self):
         print(self.USER_NAME)
         highlighted_group = self.listbox.get(tk.ANCHOR)
         print("shown")
         print(highlighted_group[0])
         if self.USER_NAME == "" or self.PASSWORD == "":
             warning_label.config(text = "Please fill the credentials", fg = "red")

         else:
             cursor.execute("INSERT INTO `user_credentials` (credential_group, user_name, password) VALUES(?, ?, ?)", (highlighted_group[0], self.USER_NAME.get(), self.PASSWORD.get(),))
             conn.commit()
             self.tree.insert('', 'end', values=(self.USER_NAME.get(), self.PASSWORD.get()))
             
             print("succes")
             
             
    

class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.PROFILE_NAME = tk.StringVar()
        self.RECEIVE_FROM = tk.StringVar()
        self.AMOUNT = tk.IntVar()
        self.GROUP = tk.StringVar()
        self.MESSAGE = tk.StringVar()
    
        receivedmessages_button = tk.Button(self,width=25,height=3, bg="#737271", text="Received Messages",
                             command=lambda: controller.show_frame(ReceivedMessages))
        receivedmessages_button.place(x=30, y=50)
        
        sentmessages_button = tk.Button(self,width=25,height=3, bg="#737271", text="Sent Messages",
                            command=lambda: controller.show_frame(SentMessages))
        sentmessages_button.place(x=30, y=130)

         
        groups_button = tk.Button(self,width=25,height=3, bg="#737271", text="Groups",
                            command=lambda: controller.show_frame(Groups))
        groups_button.place(x=30, y=200)

        
        settings_button = tk.Button(self,width=25,height=3,bg="#FF5733", text="Settings",
                            command=lambda: controller.show_frame(Settings))
        settings_button.place(x=30, y=270)

        search_entry = tk.Entry(self,  font=("", 15))
        search_entry.place(x=270,y=70)

        label_0 = tk.Label(self, text="Available profiles",width=20,font="Verdana 15 underline")
        label_0.place(x=270,y=130)

        cursor.execute( "SELECT profile_name FROM profiles GROUP BY profile_name",)
        fetch = cursor.fetchall()
        #print(fetch)
        if fetch is None :
            none_label = tk.Label(self, text = "Added profiles will be viewed here...")
            self.none_label.place(x=270, y=200)
            print("none")
        else:
          self.listbox = tk.Listbox(self, width =25, font=("", 13))
          self.listbox.place(x=270, y=150)
          rows = 0
          for profiles in fetch:
             #print(rows)
             self.listbox.insert(tk.END, fetch[rows])
             rows= rows+1
          print("profiles available")

          self.listbox.bind('<<ListboxSelect>>',self.On_Select)

        remove_button = tk.Button(self,width=13,height=1, bg="#737271", text="Remove"
                            )
        remove_button.place(x=400, y=500)

        profile_label = tk.Label(self, text="Proile Name *", font="Verdana 13")
        profile_label.place(x=550,y=100)

        self.profile_entry = tk.Entry(self, textvariable = self.PROFILE_NAME, font=("", 13))
        self.profile_entry.place(x=730,y=100)

        self.receivedfrom_label = tk.Label(self, text="Received from *", font="Verdana 13")
        self.receivedfrom_label.place(x=550,y=150)

        self.receivedfrom_entry = tk.Entry(self, textvariable = self.RECEIVE_FROM, font=("", 13))
        self.receivedfrom_entry.place(x=730,y=150)

        self.amount_label = tk.Label(self, text="Amount *", font="Verdana 13")
        self.amount_label.place(x=550,y=200)

        self.amount_entry = tk.Entry(self, textvariable = self.AMOUNT, font=("", 13))
        self.amount_entry.place(x=730,y=200)
        cursor.execute("SELECT group_name FROM `groups` ")
        fetch = cursor.fetchall()
        print("printing")
        print(fetch)
        groups = []
        for group in fetch:
            groups.append(group[0])
        
        group_label = tk.Label(self,  text="Select a group to send from *", font="Verdana 13")
        group_label.place(x=550,y=250)
        self.groups = ttk.Combobox(self, textvariable = self.GROUP, width= 40,
                            values= groups)
        self.groups.place(x=600, y=280)
       
        self.message_entry=tk.Text(self, height=10, width=50)
        self.message_entry.place(x=550,y=320)

        update_button = tk.Button(self,width=13,height=1, bg="#737271", text="Update",
                            command= self.add_profile)
        update_button.place(x=800, y=500)

    
        logout_button = tk.Button(self,width=7,height=1,text="logut"
                            )
        logout_button.place(x=10, y=500)

        mainsetting_button = tk.Button(self,width=7,height=1, text="Security", command=lambda: controller.show_frame(Account)
                            )
        mainsetting_button.place(x=100, y=500)

    def On_Select(self, event):
        self.profile_entry.delete(0,tk.END)
        self.receivedfrom_entry.delete(0,tk.END)
        self.amount_entry.delete(0,tk.END)
        self.groups.delete(0,tk.END)
        self.message_entry.delete(1.0, tk.END)
       
        
        widget = event.widget
        selection=widget.curselection()
        self.picked = widget.get(selection[0])
        
       
        highlighted = self.listbox.get(tk.ANCHOR)
       
        print(highlighted)
    
        cursor.execute("SELECT profile_name, received_from, amount, profile_group, profile_message FROM `profiles` WHERE profile_name = ?", (highlighted[0],))
        fetch = cursor.fetchone()
        print(highlighted)
        self.profile_entry.insert(10, fetch[0])
        self.receivedfrom_entry.insert(10, fetch[1])
        self.amount_entry.insert(10, fetch[2])
        self.groups.insert(10, fetch[3])
        self.message_entry.insert(tk.END, fetch[4])
          

    def add_profile(self):
         
         warning_label = tk.Label()
         warning_label.place(x=730,y=70)
         if self.PROFILE_NAME.get() == "" or self.RECEIVE_FROM.get() == "" or self.AMOUNT.get() == "" or self.GROUP.get() == "" or self.message_entry.get(1.0, tk.END) == "":
             warning_label.config(text = "Please fill all fields", fg = "red")
             print(self.MESSAGE.get())
             print(self.AMOUNT.get())

         else:
             cursor.execute("INSERT INTO `profiles` (profile_name, received_from, amount, profile_group, profile_message) VALUES(?, ?, ?, ?, ?)", (self.PROFILE_NAME.get(), self.RECEIVE_FROM.get(), self.AMOUNT.get(), self.GROUP.get(), self.message_entry.get(1.0, tk.END)))
             conn.commit()
             self.listbox.insert(tk.END, self.PROFILE_NAME.get())
            
class Account(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.NEW_USERNAME = tk.StringVar()
        self.CURRENT_PASSWORD = tk.StringVar()
        self.NEW_PASSWORD = tk.StringVar()
        self.CONFIRM_PASSWORD = tk.StringVar()

        self.lbl_text = tk.Label(self)
        self.lbl_text.place(x=400, y=120)
        
        receivedmessages_button = tk.Button(self,width=25,height=3, bg="#737271", text="Received Messages",
                             command=lambda: controller.show_frame(ReceivedMessages))
        receivedmessages_button.place(x=30, y=50)
        
        sentmessages_button = tk.Button(self,width=25,height=3, bg="#737271", text="Sent Messages",
                            command=lambda: controller.show_frame(SentMessages))
        sentmessages_button.place(x=30, y=130)

         
        groups_button = tk.Button(self,width=25,height=3, bg="#737271", text="Groups",
                            command=lambda: controller.show_frame(Groups))
        groups_button.place(x=30, y=200)

        
        settings_button = tk.Button(self,width=25,height=3,bg="#FF5733", text="Settings",
                            command=lambda: controller.show_frame(Settings))
        settings_button.place(x=30, y=270)

        label_0 = tk.Label(self, text="Change Username/Password",font=("bold", 20))
        label_0.place(x=350,y=50)
  
  
       
  
        self.username = tk.Entry(self, font="Verdana 15", textvariable=self.NEW_USERNAME)
        self.username.place(x=400,y=150)
  
        current_pass = tk.Entry(self, show = "*", font="Verdana 11", textvariable=self.CURRENT_PASSWORD)
        current_pass.place(x=400,y=200)

        new_pass= tk.Entry(self, show = "*", font="Verdana 11", textvariable=self.NEW_PASSWORD)
        new_pass.place(x=400,y=250)

        confirm_newpass= tk.Entry(self, show = "*", font="Verdana 11", textvariable=self.CONFIRM_PASSWORD)
        confirm_newpass.place(x=400,y=300)

        remove_button = tk.Button(self,width=20,height=2, bg="#737271", text="Remove",
                            command=lambda: controller.show_frame(Groups))
        remove_button.place(x=320, y=380)

        
        update_button = tk.Button(self,width=20,height=2,bg="#737271", text="Update",
                            command=self.insert_admin)
        update_button.place(x=620, y=380)

    def insert_admin(self, event=None):
            
           
            if self.NEW_USERNAME.get() == "" or self.CURRENT_PASSWORD.get() == "" or self.NEW_PASSWORD.get() == "" or self.CONFIRM_PASSWORD.get() == "":
                self.lbl_text.config(text="Please complete the required field(s)!", fg="red")
                print("test")
            else:
               cursor.execute( "SELECT username, COUNT(*) FROM users WHERE username =? GROUP BY username", (self.NEW_USERNAME.get(),))
               if cursor.fetchone() is None:

                  if self.CURRENT_PASSWORD.get() == "admin" and self.NEW_PASSWORD.get() == self.CONFIRM_PASSWORD.get():
                    cursor.execute("INSERT INTO `users` (username, password) VALUES(?, ?)", (self.NEW_USERNAME.get(), self.NEW_PASSWORD.get(),))
                    conn.commit()
                    cursor.execute( "SELECT username, COUNT(*) FROM users WHERE username ='admin' GROUP BY username",)
                    if cursor.fetchone() is not None:
                        cursor.execute( "DELETE FROM users WHERE username='admin'",)
                        conn.commit()
                        print("deleted")
               
                  else:
                          print( self.NEW_PASSWORD.get())
                          print( self.CONFIRM_PASSWORD.get())
                          print( self.CURRENT_PASSWORD.get())
                          print( self.NEW_USERNAME.get())
                          self.lbl_text.config(text="An Error Occured!!!!!!!!", fg="red")

               else:
                   self.lbl_text.config(text="A user with same username exixts", fg="red")
                   self.NEW_USERNAME.set("")
                   self.CURRENT_PASSWORD.set("")

def logged_in():
    app.show_frame(ReceivedMessages)

def logged_in_new():
    app.show_frame(Account)
        
app = SeaofBTCapp()
Database()
app.wm_maxsize(width=950,height=550)
app.wm_minsize(width=950,height=550)
app.mainloop()
