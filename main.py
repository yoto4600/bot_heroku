import discord
from discord.ext import commands, tasks
import random

bot = commands.Bot(command_prefix = "y!", description = "bot de yoto4600")
status = ["!help",
                "A votre service",
                "L'eau mouille", 
                "Le feu brule", 
                "Lorsque vous volez, vous ne touchez pas le sol", 
                "Winter is coming", 
                "Mon créateur est yoto4600", 
                "Il n'est pas possible d'aller dans l'espace en restant sur terre", 
                "La terre est ronde",
                "La moitié de 2 est 1",
                "7 est un nombre heureux",
                "Les allemands viennent d'allemagne",
                "Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
                "J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
                "Le plus grand complot de l'humanité est",
                "Pourquoi lisez vous ca ?"]


@bot.event
async def on_ready():
        print("Ready !")
        changeStatus.start()

@bot.command()
async def start(ctx, secondes = 5):
    changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status = discord.Status.dnd, activity = game)    

@bot.command()
async def serverInfo(ctx):
        server = ctx.guild
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        serverDescription = server.description
        numberOfPerson = server.member_count
        serverName = server.name
        message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
        await ctx.send(message)

@bot.command()
async def say(ctx, *texte):
    await ctx.send(" ".join(texte))

@bot.command()
async def chinese(ctx, *text):
        chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
        chineseText = []
        for word in text:
                for char in word:
                        if char.isalpha():
                                index = ord(char) - ord("a")
                                transformed = chineseChar[index]
                                chineseText.append(transformed)
                        else:
                                chineseText.append(char)
                chineseText.append(" ")
        await ctx.send(" ".join(chineseText))

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
        messages = await ctx.channel.history(limit = nombre + 1).flatten()
        for message in messages:
                await message.delete()

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.user, *reason):
        reason = " ".join(reason)
        await ctx.gild.kick(user, reason = reason)
        await ctx.send(f"{user} à été kick de {serverName}")

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.user, *reason):
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason = reason)
        await ctx.send(f"{user} à été ban de {serverName} ")

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
                if i.user.name == userName and i.user.discriminator == userId:
                        await ctx.guld.unban(i.user, reason = reason)
                        await ctx.send(f"{user} à été unban de {serverName}")
                        return
        await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
async def bansId(ctx):
        ids = []
        bans = await ctx.guild.ban()
        for i in bans:
            ids.append(str(i.user.id))
        await ctx.send("La liste des id des utilisateurs bannis du serveur est :")
        await ctx.send("\n".join(ids))
        
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")

    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole   

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)    
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
async def umute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)   
    await ctx.send(f"{member.mention} a été unmute !")
bot.run("ODU4NDI1NTk0MDYwNzM0NTE1.YNd9Ig.WE-iaSWKkKxUcWD9rvqpSZYM15Q")