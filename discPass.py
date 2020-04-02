from discord.ext import commands

from testSql import session, Member, Poste

bot = commands.Bot(command_prefix=';')

TOKEN = 'Njk1MzI3NDUzODI0MTU1Nzg5.XoYkhA.D7FkLNUAD2lZqVSoFyTW6_SI8JY'


@bot.command(description='Show information about the project')
async def info(context: commands.context.Context):
    """ Show information about the project """
    await context.channel.send("""```This bot registers to the vote.\n Use ;register to register```""")


@bot.command(description='Register to the vote')
async def register(context: commands.context.Context):
    """ Register to the vote """
    message = "```"
    q = session.query(Member).filter(Member.discord_id == context.author.id).first()
    if q is not None:
        message += context.author.display_name + " is a little cheater, right ?"
    else:
        administrator = (context.guild.owner_id == context.author.id)
        member = Member(discord_id=context.author.id, name=context.author.display_name, is_verified=administrator,
                        is_admin=administrator, avote=False)
        session.add(member)
        session.commit()
        message += context.author.display_name + " registered to the vote"
    message += "```"
    await context.channel.send(message)


@bot.command(description='list the members')
async def listing(context: commands.context.Context):
    """list the members"""
    message = "```\n"
    for member in session.query(Member).all():
        message += member.name + " is verified ? " + str(member.is_verified) + "\n"
    message += "```"
    await context.channel.send(message)


@bot.command(description='allows an admin to verify a member')
async def verify(context: commands.context.Context, *args):
    """allows an admin to verify a member"""
    message = "```\n"
    q = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    if q is None:
        message += "You're not an admin..."
    else:
        for member in session.query(Member).all():
            for arg in args:
                if arg in member.name:
                    member.is_verified = True
                    message += member.name + " has been verified\n"
    message += "```"
    await context.channel.send(message)


@bot.command(description='allows an admin set a member to admin')
async def admins(context: commands.context.Context, *args):
    """allows an admin set a member to admin"""
    message = "```\n"
    q = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    if q is None:
        message += "You're not an admin..."
    else:
        for member in session.query(Member).all():
            for arg in args:
                if arg in member.name:
                    member.is_admin = True
                    message += member.name + " has been verified\n"
    message += "```"
    await context.channel.send(message)


@bot.command(description='allows an admin to remove a member')
async def unverify(context: commands.context.Context, *args):
    """allows an admin to unverify a member"""
    message = "```\n"
    q = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    if q is not None:
        message += "You're not an admin..."
    else:
        for member in session.query(Member).all():
            for arg in args:
                if arg in member.name:
                    member.is_verified = False
                    message += member.name + " has been unverified\n"
    message += "```"
    await context.channel.send(message)


@bot.command(description='adds a post')
async def add_post(context: commands.context.Context, name, rank):
    """Adds a Post to the list of posts. Usage : ;addPost name rank"""
    message = "```"
    p = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    q = session.query(Poste).filter(name == Poste.name).first()
    if p is None:
        message += "You're not an admin..."
    else:
        if q is not None:
            message += "The post " + Poste.name + " already exists at rank " + Poste.rank
        else:
            post = Poste(name=name, rank=rank)
            session.add(post)
            session.commit()
            message += "The post " + Poste.name + " was added at rank " + Poste.rank
    message += "```"
    await context.channel.send(message)


@bot.command(description='removes a post')
async def remove_post(context: commands.context.Context, name, rank):
    """removes a Post to the list of posts. Usage : ;removePost name rank"""
    message = "```"
    p = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    q = session.query(Poste).filter(name == Poste.name).first()
    if p is None:
        message += "You're not an admin..."
    else:
        if q is None:
            message += "The post " + Poste.name + " doesn't exists at rank " + Poste.rank
        else:
            session.delete(q)
            session.commit()
            message += "The post " + Poste.name + " was removed at rank " + Poste.rank
    message += "```"
    await context.channel.send(message)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)
