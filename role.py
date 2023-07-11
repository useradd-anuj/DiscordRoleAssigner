import discord
from discord.ext import commands
import numpy as np

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
@commands.has_role("LW-Core TEAM")
async def role(ctx:commands.context.Context, arg:str):
    guild = ctx.guild
    try:
        memlist=str(await ctx.message.attachments[0].read(),encoding='utf-8')
    except:
        await ctx.send("Pls upload a csv file")
        return
    #print("READ in original",'\n',memlist)
    try:
        role = discord.utils.get(guild.roles, name=arg)
    except:
        await ctx.send("There is some problem fetching the role.")
        return
    
    if not role:
        await ctx.send("role not found pls create the role first")
        return
    if memlist.endswith('\n'):
        memlist=memlist[:len(memlist)-1]
    
    memlist=memlist.split('\n')
    #print("\n\nlist splited by \\n",'\n',memlist)

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

bot.run('MTEyNzI0OTU2OTI5ODc4ODQwNQ.GV5DpO.ffrHwS5JQay4zzWo1wf607nQSMpEExZt10rIrg')
