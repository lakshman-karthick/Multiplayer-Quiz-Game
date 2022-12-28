# Project Description 
Multiple clients can play the Quiz game at same time using the concept of concurrent file server. TCP/IP was used to create the application stack.

# Approach
1. Game starts once the maximum number of players have joined.
2. Questions are sent to the players with options.
3. Players need to answer the question within 60 secs.
4. If a player fails to answer within the time limit or answers with the wrong answer, the player will
get eliminated.
5. At the end, players who have answered all the questions can see the leaderboard. The
leaderboard is set according to the average time taken by a player to answer a question.

# Applications
- Tkinter using python to develop game widgets
- Concurrent file server using client.py and server.py by implementing TCP/IP.
