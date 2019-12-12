from discord.ext import commands
import discord
import youtube_dl
import random

token = "NTU5NjM5MTM5OTg5OTc5MTY2.D3qpGg.YuPFDl_ouZYf5W2BPw9ekF--KsU"
client = commands.Bot(command_prefix='e ')

players = {}
queues = {}

def check_queue(id):
    # if(queues != False):
        player = queues[id].pop(0)
        player[id] = player
        player.start()



# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('em'):
#         msg = 'Hello {0.author.mention}'.format(message)
#         await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def ping():
    await client.say('Pong!')

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    return await client.say("Connected.")


@client.command(pass_context=True)
async def leave(ctx):
    for i in client.voice_clients:
        if(i.server == ctx.message.server):
            await i.disconnect()
            players.clear()
            return await client.say("Disconnected.")
    return await client.say("I'm not connected to any voice channel.")

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    if(not players):
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, ytdl_options = {'default_search': 'auto'}, after=lambda: check_queue(server.id))
        players[server.id] = player
        player.start()
        return await client.say("Playing...")
    else:
        await client.say("I can only play one song at a time.")

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await client.say("Paused.")

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await client.say("Resumed.")

@client.command(pass_context=True)
async def skip(ctx):
    id = ctx.message.server.id
    players[id].stop()
    await client.say("Skipped.")

@client.command(pass_context=True)
async def stop(ctx):
    for i in client.voice_clients:
        if(i.server == ctx.message.server):
            await i.disconnect()
            players.clear()
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
            return await client.say("Stopped.")
    await client.say("I'm not connected to any voice channels.")

@client.command(pass_context=True)
async def q(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say("Queued.")

@client.command(pass_context=True)
async def loop(ctx):
    if('559928632659935242' in [role.id for role in ctx.message.author.roles]):
        await client.say("Looped.")
    else:
        await client.say("You don't have looping permissions.")

@client.command(pass_context=True)
async def ahri():


@client.command()
async def eightball(name='8ball',description='Answers yes/no questions.', brief='8ball q\'s',pass_context=True):
    possible_responses = [
        'Yes',
        'No', 
        'Not Likely',
        'It is certain'
        'Too hard to tell'
    ]
    await client.say(random.choice(possible_responses))

client.run(token)
