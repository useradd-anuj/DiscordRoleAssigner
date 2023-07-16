import discord
from discord.ext import commands
import numpy as np

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

bot.remove_command("help")

@bot.command()
async def help(ctx):
    await ctx.send("The commands are as below.\n1. $help --> to see this help.\n2. $role --> assigns role by taking rolename and csv file, respectively.\n3. $instant --> assign role to single user by taking rolename and username in the same order.\n\nNote: the username must be the one that is below the user's display name. If not present display name of the user will do.")


@bot.command()
@commands.has_role("LW-Core TEAM")
async def instant(ctx:commands.context.Context, rolename:str, username:str):
    user = ctx.guild.get_member_named(username)
    role = discord.utils.get(ctx.guild.roles, name=rolename)
    if role is None:
        await ctx.send(rolename+"does not exist")
        return
    if user is not None:
        await user.add_roles(role)
        await ctx.send(username+" given role to "+ rolename)
    else:
        await ctx.send(username+" cannot be found or user has used deprecated username")

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

    i=0
    while i!=len(memlist):
        memlist[i]=memlist[i].split(',')# type: ignore            
        i=i+1
    
    memlist=np.array(memlist,dtype=str)
    
    i=0
    while "username" not in memlist[0,i].strip().lower():
        i=i+1
    
    memlist=memlist[1:,i]
    
    for i in memlist:
        i=i[:len(i)-1]
        print(i)
        user = guild.get_member_named(i)
        if user is not None:
            await user.add_roles(role)
            await ctx.send(i+" set role of "+arg)
        else:
            await ctx.send(i+" cannot be found or user has used deprecated username")

@bot.event
async def on_command_error(ctx:commands.context.Context, error):
    if isinstance(error, commands.MissingRole):
        try:
            await ctx.send("users with "+error.args[0][0].lower()+error.args[0][1:])
        except:
            await ctx.send("You don't have permission to run this bot.\nContact the server admin if this a mistake.")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("either role name or username is missing.\n\nThe syntax is $command rolename <username or the csv file> based upon the command name.\n$help to see list of commands.")
    else:
        raise error


bot.run('Your token here')
