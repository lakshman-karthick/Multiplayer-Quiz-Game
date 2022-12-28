from socket import AF_INET, socket, SOCK_STREAM
from timeit import default_timer as timer
from threading import Thread
import sys, select, tkinter, time
from tkinter import *

HOST='192.168.92.224'
PORT=5000
BUFFERSIZE=1024


ADDR=(HOST,int(PORT))
client_socket=socket(AF_INET,SOCK_STREAM)
client_socket.connect(ADDR)
start_time=0.0
sent = 0

def send_ans(ans):
	client_socket.send(bytes(str(ans),"utf8"))
	global sent
	sent = 1

def timeout():

	start_time = timer()
	global sent
	while(1):
		if (timer() - start_time > 60):
			client_socket.send(bytes(str("e"),"utf8"))
			client_socket.send(bytes(str(timer() - start_time),"utf8"))
			break
		else:
			if sent:
				client_socket.send(bytes(str(timer() - start_time),"utf8"))
				sent = 0
				return
			else:
				continue

def send_name(name):
	if(name!=''):
		client_socket.send(bytes(str(name),"utf8"))
		entry_field.destroy()
		send_button.destroy()
		la.destroy()

def quit_app ():
	exit(0)

top=tkinter.Tk()
top.geometry('650x400')
top.title("Multiplayer Quiz")
top.configure(bg='grey20')
top.resizable(0,0)



l = Label(top, text="Multiplayer Quiz", width=52, height=2, borderwidth=5, relief="solid", font = ("Courier", 18, "bold"), background='yellow')
l.grid(padx = 2)


messages_frame=tkinter.Frame(top)
scrollbar=tkinter.Scrollbar(messages_frame)

msg_list=tkinter.Listbox(messages_frame,height=5,width=105,borderwidth=5, relief="solid",font = ("Courier", 10, "bold"))
msg_list.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
l.pack()
padding = {'padx': 5, 'pady': 5}
msg_list.pack()
messages_frame.pack()
la= tkinter.Label(top, text="Name",background='yellow')
la.pack(side=LEFT,padx=15)
my_msg=tkinter.StringVar()
entry_field=tkinter.Entry(top,textvariable=my_msg,font=("Arial", 10),width=70)
entry_field.bind("<Return>", lambda x:send_name(my_msg.get()))
entry_field.pack(side=LEFT, padx=0, pady=80)
send_button=tkinter.Button(top,text="Send",command=lambda:send_name(my_msg.get()), bg="#FF3399", fg="#FFFFFF", font=("Arial", 10),padx=6)
send_button.pack(side=LEFT, padx=15, pady=0)

option_a = tkinter.StringVar()
option_b = tkinter.StringVar()
option_c = tkinter.StringVar()
option_d = tkinter.StringVar()

button_a = tkinter.Button(
	    textvariable=option_a,
	    width=25,
	    height=3,
	    bg="blue",
	    fg="yellow",
		command=lambda: send_ans("a")
	)
button_b = tkinter.Button(
	textvariable=option_b,
	width=25,
	height=3,
	bg="blue",
	fg="yellow",
	command=lambda: send_ans("b")
)
button_c = tkinter.Button(
	textvariable=option_c,
	width=25,
	height=3,
	bg="blue",
	fg="yellow",
	command=lambda: send_ans("c")
)
button_d = tkinter.Button(
	textvariable=option_d,
	width=25,
	height=3,
	bg="blue",
	fg="yellow",
	command=lambda: send_ans("d")
)
quit_button = tkinter.Button(
	    text="QUIT !",
	    width=25,
	    height=5,
	    bg="blue",
	    fg="yellow",
		command=quit_app
	)

def start_game():
	global start_time
	msg_list.insert(tkinter.END,"Please enter your name and press send")
	x=client_socket.recv(1024).decode("utf8")
	msg_list.insert(tkinter.END,x)
	client_socket.recv(6)
	button_a.pack()
	button_b.pack()
	button_c.pack()
	button_d.pack()
	while(1):

		question=client_socket.recv(1024).decode("utf8")

		if question=="END_OF_QUIZ" :
			break

		question=question.split(',')
		msg_list.delete(0,1)
		msg_list.insert(tkinter.END,question[0]+") "+question[1])
		msg_list.insert(tkinter.END,"You have 60 seconds to answer!")
		
		option_a.set("(A) "+question[2])
		option_b.set("(B) "+question[3])
		option_c.set("(C) "+question[4])
		option_d.set("(D) "+question[5])
		
		Thread(target=timeout).start()

		flag=client_socket.recv(1).decode("utf8")

		if(int(flag)):
			pass
		else:
			msg_list.delete(0,1)
			msg=client_socket.recv(1024).decode("utf8")
			msg_list.insert(tkinter.END,msg)
			msg_list.insert(tkinter.END,"Better luck next time")
			client_socket.close()
			button_a.destroy()
			button_b.destroy()
			button_c.destroy()
			button_d.destroy()
			quit_button.pack()
			return
			
	msg_list.delete(0,1)
	msg_list.insert(tkinter.END,"Waiting for other clients to complete")

	button_a.destroy()
	button_b.destroy()
	button_c.destroy()
	button_d.destroy()

	result=client_socket.recv(1024).decode("utf8")
	msg_list.delete(0)
	msg_list.insert(tkinter.END,"Leaderboard")
	x=1
	for player in result.split(";"):
		player_info=player.split(",")
		msg=str(x)+"   "+player_info[0]+"   "+str(round(float(player_info[1]),3))+"s"
		msg_list.insert(tkinter.END,msg)
		x=x+1
	msg_list.insert(tkinter.END,"Thank you!")

	quit_button.pack()
	

receive_thread=Thread(target=start_game)
receive_thread.start()
tkinter.mainloop()
client_socket.close()