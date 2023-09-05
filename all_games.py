# get the all files name the the games folder
# and run the main.py on each file 

# Path: chessDataBase.py

# load the files names
import os
import subprocess

fileNames = os.listdir("games")
fileNames.sort()
print(fileNames)


for game in fileNames:
    subprocess.run(["python3", "main.py", "games/" + game])
    print("Done with the game: ", game)


