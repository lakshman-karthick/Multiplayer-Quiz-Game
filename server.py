from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread
import time

clients = {}
addresses= {}
times = []
threads = []

HOST ='192.168.92.224'
PORT = 5000
BUFFERSIZE=1024
CURR_CLIENT_NO = 0
TOT_CLIENT_NO = 2
ADDR=(HOST,PORT)
SERVER=socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

all_times = []

def accept_in_connections():
	print("accept-start")
	global CURR_CLIENT_NO,TOT_CLIENT_NO
	while CURR_CLIENT_NO < TOT_CLIENT_NO:
		CURR_CLIENT_NO+=1
		client,client_addr=SERVER.accept()
		print("%s:%s has joined the quiz."%client_addr)
		addresses[client]=client_addr
		thr = Thread(target=handle_client,args=(client,))
		threads.append(thr)
		thr.start()
		time.sleep(.1)
	for t in threads:
		t.join()
	time.sleep(1)
	print("accept-end")
def handle_client(client):
	print("handle-start")
	name=client.recv(BUFFERSIZE).decode("utf8")
	welcome='Welcome %s! Please wait for the other clients to join' %name
	client.send(bytes(welcome,"utf8"))
	clients[client]=name
	
	print("Waiting for more users to join")
	while (len(clients) != TOT_CLIENT_NO):
		pass
	start_game(client,name)
	print("game ended for "+name)
	print("handle-end")
    
def start_game(client,name):
	print("start-start")
	client.send(bytes("start","utf8"))
	time.sleep(.1)
	q_file = open("question.csv", "r")
	line = q_file.readline()
	line = q_file.readline()
	tot_time = 0

	while(line != ''):

		client.send(bytes(line[0:-3],"utf8"))
		if line=="END_OF_QUIZ___" :
			break

		crct_ans = line.split(sep=',')[6][0]
		ans=str(client.recv(1).decode("utf8"))
		q_time=(client.recv(BUFFERSIZE).decode("utf8"))
		q_time=float(q_time)
		if ans==crct_ans :
			client.send(bytes("1","utf8"))
			tot_time+=q_time
		else:
			del clients[client]
			client.send(bytes("0","utf8"))
			if ans=="e":
				client.send(bytes("You took more than 60 seconds!","utf8"))
			else:
				client.send(bytes("Wrong answer!","utf8"))
			client.close()
			return

		line = q_file.readline()

	avg_time = tot_time / 2
	all_times.append({
		"name" : name,
		"time" : avg_time
	})
	print("start-end")
if __name__ == "__main__":
	SERVER.listen(TOT_CLIENT_NO)
	# start_game()
	accept_in_connections()

	all_times = sorted(all_times, key=lambda x: x["time"])
	print("yes")
	result=''
	for i in all_times:
		result=result+str(i["name"])+","+str(i["time"])+";"
	for i in clients:
		i.send(bytes(result[0:-1],"utf8"))
		print("___________LEADERBOARD___________")
		print(result)
		SERVER.close()
	# for i in all_times
	SERVER.close()