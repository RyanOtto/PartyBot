import discord
from discord.ext.commands import Bot
from discord.ext import commands 
import asyncio
import random
from bs4 import BeautifulSoup
import urllib.request
import os
from boto.s3.connection import S3Connection

Client = discord.Client()
client = commands.Bot(command_prefix='$')
client.remove_command("help")

# Hangman variables
word = ""
guessesLeft = 6
playingHangman = False
blanks = []
guessedLetters=[]
lettersFound = 0

# Blackjack variables
playingBlackJack = False
dealerValue = 0
playerValue = 0
dealerCards = []
playerCards = []
dealerNumAces = 0
playerNumAces = 0
cardNames = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine',
             10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
cardValues = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 10, 12: 10, 13: 10, 14: 11}

# Rock paper scissors variables (1 == rock, 2 == paper, 3 == scissors)
playingRPS = False
aiChoice = 0
playerChoice = 0
aiPoints = 0
playerPoints = 0

# Riddle variables
answering = False
riddle = ""
riddleAnswer = ""
riddleLine = 0
riddleGuessesLeft = 3
prevRiddleLine = 0

# Good Morning variables
gmOptionEnabled = False

@client.event
async def on_message(message):
    author = message.author
    if str.lower(message.content) == 'good morning' or str.lower(message.content) == 'morning' or str.lower(message.content) == 'mornin':
        await client.send_message(message.channel, 'Hello, ' + author)

@client.command()
async def morninggreet(nOrOff):
    global gmOptionEnabled
    if str.lower(onOrOff) == "on" and gmOptionEnabled == False:
        gmOptionEnabled = True
        await client.say("PartyBot will now greet people when they say good morning")
    elif str.lower(onOrOff) == "off" and gmOptionEnabled == True:
        gmOptionEnabled = False
        await client.say("PartyBot will no longer greet people when they say good morning")

@client.command()
async def search(*, word):
    linkWord = word.replace(' ', '+')
    url = 'http://www.dictionary.com/browse/' + linkWord
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    header = soup.find( "header", {"class":"luna-data-header"} ).text
    definition = soup.find( "div", {"class":"def-set"} ).text
    await client.say(word + ":" + header + definition[3:])

@client.command()
async def usearch(*, word):
    linkWord = word.replace(' ', '+')
    url = 'https://www.urbandictionary.com/define.php?term=' + linkWord
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    definition = soup.find("div", {"class": "meaning"}).text
    definition = definition.replace("&apos;", "")
    example = soup.find("div", {"class": "example"}).text
    example = example.replace("&apos;", "")
    await client.say(word + ": " + definition + "\n\n" + example)

@client.command()
async def riddle():
    global riddle, riddleLine, prevRiddleLine, riddleAnswer, riddleGuessesLeft, answering
    answering = True
    riddle = ""
    riddleAnswer = ""
    riddleGuessesLeft = 3

    with open("riddles.txt", "r") as f:
        lines = f.readlines()
    while riddle == "" or "=" in riddle or riddleLine == prevRiddleLine:
        riddleLine = random.randrange(0, len(lines))
        riddle = lines[riddleLine]
        riddleAnswer = lines[riddleLine+1]
    prevRiddleLine = riddleLine
    f.close()

    riddleAnswer = riddleAnswer.replace("=", "")
    riddleAnswer = riddleAnswer.replace(" ", "")

    await client.say("Use $answer <word> to solve the riddle.  All answers to these riddles will be one word or number.  You have three guesses per riddle.\n\n" + "`"+riddle+"`")

@client.command()
async def answer(userAnswer):
    global riddleAnswer, riddleGuessesLeft, answering

    if answering is False:
        await client.say("Use $riddle to receive another riddle")
        return

    userAnswer = userAnswer.strip()
    riddleAnswer = riddleAnswer.strip()

    if str.lower(userAnswer) == str.lower(riddleAnswer):
        await client.say("Correct!")
        answering = False
    else:
        riddleGuessesLeft -= 1
        await client.say("Incorrect!  Guesses left:" + str(riddleGuessesLeft))
    if riddleGuessesLeft == 0:
        await client.say("Out of guesses!  The answer was: " + riddleAnswer)

@client.event 
async def on_ready(): 
    print("Bot Online!") 
    print("Name: {}".format(client.user.name)) 
    print("ID: {}".format(client.user.id))

@client.command()
async def help():
    await client.say("`GAMES\n$hangman -> Start a new game of hangman"
                     "\n$blackjack -> Start a new game of blackjack"
                     "\n$riddle -> Get a riddle to answer"
                     "\n$rps -> Start a new game of rock, paper, scissors "
                     "\nUTILITY\n$search <word> to search for a word's definition"
                     "\n$usearch <word> to search for an urban dictionary word's definition`"
                     "\n$morninggreet <on/off> to turn on bot greeting in response to user greetings (IE 'good morning')")

@client.command()
async def rps():
    await client.say("""`
------           -     ------                        -----      -                        
| ___ \         | |    | --- \                      /  ___|    (_)                       
| |_/ /---   ---| | __ | |_/ /--- - --   ---  ----| \  --.  --- - --- ---  --- |----|--- 
|    // _ \ /---| |/ / |  --/ _  |  _ \ / - \|  __|  ---. \/ __| / __/ __|/ _ \|  --| __|
| |\ \ (_) | (__|   <  | | | (_| | |_) |  --/| |    /\__/ / (__| \__ \__ \ (_) | |  \__ 
\_| \_\---/ \---|_|\_\ \_|  \__ _|  __/ \--- |_|    \____/ \___|_|___/___/\___/|_|  |___/
                                 | |                                                    
                                 |_|                                                                                                                                              
    `""")

    await client.say("Type $choose rock/paper/scissors to make your choice for the round.  First to 3 points wins! ")
    global playingRPS
    playingRPS = True

@client.command()
async def choose(rockPaperOrScissors):
    global playingRPS, aiChoice, playerChoice, aiPoints, playerPoints

    if playingRPS is False:
        await client.say("Type $rps to play a game of rock paper scissors!")
        return

    #AI choice
    aiChoice = random.randrange(1,4)
    choiceList = {1:"rock", 2:"paper", 3:"scissors"}

    #Player choice
    if str.lower(rockPaperOrScissors) == "rock": playerChoice = 1
    if str.lower(rockPaperOrScissors) == "paper": playerChoice = 2
    if str.lower(rockPaperOrScissors) == "scissors": playerChoice = 3

    #See who won
    await client.say("You picked: " + rockPaperOrScissors + " and AI picked: " + choiceList[aiChoice] + ".")
    if playerChoice is 1 and aiChoice is 3 or playerChoice is 2 and aiChoice is 1 or playerChoice is 3 and aiChoice is 2:
        playerPoints += 1
        await client.say("You win the round!")
    elif playerChoice == aiChoice:
        await client.say("Tie!")
    else:
        aiPoints += 1
        await client.say("AI wins the round!")

    #End game if someone hit 3 points
    if playerPoints == 3:
        await client.say("You hit 3 points.  You win!")
        await endRPS()
        return
    if aiPoints == 3:
        await client.say("AI hit 3 points.  You lose!")
        await endRPS()
        return
    await client.say("Type $choose <rock/paper/scissors> to continue. ")
    await client.say("SCORE -> Player: " + str(playerPoints) + " AI: " + str(aiPoints))

async def endRPS():
    global playingRPS, aiChoice, playerChoice, aiPoints, playerPoints
    playingRPS = False
    aiChoice = 0
    playerChoice = 0
    aiPoints = 0
    playerPoints = 0

async def printCards(playerOrComputer):
    if playerOrComputer is 1:
        await client.say("Your value: " + str(playerValue))
        await client.say("Your cards: " + str.join(" ", playerCards))
    elif playerOrComputer is 2:
        await client.say("Dealer value: " + str(dealerValue))
        await client.say("Dealer cards: " + str.join(" ", dealerCards))
    elif playerOrComputer is 3:
        await client.say("Your value: " + str(playerValue))
        await client.say("Your cards: " + str.join(" ", playerCards))
        await client.say("Dealer value: " + str(dealerValue))
        await client.say("Dealer cards: " + str.join(" ", dealerCards))

async def resetBlackJack(finishedOrReset):
    global playingBlackJack, dealerValue, playerValue, dealerCards, playerCards, dealerNumAces, playerNumAces, cardNames, cardValues
    if finishedOrReset is 0:
        await printCards(3) #Print both player and AI's values and cards
        if(playerValue > 21 or playerValue <= 21 and dealerValue <= 21 and playerValue < dealerValue):
            await client.say("You lose!")
        elif(dealerValue > 21 or playerValue <= 21 and dealerValue <= 21 and playerValue > dealerValue):
            await client.say("You win!")
        playingBlackJack = False
    dealerValue = 0
    playerValue = 0
    dealerCards = []
    playerCards = []
    dealerNumAces = 0
    playerNumAces = 0

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
    await resetBlackJack(1)
    global playingBlackJack, dealerValue, playerValue, dealerCards, playerCards, dealerNumAces, playerNumAces, cardNames, cardValues
    playingBlackJack = True

    #Simulate dealer's turn
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

    #Give player 2 cards
    for i in range(0,2):
        nextCard = random.randrange(1, 15)
        playerValue += cardValues[nextCard]
        playerCards.append(cardNames[nextCard])

    #print("Dealer value: " + str(dealerValue))
    #print("Dealer cards: " + str.join(" ", dealerCards))
    await client.say("Say $hit to be dealt another card, and $stay to stick with your current total value.")
    await client.say("Dealer's first card is: " + dealerCards[0])
    await printCards(1) #Print player cards/value

@client.command()
async def hit():
    if playingBlackJack is False:
        await client.say("Type $blackjack to begin a game of blackjack")
        return
    global playerValue, playerCards, playerNumAces
    nextCard = random.randrange(1, 15)
    if nextCard is 14: playerNumAces += 1
    playerCards.append(cardNames[nextCard])
    playerValue += cardValues[nextCard]
    while playerValue > 21:
        if (playerNumAces > 0):
            playerValue -= 10
            playerNumAces -= 1
        else:
            await resetBlackJack(0)
            break
    await printCards(1) #Print player cards/value

@client.command()
async def stay():
    if playingBlackJack is False:
        await client.say("Type $blackjack to begin a game of blackjack")
        return
    await resetBlackJack(0) #End the game

@client.command()
async def hangman():
    global playingHangman, word, guessesLeft, blanks, lettersFound, guessedLetters
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
                                                      "To guess a letter, type $guess letter \n" + " ".join(blanks))

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
            #print(lettersFound)
            #print(len(word))

            if guessesLeft == 0:
                await client.say("No guesses left.  You lose!")
                playingHangman = False
            if lettersFound == len(word)-1:
                await client.say("You guessed all the letters!  You've won!  The word was: " + word)
                playingHangman = False

        else:
            await client.say("ERROR: You can only guess with single letters that haven't already been entered.")
            await client.say("Guessed letters: " + " ".join(guessedLetters))

    else: await client.say("Start a game of Hangman with $hangman before trying to guess a letter!")

s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])
client.run(os.environ['DISCORD'])