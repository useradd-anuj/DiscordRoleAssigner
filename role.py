import discord
from discord.ext import commands
import numpy as np

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
@commands.has_role("LW-Core TEAM")#change as per your req
async def role(ctx:commands.context.Context, arg:str):
    guild = ctx.guild
    try:
        #reading from the file
        memlist=str(await ctx.message.attachments[0].read(),encoding='utf-8')
    except:
        #if there is no file that is uploaded with the message this runs
        await ctx.send("Pls upload a csv file")
        return
        
    try:
        role = discord.utils.get(guild.roles, name=arg)
    except:
        await ctx.send("There is some problem fetching the role.")
        return
    
    if not role: #when no role exist,as defined in argument 
        await ctx.send("role not found pls create the role first")
        return
        
    if memlist.endswith('\n'):
        memlist=memlist[:len(memlist)-1]
    
    memlist=memlist.split('\n')

    i=0
    while i!=len(memlist):
        memlist[i]=memlist[i].split(',')# type: ignore            
        i=i+1
    del i
    
    memlist=np.array(memlist,dtype=str)
    
    i=0
    while "username" not in memlist[0,i].strip().lower():
        i=i+1
    memlist=memlist[1:,i]
    #print(memlist)
    for i in memlist:
        i=i[:len(i)-1]
        print(i)
        user = guild.get_member_named(i)
        #user.add_roles()
        await user.add_roles(role)
        await ctx.send(i+" set role of "+arg)

bot.run('Your Token here')
