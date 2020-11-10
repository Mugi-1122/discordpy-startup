from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()
ch_id1 = 768052430172061717
ch_id2 = 768052555208327168
s1_id = 637735141598560268
s2_id = 767192822352052235

@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)
    channel1 = client.get_channel(ch_id1)
    channel2 = client.get_channel(ch_id2)
    await channel1.send('@everyone オンラインになったよ！')
    await channel2.send('@everyone オンラインになったよ！')

# 返信する非同期関数を定義
async def reply(message, file_data):
    guild_id = f'{message.guild.id}'# 送信されたサーバーのid
    channel_1 = client.get_channel(ch_id1)
    channel_2 = client.get_channel(ch_id2)
    sender_user_name = message.author.name
    if message.attachments == [] :
        reply = f'**Sender : {sender_user_name}** \n{message.content}'# 返信メッセージの作成
    elif message.content == "":
        reply = f'**Sender : {sender_user_name}** \n**URL** : {file_data.url}'#file_data.urlは#attachments内のurlを取り出している
    else:
        reply = f'**Sender : {sender_user_name}** \n{message.content} \n**URL** : {file_data.url}'
    print(message)
    print(file_data)
    print("guild_name => " + message.guild.name+ " , " + "sender => " + sender_user_name + "#" + message.author.discriminator + " , "  + "message => " + message.content)
    print("*----------*----------*----------*")

    if (int(guild_id) == int(s1_id)) :
        await channel_2.send(reply) # 返信メッセージを送信
    elif (int(guild_id) == int(s2_id)) :
        await channel_1.send(reply)
    else :
        await channel_1.send('idが設定されていません')
        await channel_2.send('idが設定されていません')

# 発言時に実行されるイベントハンドラを定義
@client.event
async def on_message(message):
    if message.author.bot:
        return
    #if client.user in message.mentions: # 話しかけられたかの判定
    elif(message.attachments == []):#ファイルが送信されていないか
        file_data = "FileData is none"
        await reply(message, file_data) # 返信する非同期関数を実行
    else:
        file_data = message.attachments[0] #attachmentsの取り出し
        await reply(message, file_data)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


bot.run(token)
