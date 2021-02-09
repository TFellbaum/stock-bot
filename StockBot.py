import boto3
import discord
import json
import os
from aiohttp import ClientSession
from boto3.dynamodb.conditions import Key, Attr
from discord import Embed, Color
from discord.ext import commands, tasks
from dotenv import load_dotenv


# Loads env file with Discord Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TOONTOWN_CHANNEL = int(os.getenv('DISCORD_STOCK_CHANNEL'))
REGION = os.getenv('AWS_DEFAULT_REGION')

# Starts client and initializes stocks and messages
client = discord.Client()
dynamodb = boto3.resource('dynamodb', region_name=REGION)
#stockRequestsTable = dynamodb.Table('stock-requests')
stocks = set()
messages = set()
mentionRequests = set()


# Stock Class
class Stock(object):
    def __init__(self, stock):
        self.stock = stock
        self.message = ''

    def __eq__(self, other):
        return self.stock == other.stock

    def __hash__(self):
        return hash(self.stock)


# Stock Request Class
class StockRequest(object):
    def __init__(self, user, stock):
        self.user = user
        self.stock = stock

    def __eq__(self, other):
        return self.user == other.user and self.stock == other.stock

    def __hash__(self):
        return hash((self.user, self.stock))

# Starts retrieving stocks when StockBot is ready/connected
@client.event
async def on_ready():
    print('{0} has connected to Discord!'.format(client.user.name))
#/    purging = await purgeMessages()
#/    while(not purging is None and len(purging) > 0):
#/        purging = await purgeMessages()

#/    await sendHelpMessage()
#/    await initializeMentionRequests() 
#/    await retrieveStocks.start()


# Retrieves and updates stocks and messages every 30 seconds
@tasks.loop(seconds=30)
async def retrieveStocks():
    print("Retrieving stocks")
    # Start Client session and GET Stock API Response
#/    async with ClientSession() as session:
#/        async with session.get("Some stock API") as response:
            # Retrieve and parse json stock data
#/            html = await response.text()
#/            stockData = json.loads(html)

            # Keep track of most recent stock data - API record tracker
#/            updatedStocks = set()

            # Traverse API pulled stock Data
#/           for s in stockData:
#/                updatedStock = createStock(s)
#/                updatedStocks.add(updatedStock)

                # If the most recent stockData is already in tracked stocks, edit the message and continue to next stock
                # At this point updatedStock (API Data) has no message id but updated data and s in stocks has a message id but old data
#/                if updatedStock in stocks:
#/                    for stock in stocks:
#/                        if updatedStock == stock:
#/                            messageToEdit = await fetchMessage(stock.message)
#/                            await editMessage(messageToEdit, updatedStock)
#/                    continue
                
                # Else send a new stock message, create message id and add it to tracked stock and tracked messages
#/                else:
#/                    message = await sendMessage(updatedStock)
#/                    updatedStock.message = message.id
#/                    stocks.add(updatedStock)
#/                    messages.add(message.id)

            # After editing or creating messages, check if any stock ended and messages need to be deleted
#/            for stock in stocks:
#/                if stock in updatedStocks:
                    # This is necessary because data within sets are immutable. stocks has objects with message ids where
                    # updatedStocks does not. This removes the similar stockObjects to add the message id to the updatedStocks
#/                    updatedStocks.remove(stock)
#/                    updatedStocks.add(stock)

            # Updates tracked stocks with most recent API stocks via intersection then delete ended stock messages    
#/            stocks.intersection_update(updatedStocks)
#/            await deleteMessages()


# Checks if a user requested a mention for stocks
@client.event
async def on_message(message):
    if isBot(message):
        return

    # Requests a specific stock to track
    if 'i want ' in message.content.lower():
        print("start tracking stock")
#/       stock = message.content[#7:]
#/       user = message.author.id
#/       mentionRequest = MentionRequest(user, stock)
#/       mentionRequests.add(mentionRequest)
#/       mentionRequestsTable.put_item(
#/           Item={
#/               'user': str(user),
#/               'stock': stock
#/           }
#/        )
#/       await message.delete()

    # Requests to stop tracking all stocks
    elif 'stop tracking stocks' in message.content.lower():
        print("stock tracking all stocks")
#/        mentionsToRemove = set()
#/        for mention in mentionRequests:
#/            if mention.user == message.author.id:
#/                mentionsToRemove.add(mention)
#/
#/        for mention in mentionsToRemove:
#/            mentionRequests.remove(mention)
#/            mentionRequestsTable.delete_item(
#/                Key={
#/                    'user': str(mention.user),
#/                    'stock': mention.stock
#/                }
#/            )
#/        await message.delete()

    # Requests to stop tracking a specific stock
    elif 'stop tracking ' in message.content.lower():
        print("Stop tracking stocks")
#/        stock = message.content[#14:]
#/        mentionsToRemove = set()
#/        for mention in mentionRequests:
#/            if mention.user == message.author.id and (mention.stock == stock):
#/                mentionsToRemove.add(mention)
#/
#/        for mention in mentionsToRemove:
#/            mentionRequests.remove(mention)
#/            mentionRequestsTable.delete_item(
#/                Key={
#/                    'user': str(mention.user),
#/                    'stock': mention.stock
#/                }
#/            )
#/        await message.delete()

    # Shows all of users currently tracked stocks
    elif 'tracked stocks' in message.content.lower():
        content = ''
        for mention in mentionRequests:
            if mention.user == message.author.id:
                content = content + mention.stock + '\n'
        content = content.strip()
        if len(content) > 0:
            await getChannel().send(content=content)
        else:
            await getChannel().send(content='{0} is not tracking any stocks'.format(message.author.name.split('#')[0]))

    # Displays help info
    elif 'help stockbot' in message.content.lower():
        await sendHelpMessage()

        
# Sends and returns message in Discord Channel
async def sendMessage(stock):
    print("send message")
#/    embed, mentions = createMessage(stock)
#/    message = await getChannel().send(content=mentions, embed=embed)
#/    return message


# Fetches and edits message in Discord Channel
async def editMessage(message, newStockData):
    print("edit message")
#/    editedMessage, mentions = createMessage(newStockData)
#/    await message.edit(content=mentions, embed=editedMessage)


# Deletes messages for stocks removed    
async def deleteMessages():
    # Creates a set of only current stock message ids
    currentStockMessages = set()
    for s in stocks:
        currentStockMessages.add(s.message)

    # Takes the difference of the newly updated stocks with new messages and the current messages still left in the list to determine
    # if any stocks have disappeared thus ended and removes them from messages tracker and deletes accordingly
    messagesToDelete = messages.difference(currentStockMessages)
    for message in messagesToDelete:
        deleteMessage = await getChannel().fetch_message(message)
        await deleteMessage.delete()
        messages.remove(message)


# Gets message object from id
async def fetchMessage(messageId):
    return await getChannel().fetch_message(messageId)


# Sends help message
async def sendHelpMessage():
    print("Send help message")
#/    content = str("""```bash\n""" + "Help Message" + """```""")
#/    await getChannel().send(content)


# Initializes stock requests upon Bot start
async def initializeStockRequests():
    print("Initializing")
#/    response = stockRequestsTable.scan()
#/    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
#/        items = response['Items']
#/        for request in items:
#/           user = int(request['user'])
#/           stock = request['stock']
#/           stockRequest = StockRequest(user, stock)
#/           stockRequests.add(stockRequest)
        

# Deletes all StockBot messages upon application start
async def purgeMessages():
    deleted = await getChannel().purge(limit=100)
    return deleted


# Gets and formats mention requests for messages
def getMentionRequests(stock):
    print("getMentionRequests")
#/    usersToMention = set()
#/    for mention in mentionRequests:
#/        if mention.stock.lower() == stock.lower():
#/            usersToMention.add('<@{0}>'.format(mention.user))
#/            
#/    content = ''
#/    for mention in usersToMention:
#/        content = content + mention + ' '
#/    content = content.strip()
#/    return content


# Creates embeded message
def createMessage(stock):
    print("Create message")
#/    mentions = getStockRequests(stock.stock)
#/    embed = Embed(color=getStockColor(stock.stock))
#/    embed.set_author(name='Stock Name',
#/                     icon_url="Stock Icon",
#/                     url='stock Url')
#/    embed.description = 'Stock description'
#/    return embed, mentions


# Checks if message is sent by StockBot
def isBot(message):
    return message.author == client.user


# Gets message color based on stock type for fun
def getStockColor(stock):
    return Color.dark_theme()


# Parses stock to create Stock Object
def createStock(stock):
    print("create stock")
#/    stockInfo = "Some stock"
#/    return Stock(stockInfo)


# Gets Discord Channel
def getChannel():
    return client.get_channel(id=TOONTOWN_CHANNEL) #TOONTOWN_CHANNEL is for Rmy

                
client.run(TOKEN)
