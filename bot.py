import discord 
from discord.ext.commands import Bot
from discord.ext import commands 
import asyncio
import random 

Client = discord.Client()
client = commands.Bot(command_prefix='.')

word = ""
guessesLeft = 6
playingHangman = False
blanks = []
guessedLetters=[]
lettersFound = 0


@client.event 
async def on_ready(): 
    print("Bot Online!") 
    print("Name: {}".format(client.user.name)) 
    print("ID: {}".format(client.user.id)) 

@client.command()
async def blackjack():
    await client.say("""`
    
 _     _            _     _            _    
| |__ | | __ _  ___| | __(_) __ _  ___| | __
|  _ \| |/ _  |/ __| |/ /| |/ _  |/ __| |/ /
| |_) | | (_| | (__|   < | | (_| | (__|   < 
|_ __/|_|\__,_|\___|_|\_\/ |\__ _|\___|_|\_
                       |__/                 
                                       
                                                                   
    `""")
    dealerValue = 0
    playerValue = 0
    dealerCards=[]
    playerCards=[]
    dealerNumAces=0
    playerNumAces=0
    cardNames={1:'One',2:'Two',3:'Three',4:'Four',5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine',10:'Ten',11:'Jack',12:'Queen',13:'King',14:'Ace'}
    cardValues = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:10, 12:10, 13:10, 14:11}

    while dealerValue < 17:
        nextCard = random.randrange(1,15)
        if nextCard is 14: dealerNumAces += 1
        dealerCards.append(cardNames[nextCard])
        dealerValue += cardValues[nextCard]
        while dealerValue > 21:
            if(dealerNumAces > 0):
                dealerValue -= 10
                dealerNumAces -= 1
            else: break
        print("Dealer value: " + str(dealerValue))
        print("Dealer cards: " + str.join(" ", dealerCards))
    await client.say("Bot went!")




@client.command()
async def hangman():
    global playingHangman
    global word
    global guessesLeft
    global blanks
    global lettersFound
    global guessedLetters
    lines = []
    with open("hangmanwords.txt", "r") as f:
        lines = f.readlines()
    random_line_num = random.randrange(0, len(lines))
    word = lines[random_line_num]
    f.close()
    blanks = []
    guessedLetters = []
    lettersFound = 0
    guessesLeft = 6
    playingHangman = True
    for i in range(1, len(word)):
        blanks .append("-")
    await client.say("""`                                                                      
  _                                   
 | |_  ____ _ _  __ _ _ __  __ _ _ _  
 | - \/ -  | - \/ -  |  - \/ -  | - \ 
 |_||_\__,_|_||_\__, |_|_|_\__,_|_||_|
                |___/                                                                                                   
`""")

    await client.say("Welcome to hangman.")
    await client.say("You have " + str(guessesLeft) + " "
                                                      "guesses to get all of the letters in the word.  "
                                                      "To guess a letter, type .guess letter \n" + " ".join(blanks))

@client.command()
async def guess(guess):
    global playingHangman
    global word
    global guessesLeft
    global blanks
    global lettersFound
    global guessedLetters
    if playingHangman is True:
        if str.isalpha(guess) and len(guess) is 1 and str.lower(guess) not in guessedLetters:
            if str.lower(guess) in word:
                await client.say(guess + " is in the word.  Good job!")
                for i in range(0, len(word)):
                    if word[i] == str.lower(guess):
                        blanks[i] = str.lower(guess)
                        lettersFound += 1

            else:
                await client.say(guess + " is NOT in the word.")
                guessesLeft -= 1

            guessedLetters.append(str.lower(guess))
            await client.say(" ".join(blanks))
            await client.say("Guessed letters: " + " ".join(guessedLetters))
            await client.say("Guesses left: " + str(guessesLeft))

            if guessesLeft == 0:
                await client.say("No guesses left.  You lose!")
                playingHangman = False
            elif lettersFound == len(word):
                await client.say("You guessed all the letters!  You've won!  The word was: " + word)
                playingHangman = False

        else:
            await client.say("ERROR: You can only guess with single letters that haven't already been entered.")
            await client.say("Guessed letters: " + " ".join(guessedLetters))

    else: await client.say("Start a game of Hangman with .hangman before trying to guess a letter!")


client.run("")