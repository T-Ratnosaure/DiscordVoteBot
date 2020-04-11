import os

from discord.ext import commands
from dotenv import load_dotenv

from testSql import session, Member, Poste, Candidature, Vote, Start

load_dotenv()
bot = commands.Bot(command_prefix=';')

TOKEN = os.getenv("TOKEN")


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
        liste = []
        for member in session.query(Member).all():
            for arg in args:
                if arg in member.name:
                    liste.append(member)
        if len(liste) == 1:
            liste[0].is_verified = True
            message += liste[0].name + " has been verified\n"
        else:
            message += "Did you mean \n"
            for membre in liste:
                message += membre.name + "\n"
        session.commit()
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
                    message += member.name + " is now admin\n"
        session.commit()
    message += "```"
    await context.channel.send(message)


@bot.command(description='allows an admin to remove a member')
async def unverify(context: commands.context.Context, *args):
    """allows an admin to unverify a member"""
    message = "```\n"
    q = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    if q is None:
        message += "You're not an admin..."
    else:
        for member in session.query(Member).all():
            for arg in args:
                if arg in member.name:
                    member.is_verified = False
                    message += member.name + " has been unverified\n"
        session.commit()
    message += "```"
    await context.channel.send(message)


@bot.command(description='adds a post')
async def add_post(context: commands.context.Context, name, rank):
    """Adds a Post. Usage : ;addPost name rank"""
    message = "```"
    p = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    q = session.query(Poste).filter(name == Poste.name).first()
    if p is None:
        message += "You're not an admin..."
    else:
        if q is not None:
            message += "The post " + q.name + " already exists at rank " + str(q.rank)
        else:
            post = Poste(name=name, rank=rank)
            session.add(post)
            session.commit()
            message += "The post " + post.name + " was added at rank " + str(post.rank)
        session.commit()
    message += "```"
    await context.channel.send(message)


@bot.command(description='removes a post')
async def remove_post(context: commands.context.Context, name):
    """removes a Post. Usage : ;removePost name"""
    message = "```"
    p = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    q = session.query(Poste).filter(name == Poste.name).first()
    if p is None:
        message += "You're not an admin..."
    else:
        if q is None:
            message += "The post " + name + " doesn't exists"
        else:
            session.delete(q)
            message += "The post " + q.name + " was removed"
        session.commit()
    message += "```"
    await context.channel.send(message)


@bot.command(description='Candidate to a poste')
async def candidate(context: commands.context.Context, namePost):
    """Candidate to a post"""
    message = "```"
    verified_member = session.query(Member).filter(Member.discord_id == context.author.id).filter(
        Member.is_verified == True).first()
    post_wanted = session.query(Poste).filter(namePost == Poste.name).first()
    if verified_member is None:
        message += "You're not verified..."
    else:
        if post_wanted is None:
            message += "This post does NOT exist... Did you mean : \n"
            posts = session.query(Poste).all()
            if not posts:
                message = "```No posts created. Add a post first"
            else:
                for post in session.query(Poste).all():
                    message += post.name + "\n"
        else:
            candidat = Candidature(poste_id=post_wanted.id, membre_id=verified_member.id)
            session.add(candidat)
            message += verified_member.name + " wants the post of " + post_wanted.name
    session.commit()
    message += "```"
    await context.channel.send(message)


@bot.command(description='Remove candidature to a poste')
async def remove_candidature(context: commands.context.Context, namePost):
    """Removes your candidature to a post"""
    message = "```"
    verified_member = session.query(Member).filter(Member.discord_id == context.author.id).filter(
        Member.is_verified == True).first()
    post_unwanted = session.query(Poste).filter(namePost == Poste.name).first()
    if verified_member is None:
        message += "You're not verified... So you can't candidate... Why are you trying this ?"
    else:
        if not post_unwanted:
            message += "This post does NOT exist..."
        else:
            candidature = session.query(Candidature).filter(post_unwanted.id == Candidature.poste_id).first()
            if not candidature:
                message += "Vous n'avez pas candidaté au poste de " + namePost
            else:
                message += "Vous avez démissionné de la candidature au poste de " + namePost
                session.delete(candidature)
    session.commit()
    message += "```"
    await context.channel.send(message)


@bot.command(description="starts a voting session")
async def start_session(context: commands.context.Context, namePost):
    """Usage : ;start_session post"""
    message = "```"
    admin = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin == True).first()
    post = session.query(Poste).filter(namePost == Poste.name).first()
    started = session.query(Start).first()
    if not admin:
        message += "You're not an admin..."
    elif not started.is_started:
        message += "A session is already started"
    else:
        if not post:
            message += "Please enter a valid post"
        else:
            start = session.query(Start).first()
            start.is_started = True
            start.poste_id = post.id
            session.commit()
    message += '```'
    await context.channel.send(message)


@bot.command(description="votes for someone")
async def vote(context: commands.context.Context, name):
    """Votes for someone"""
    message = "```"
    start = session.query(Start).first()
    votant = session.query(Member).filter(Member.discord_id == context.author.id).filter(
        Member.id not in Vote.member_id).filter(Member.is_verified == True).first()
    if votant is None:
        message += "You're not verified. Ask an admin for verification. Or you have already voted. Or no session was started"
    elif not start.is_started:
        message += "Ask an admin to start the vote"
    else:
        liste = []
        for member in session.query(Member).all():
            if name in member.name:
                liste.append(member)
        if len(liste) == 1:
            voted = session.query(Member).filter(Member.name == liste[0].name).first()
            message += liste[0].name + " a voté pour" + voted.name + "\n"
            vote = Vote(member_id=liste[0].id, candidat_id=voted.id)
        else:
            message += "Did you mean \n"
            for membre in liste:
                message += membre.name + "\n"
        session.commit()
    message += " Vous ne pourrez pas changer ! \n```"
    await context.channel.send(message)


@bot.command(description="ends the voting session")
async def end_session(context: commands.context.Context):
    """ends session"""
    message = "```"
    admin = session.query(Member).filter(Member.discord_id == context.author.id).filter(Member.is_admin).first()
    start = session.query(Start).first()
    post = session.query(Poste).filter(start.poste_id == Poste.id).first()
    started = session.query(Start).first()
    candidats = session.query(Candidature).filter(Candidature.poste_id == start.poste_id).all()
    votes = session.query(Vote).filter(Vote.poste_id == start.poste_id).all()
    m = 0
    elu = ""
    if not admin:
        message += "You're not an admin..."
    elif not started.is_started:
        message += "No session started"
    else:
        for candidate in candidats:
            u = 0
            for vote in votes:
                if vote.candidat_id == candidate.id:
                    u += 1
            if u > m:
                qui = session.query(Member).filter(Member.id == candidate.member_id).first()
                elu = qui.name
        message += elu + " is elected for the post of " + post.name + "\n"
        start.is_started = False
        start.poste_id = -1
        session.commit()
    message += '```'
    await context.channel.send(message)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)
