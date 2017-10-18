import discord 
from discord.ext.commands import Bot
from discord.ext import commands 
import asyncio
import random 

#TODO: Merge list into string

Client = discord.Client() 
client = commands.Bot(command_prefix='.') 
word = ""
guessesLeft = 6
playingHangman = False
blanks = []
lettersFound = 0


@client.event 
async def on_ready(): 
    print("Bot Online!") 
    print("Name: {}".format(client.user.name)) 
    print("ID: {}".format(client.user.id)) 



@client.command()
async def hangman():
    global playingHangman
    global word
    global guessesLeft
    global blanks
    word="test"
    playingHangman = True
    for i in range(0, len(word)):
        blanks .append("-")
    guessesLeft = 6
    await client.say("""`                                                                                 
  _                                   
 | |_  ____ _ _  __ _ _ __  __ _ _ _  
 | ' \/ _  | ' \/ _' | '  \/ _' | ' \ 
 |_||_\__,_|_||_\__, |_|_|_\__,_|_||_|
                |___/                                                                                                   
`""")

    await client.say("Welcome to hangman.")
    await client.say("You have " + str(guessesLeft) + " "
                                                      "guesses to get all of the letters in the word.  "
                                                      "To guess a letter, type .guess letter \n" + str(blanks))

@client.command()
async def guess(guess):
    global playingHangman
    if playingHangman is True:
        if str.isalpha(guess) and len(guess) is 1:
            global word
            global guessesLeft
            global blanks
            global lettersFound
            if guess in word:
                await client.say(guess + " is in the word.  Good job!  Guess again!")
                for i in range(0, len(word)):
                    if word[i] == guess:
                        blanks[i] = guess
                        lettersFound += 1
                await client.say(blanks)
            else:
                await client.say(guess + " is NOT in the word.  Guess again!")
                guessesLeft -= 1
            await client.say("Guesses left: " + str(guessesLeft))
            if guessesLeft == 0:
                await client.say("No guesses left.  You lose!")
                playingHangman = False
            elif lettersFound == len(word):
                await client.say("You guessed all the letters!  You've won!  The word was: " + word)
                playingHangman = False
        else:
            await client.say("ERROR: You can only guess with single letters.")
    else: await client.say("Start a game of Hangman with .hangman before trying to guess a letter!")





@client.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await client.say('{0.name} joined in {0.joined_at}'.format(member))

client.run("")