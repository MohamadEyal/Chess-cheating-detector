import chessDataBase
import sys
import plotext as plt


# Database connection
uri = "mongodb+srv://swalha:12345678911@chess.t4z9lx3.mongodb.net/?retryWrites=true&w=majority"
database = chessDataBase.ChessGameDatabase(uri)
database.connect()

playerName=sys.argv[1]
player_all_time_accuracy = []
for PlayerGame in database.getPlayer(playerName):
    player_all_time_accuracy.append(PlayerGame["accuracy"])

print(playerName ," all time accuracy: ", player_all_time_accuracy) 

plt.clear_data()
plt.plot(player_all_time_accuracy)

plt.title(playerName + " all time accuracy")
plt.xlabel("Games")
plt.ylabel("Accuracy")
plt.theme("clear")
plt.show()
