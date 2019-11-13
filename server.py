import socket
import select
import datetime


class Server:
    def __init__(self):
        self.ip = "0.0.0.0"
        self.port = 8080
        self.server_socket = socket.socket()
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        self.open_client_sockets = {}
        self.messages = []
        self.managing_client_sockets = []
        self.denied_clients = []
        self.private_conversation = []


    def send_waiting_messages(self, wlist):
        for message in self.messages:
            (current_sockets, data) = message
            for client_socket in list(self.open_client_sockets.keys()):
                if client_socket not in current_sockets and client_socket in wlist:
                    if type(data) == type(list()):
                        data = " ".join(data)
                    msg = datetime.datetime.now().strftime("%X") + " " + data
                    msg_to_send = str(len(msg))+msg
                    client_socket.send(msg_to_send)
                    current_sockets.append(client_socket)
                    message = (current_sockets, data)
                    if len(current_sockets) == len(list(self.open_client_sockets.keys())):
                        self.messages.remove(message)


    def send_massege_to_all(self,data,socket):
        if socket in self.managing_client_sockets:
           msg_to_all = str("@"+self.open_client_sockets[socket]+": "+data)
        else:
            msg_to_all = str(self.open_client_sockets[socket] + ": " + data)
        combination1 = []
        combination1.append(socket)
        self.messages.append((combination1, msg_to_all))

    def quit_msg(self,socket):
        if socket in self.managing_client_sockets:
           msg_to_all = str("@"+self.open_client_sockets[socket]+" has left the chat")
           self.managing_client_sockets.remove(socket)
           if self.managing_client_sockets == [] and len(self.open_client_sockets.keys()) == 2:
               #to do manage new manager (the firs in keys)
               self.managing_client_sockets.append(self.open_client_sockets.keys()[1])#not the server
        else:
            msg_to_all = str(self.open_client_sockets[socket] + " has left the chat")
        del self.open_client_sockets[socket]
        self.messages.append(([], msg_to_all))



     #sends the managers list to the wanted socket
    def view_managers(self, wanted_socket):
        msg = "the managers are: "
        b = True
        for msocket in self.managing_client_sockets:
            if b==True:
                msg = str(msg + "@"+self.open_client_sockets[msocket])
                b=False
            else:
                 msg =str(msg +", @"+self.open_client_sockets[msocket])
        combination1 = list(self.open_client_sockets.keys())
        combination1.remove(wanted_socket)  # removes the wanted socket from the list of the sockets we do'nt want to send to
        self.messages.append((combination1, msg))


# to do in the decifer data the listen to the muted clients
    def shut_up(self, socket, wanted_socket):
        if socket in self.managing_client_sockets and wanted_socket not in self.denied_clients and wanted_socket not in self.managing_client_sockets:
            msg_to_wanted = "you are muted ( " + str(self.open_client_sockets[socket]) + "did it)"
            combination1 = self.open_client_sockets.keys()
            combination1.remove(wanted_socket)  # removes the wanted socket from the list of the sockets we do'nt want to send to
            self.messages.append((combination1, msg_to_wanted))
            #msg_to_socket = str(self.open_client_sockets[wanted_socket]) + "is muted successfully"
            #combination2 = self.open_client_sockets.keys()
            #combination2.remove(socket)
            #self.messages.append((combination2, msg_to_socket))
            self.denied_clients.append(wanted_socket)  # add to dinied sockes
        elif socket in self.managing_client_sockets and wanted_socket in self.denied_clients:
            combination = self.open_client_sockets.keys()
            combination.remove(socket)
            msg_to_socket = str(self.open_client_sockets[wanted_socket]) + " is already muted "
            self.messages.append((combination, msg_to_socket))
        elif socket not in self.managing_client_sockets:
            combination = self.open_client_sockets.keys()
            combination.remove(socket)
            msg_to_socket = str(self.open_client_sockets[socket]) + " you are not a manager"
            self.messages.append((combination, msg_to_socket))
        elif socket in self.managing_client_sockets and wanted_socket in self.managing_client_sockets:
            combination = self.open_client_sockets.keys()
            combination.remove(socket)
            msg_to_socket = "@"+str(self.open_client_sockets[wanted_socket]) + " is a manager (you can't mute him)"
            self.messages.append((combination, msg_to_socket))

    def you_cant_speak(self, socket):
        msg = "You cannot speak here"
        combination1 = list(self.open_client_sockets.keys())
        combination1.remove(socket)  # removes the wanted socket from the list of the sockets we do'nt want to send to
        self.messages.append((combination1, msg))


    def kick(self, socket, wanted_socket):
        if socket in self.managing_client_sockets and wanted_socket not in self.managing_client_sockets:
            #msg_to_wanted = "you have kicked from the chat ( @" + str(self.open_client_sockets[socket]) + "did it)"
            wanted_socket_name = str(self.open_client_sockets[wanted_socket])
            #combination1 = self.open_client_sockets.keys()
            #combination1.remove(wanted_socket)
            #self.messages.append((combination1, msg_to_wanted))
            del self.open_client_sockets[wanted_socket] #delete this socket from open client socket
            msg_to_all = wanted_socket_name+" has been kicked from the chat"
            combination1 = []
            self.messages.append((combination1, msg_to_all))
        elif socket in self.managing_client_sockets and wanted_socket in self.managing_client_sockets:
            msg_to_socket = "@"+str(self.open_client_sockets[wanted_socket]) + " is a manager (you can't kick him)"
            combination = self.open_client_sockets.keys()
            combination.remove(socket)
            self.messages.append((combination, msg_to_socket))
        else:
            msg_to_socket = str(self.open_client_sockets[socket]) + " you are not a manager"
            combination = self.open_client_sockets.keys()
            combination.remove(socket)
            self.messages.append((combination, msg_to_socket))


    def manage_msg(self,wanted):
        msg_to_wanted = "you are a manager !!! "
        combination1 = self.open_client_sockets.keys()
        combination1.remove(wanted)  # removes the wanted socket from the list of the sockets we do'nt want to send to
        self.messages.append((combination1, msg_to_wanted))


    def manager(self, socket, wanted_socket):
        if socket in self.managing_client_sockets and wanted_socket not in self.managing_client_sockets:
            self.managing_client_sockets.append(wanted_socket)
            msg_to_wanted = "you are a manager ( @"+str(self.open_client_sockets[socket])+" did it)"
            combination = self.open_client_sockets.keys()
            combination.remove(wanted_socket)#removes the wanted socket from the list of the sockets we do'nt want to send to
            self.messages.append((combination, msg_to_wanted))
            #msg_to_socket = str(self.open_client_sockets[wanted_socket])+" managed to be a manager successfully"
            #combination = self.open_client_sockets.keys()
            #combination.remove(socket)
            #self.messages.append((combination,msg_to_socket))
        elif socket in self.managing_client_sockets and wanted_socket in self.managing_client_sockets:
            combination = self.open_client_sockets.keys()
            combination.remove(socket)
            msg_to_socket = "@"+str(self.open_client_sockets[wanted_socket])+" is already a manager"
            self.messages.append((combination, msg_to_socket))
        elif socket not in self.managing_client_sockets:
            combination = self.open_client_sockets.keys()
            combination.remove(socket)
            msg_to_socket = str(self.open_client_sockets[socket]) + " you are not a manager"
            self.messages.append((combination, msg_to_socket))

    # def private_msg(self, socket, wanted_socket,data):


    def decifer_data(self, data, socket):
        dt = data
        if self.open_client_sockets[socket] == "":
            # print "name"
            name = data
            self.open_client_sockets[socket] = name

        else:
            for i in range(1, 1000):
                if self.open_client_sockets[socket] == (data[i:int(data[0:i])+i]):
                    data = data[int(data[0:i])+i:]
                    break
            command_value = data[0:1]
            dt = data[1:]
            print ("command value=> "+command_value)

            if command_value!="1" and command_value!="5":
                wanted_socket = ""
                for i in range(1, 1000):
                    if (data[i:int(data[0:i]) + i]) in list(self.open_client_sockets.values()):
                        for socketss in list(self.open_client_sockets.keys()):
                            if self.open_client_sockets[socketss] == (data[i:int(data[0:i]) + i]):
                                wanted_socket = socketss
                                break
                        break

                print ("the command value is ; "+ command_value)
                if command_value == "2":
                    self.manager(socket,wanted_socket)
                if command_value == "3":
                    self.kick(socket, wanted_socket)
                if command_value == "4":
                    self.shut_up(socket, wanted_socket)


            if command_value == "1":
                data = data[2:]
                print ("data => " + data)
                if data == "vm":
                    self.view_managers(socket)
                elif data == "quit":
                    print ("want to quit")
                    self.quit_msg(socket)

                elif socket in self.denied_clients and data != "vm" and data != "quit": #to be sure...
                    self.you_cant_speak(socket)
                else:
                    self.send_massege_to_all(data,socket)

            if command_value == "5":
                 wanted_socket = ""
                 mss = ""
                 for i in range(1, 1000):
                     print (str(i))
                     for user_socket in list(self.open_client_sockets.keys()):
                         if dt[i:int(dt[0:i]) + i] == self.open_client_sockets[user_socket]:
                             wanted_socket = user_socket
                             dt = dt[int(dt[0:i]) + i:]
                             mss = dt
                             break
                     if mss != "":
                         break
                 for i in range(1, 1000):
                     if int(dt[0:i]) == len(dt[i:]):
                         dt = dt[i:]
                         break
                 if  wanted_socket in self.open_client_sockets.keys() :
                     name = self.open_client_sockets[socket]
                     if socket in self.managing_client_sockets:
                         name = "@" + name
                     ms = "---private message from "+name + "--- : " + dt
                     socketsss = list(self.open_client_sockets.keys())
                     socketsss.remove(wanted_socket)
                     combination = (socketsss, ms)
                     self.messages.append(combination)
                 else:
                     socketsss = list(self.open_client_sockets.keys())
                     socketsss.remove(socket)
                     combination = (socketsss, "WRONG USERNAME")
                     self.messages.append(combination)

    def run(self):
        print ("server start")
        count = 0
        while True:
            count = count+1

            aaa = [self.server_socket] + list(self.open_client_sockets.keys())
            if count % 1000000 == 0:
               print (aaa)
            rlist, wlist, xlist = select.select(aaa, list(self.open_client_sockets.keys()), [])
            for current_socket in rlist:
                if current_socket is self.server_socket:
                    (new_socket, address) = self.server_socket.accept()
                    self.open_client_sockets[new_socket] = ""
                    print("new client")


                else:
                    try:
                        print("befor data recv")
                        data = current_socket.recv(1024)
                        print (str(data))
                        print ("befor  decifer")
                        self.decifer_data(data, current_socket)

                        if self.managing_client_sockets == [] and self.open_client_sockets.keys() != []:
                            for socketsss in list(self.open_client_sockets.keys()):
                                if self.open_client_sockets[socketsss] != "":
                                    self.managing_client_sockets.append(socketsss)
                                    self.manager_msg(socketsss)

                                    break

                    except:
                        print ("fail")
                        continue
                    self.send_waiting_messages(wlist)
if __name__ == '__main__':
    Server().run()