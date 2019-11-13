from tkinter import*
import socket
import select
import sys
import winsound
import time


class GUI_Client():

    def __init__(self):
        self.messages = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ""
        self.win = Tk()
        self.chat_window = ""
        self.msg = ""
        self.count = 0

    def login(self):

        self.win.title("Log-in")
        #self.win.geometry('410x175+550+250')
        self.win.geometry('700x220+550+250')
        self.win.configure(bg="pink")
        a=Label(self.win, text="                             LOG IN",font="Times 26 bold",bg="pink")
        a.grid(column=0,row=0,sticky='w')
        Label(self.win, bg="pink", text=" ", font="Times 26 bold").grid(column=0, row=3, sticky='w')
        b=Label(self.win, text="ENTER YOUR NAME PLEASE: ", font="Times 18", bg="pink")
        b.grid(column=0, row=1, sticky='w')
        name = StringVar()
        entered_name = Entry(self.win, width=20, textvariable=name,font="Times 20")
        entered_name.grid(column=1, row=1)
        action = Button(self.win,bd=1,width=30,font="Times 16 bold", text="SUBMIT!", bg="pale violet red",command=lambda: submit(action, name, self,self.win))

        action.grid(column=0, row=4, sticky=W)
        print(self.username)
        while True:
            try:
                if self.count % 500 == 0:
                    self.win.update()
                if self.username != "":
                    print("the username is : " + self.username)
                    return True
                self.count = self.count + 1

            except:
                sys.exit()
                break

    def chat_time(self):
        self.win.destroy()
        if self.username[-1] == " ":
            self.username = self.username[:-1]
        self.messages.append(self.username)
        print (self.messages)
        self.my_socket.connect(("127.0.0.1", 8080))
        self.send_messages()
        root = Tk()
        root.title(self.username + " online")
        root.geometry("680x490+0+0")
        txt = Text(root, font="Times 14", height=35, width=50, bg="plum1", fg="black")
        scr = Scrollbar(root)
        scr.config(command=txt.yview)
        txt.configure(wrap="word")
        txt.config(yscrollcommand=scr.set)
        txt.pack(side=LEFT)
        txt.insert(END,
                   "WELCOME TO THE CAHT " + self.username + "!\n\nYOU CAN DO SOME COOL THINGS:\n \n1.USE THE MESSAGE BOTTON TO SEND A MESSEAGE TO ALL MEMBERS\n\n2.USE THE PRIVATE BOTTON TO SEND A PRIVATE MESSAGE TO ONE MEMBER\n\n3.USE THE VIEW MANAGERS BOTTON TO SEE THE MENAGERS LIST\n\n4. USE THE QUIT BOTTON TO QUIT FROM THE CHAT\n\nMANAGERS MENU:\n\n1.USE THE MAKE NEW MANAGER BOTTON TO APPOINT A NEW MANAGER\n\n2. USE THE KICK BOTTON TO LICK A MEMBER FROM THE CHAT")
        txt.insert(END, "\n")
        scr.pack(side="right", fill="y", expand=False)
        txt.pack(side="left", fill="both", expand=True)
        txt.configure(state="disabled")
        msgwin = Tk()
        msgwin.title("sender")
        msgwin.geometry("680x120+0+520")
        msgwin.configure(bg="plum3")
        l1 = Label(msgwin, text="ENTER YOUR MESSAGE:", font="Times 14 bold", bg="plum3")
        l1.grid(column=0, row=1, sticky='w')
        name = StringVar()
        entered_name = Entry(msgwin, width=60, textvariable=name, font="Helvetica 10 bold")
        entered_name.grid(column=0, row=2)
        action = Button(msgwin,bd=1, fg="black", bg="LightBlue2", width=54, text="SEND!",font="Helvetica 10 bold",
                        command=lambda: p1(entered_name, self))
        action.grid(column=0, row=3, sticky=W)
        vm_button = Button(msgwin, font="Helvetica 10 bold",bd=1, fg="black", bg="LightBlue2", width=22, text="VIEW MANAGERS",
                           command=lambda: p2(self, "vm"))
        vm_button.grid(column=2, row=2, sticky=W)
        quit_button = Button(msgwin, font="Helvetica 10 bold", bd=1,fg="black", bg="LightBlue2", width=22, text="QUIT CHAT",
                             command=lambda: p2(self, "quit"))
        quit_button.grid(column=2, row=3, sticky=W)
        win3 = Tk()
        win3.title("commands")
        win3.geometry("130x640+680+0")
        prvate_msg = Button(win3, font="Times 10 bold", bd=1, fg="black", bg="orchid1", width=20,height=10, text="PRIVAE MASSEGE",
                           command=lambda: p4(self))
        prvate_msg.grid(column=0,row=0)
        mute = Button(win3, font="Times 10 bold", bd=1, fg="black", bg="orchid2", width=20,height=10, text="mute",
                            command=lambda: p5(1,self))
        mute.grid(column=0, row=1)
        kick = Button(win3, font="Times 10 bold", bd=1, fg="black", bg="orchid3", width=20,height=10, text="kick",
                      command=lambda: p5(0, self))
        kick.grid(column=0, row=2)
        manage = Button(win3, font="Times 10 bold", bd=1, fg="black", bg="orchid4", width=20, height=10,text="make admin",
                      command=lambda: p5(2, self))
        manage.grid(column=0, row=3)

        count = 0

        while 1:
            count = count + 1
            rlist, wlist, xlist = select.select([self.my_socket], [self.my_socket], [])
            if self.my_socket in rlist:
                data = self.my_socket.recv(1024)
                print (data)
                d = data
                try:
                    data = without_len(
                        data)  # if someone sends me without the length of the msg I will get the data any way
                except:
                    data = d
                txt.configure(state="normal",wrap="word")  # make it enable to add text to moment befor adding text
                txt.insert(END, "\n" + data)
                txt.see(END)
                txt.edit_modified(0)
                txt.configure(state="disabled")  # returns it to read onlys
                winsound.Beep(1250, 350)
            try:
                root.update()
                msgwin.update()
                win3.update()
            except:
                message = str(len(self.username)) + self.username + "1" + str(len("quit")) + "quit"
                self.messages.append(message)
                self.send_messages()
                sys.exit()

    def send_messages(self):
        for message in self.messages:
            try:
                self.my_socket.send(message)
                print ("sent: " + message)
                self.messages.remove(message)
            except:
                continue

    def set_msg(self, msg):
        self.msg = msg

    def get_messages(self):
        return self.messages

    def set_messages(self, messages):
        self.messages = messages

    def get_username(self):
        return self.username

    def set_username(self, str):
        name = str
        if name == "":
            return False
        if name[0] == "@" or name == "":
            return False
        self.username = name
        return True


def without_len(data):
    for i in range(1, 1000):
        n = int(data[0:i])
        if n == len(data[i:]):
            print ("the msg is:" + data[i:])
            return data[i:]
            break


def submit(action, name, GUI_client,win):
    is_username_ok = GUI_client.set_username(name.get())
    l1 = Label(text="The name can't start with <@> ", fg="red",bg="snow",font="Helvetica 10 bold")
    l2 = Label(text="Connecting...                              ",fg="green",bg="snow",font="Helvetica 10 bold")  # to delete all the last label
    l3 = Label(text="Enter a name                           ",fg="red",bg="snow",font="Helvetica 10 bold")
    try:
        if name.get()=="":
            l3.grid(column=0, row=5, sticky='w')
        elif is_username_ok == False:
            l1.grid(column=0, row=5, sticky='w')
            print("The name can't start with <@> ")
        else:
            l2.grid(column=0, row=5, sticky='w')
            try:
                win.update()
            except:
                pass
            time.sleep(2)
            print ("Good username ")
            return True
    except:
        print


def p1(entered_name, GUI_Client):
    message = entered_name.get()
    entered_name.delete(0, END)
    print ("this is msg :" + message)
    if message != "":

        if message[0:2] == "k ":  # <= inclood the space

            name_of_wanted = message[2:]
            message = str(len(GUI_Client.get_username())) + GUI_Client.get_username() + "3" + str(
                len(name_of_wanted)) + name_of_wanted
        elif message[0:2] == "m ":  # <= inclood the space

            name_of_wanted = message[2:]
            message = str(len(GUI_Client.get_username())) + GUI_Client.get_username() + "4" + str(
                len(name_of_wanted)) + name_of_wanted
        elif message[0:4] == "anm ":  # <= inclood the space

            name_of_wanted = message[4:]
            message = str(len(GUI_Client.get_username())) + GUI_Client.get_username() + "2" + str(
                len(name_of_wanted)) + name_of_wanted
        elif message[0:2] == "p ":

            msg = message.split(" ")
            msg = msg[2:]
            msg = " ".join(msg)
            name_of_wanted = message.split(" ")[1]
            message = str(len(GUI_Client.get_username())) + GUI_Client.get_username() + "5" + str(
                len(name_of_wanted)) + name_of_wanted + str(len(msg)) + msg
        else:

            message = str(len(GUI_Client.get_username())) + GUI_Client.get_username() + "1" + str(
                len(message)) + message
            print (message)

        m = GUI_Client.get_messages()
        m.append(message)
        GUI_Client.set_messages(m)
        GUI_Client.send_messages()


def p2(GUI_Client, message):
    m = str(len(GUI_Client.get_username())) + GUI_Client.get_username() + "1" + str(len(message)) + message
    msgs = GUI_Client.get_messages()
    msgs.append(m)
    GUI_Client.set_messages(msgs)
    GUI_Client.send_messages()
def send_private(entered_name,entered_msg,win, client):
    msg = entered_msg.get()
    name = entered_name.get()

    msg_to_send = str(str(len(client.get_username())) + client.get_username() + "5" + str(
                len(name)) + name + str(len(msg)) + msg)
    print (msg_to_send)
    try:
        msgs = client.get_messages()
        msgs.append(msg_to_send)
        client.set_messages(msgs)
        client.send_messages()
        print ("private sent ! ")
    except:
        print ("fail")
    win.destroy()
    return


def p4(client):
    pwin = Tk()
    pwin.config(bg="snow")
    pwin.geometry("700x110+300+300")
    l1 = Label(pwin,font="Helvetica 12 bold",text="private msgs :",fg="red",bg="snow",)
    l1.grid(column=0,row=0,sticky='w')
    msg = StringVar()
    entered_msg = Entry(pwin, width=60, textvariable=msg, font="Helvetica 12")
    entered_msg.grid(column=1, row=1)
    l2 = Label(pwin, font="Helvetica 12", text="to : ",bg="snow")
    l2.grid(column=0, row=1, sticky='w')
    name = StringVar()
    entered_name = Entry(pwin, width=60,bg="snow", textvariable=name, font="Helvetica 12")
    entered_name.grid(column=1, row=2)
    l2 = Label(pwin, font="Helvetica 12", text="msg : ",bg="snow")
    l2.grid(column=0, row=2, sticky='w')
    action = Button(pwin, bd=1, fg="black", bg="green", width=20, text="send !", font="Helvetica 12 bold",
                    command=lambda: send_private(entered_msg, entered_name,pwin,client))
    action.grid(column=0, row=3, sticky=W)


def mute_or_kick_or_anm(param, entered_msg, pwin, client):
    name_of_wanted = entered_msg.get()

    if param == 0:
        msg_to_send = str(len(client.get_username())) + client.get_username() + "3" + str(len(name_of_wanted)) + name_of_wanted
    if param == 1:
        msg_to_send = str(len(client.get_username())) + client.get_username() + "4" + str(len(name_of_wanted)) + name_of_wanted
    if param == 2:
        msg_to_send = str(len(client.get_username())) + client.get_username() + "2" + str(len(name_of_wanted)) + name_of_wanted

    print (msg_to_send)
    try:
        msgs = client.get_messages()
        msgs.append(msg_to_send)
        client.set_messages(msgs)
        client.send_messages()
        print ("private sent ! ")
    except:
        print ("fail")
    pwin.destroy()
    return


def p5(param,client):
    pwin = Tk()
    pwin.geometry("740x85+300+300")
    pwin.configure(bg="snow")
    if param == 1:
        l1 = Label(pwin, font="Helvetica 16", bg= "snow",text="mute member :", fg="red")
        l1.grid(column=0, row=0, sticky='w')
        msg = StringVar()
        entered_msg = Entry(pwin, width=60, textvariable=msg, font="Helvetica 12", bg= "snow")
        entered_msg.grid(column=1, row=1)
        l2 = Label(pwin, font="Helvetica 12", text="to mute : ", bg= "snow")
        l2.grid(column=0, row=1, sticky='w')

    if param == 0:
        l1 = Label(pwin, font="Helvetica 16", text="kick member :", fg="red", bg= "snow")
        l1.grid(column=0, row=0, sticky='w')
        msg = StringVar()
        entered_msg = Entry(pwin, width=60, textvariable=msg, font="Helvetica 12", bg= "snow")
        entered_msg.grid(column=1, row=1)
        l2 = Label(pwin, font="Helvetica 12", text="to kick : ", bg= "snow")
        l2.grid(column=0, row=1, sticky='w')

    if param == 2:
        l1 = Label(pwin, font="Helvetica 16", text="make admin : ", fg="red", bg= "snow")
        l1.grid(column=0, row=0, sticky='w')
        msg = StringVar()
        entered_msg = Entry(pwin, width=60, textvariable=msg, font="Helvetica 12", bg= "snow")
        entered_msg.grid(column=1, row=1)
        l2 = Label(pwin, font="Helvetica 12", text="to make manager : ", bg= "snow")
        l2.grid(column=0, row=1, sticky='w')



    action = Button(pwin, bd=1, fg="black", bg="green", width=20, text="send !", font="Helvetica 12 bold",
                    command=lambda: mute_or_kick_or_anm(param,entered_msg, pwin, client))
    action.grid(column=0, row=3, sticky=W)


if __name__ == '__main__':
    c = GUI_Client()
    c.login()
    c.chat_time()