
def gameHash(game):
  #lets make a deep copy of the game
  newGame = game
  return myHash("\n".join(newGame.readlines())) 

def myHash(text:str):
  hash=0
  for ch in text:
    hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
  return hash