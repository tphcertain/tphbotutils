import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with your channel ID
LOG_CHANNEL_ID = 1384031801437323294

SPECIAL_USER_IDS = [
    1355167196665479211,
    1274896524228427776
]

@bot.event
async def on_presence_update(before, after):
    if after.id not in SPECIAL_USER_IDS:
        return

    # Status changed?
    if before.status == after.status:
        return

    # Only respond to truly going offline or coming online
    going_offline = before.status != discord.Status.offline and after.status == discord.Status.offline
    coming_online = before.status == discord.Status.offline and after.status != discord.Status.offline

    if going_offline or coming_online:
        # Make sure to only log ONCE
        user = after
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            if going_offline:
                await log_channel.send(
                    f"⚠️ **Special user went offline:** {user.name}#{user.discriminator}"
                )
            elif coming_online:
                await log_channel.send(
                    f"✅ **Special user came online:** {user.name}#{user.discriminator} is now {after.status}"
                )



@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    status=discord.Status.dnd,
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Void Scary"))


@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(
            f"🗑️ **Message deleted**\n"
            f"**Author:** {message.author.mention}\n"
            f"**Channel:** {message.channel.mention}\n"
            f"**Content:** {message.content}"
        )

@bot.event
async def on_message_edit(before, after):
    if after.author.bot:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(
            f"✏️ **Message edited**\n"
            f"**Author:** {after.author.mention}\n"
            f"**Channel:** {after.channel.mention}\n"
            f"**Before:** {before.content}\n"
            f"**After:** {after.content}"
        )

@bot.event
async def on_member_join(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(
            f"✅ **Member joined:** {member.mention} (ID: {member.id})"
        )

@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(
            f"❌ **Member left:** {member.mention} (ID: {member.id})"
        )

@bot.event
async def on_member_update(before, after):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return

    # Check for role changes
    before_roles = set(before.roles)
    after_roles = set(after.roles)

    added_roles = after_roles - before_roles
    removed_roles = before_roles - after_roles

    for role in added_roles:
        await log_channel.send(
            f"➕ **Role added** to {after.mention}: {role.name}"
        )

    for role in removed_roles:
        await log_channel.send(
            f"➖ **Role removed** from {after.mention}: {role.name}"
        )

@bot.event
async def on_guild_role_update(before, after):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return

    changes = []
    if before.name != after.name:
        changes.append(f"**Name:** `{before.name}` ➜ `{after.name}`")
    if before.permissions != after.permissions:
        changes.append(f"**Permissions changed**")

    if changes:
        await log_channel.send(
            f"⚙️ **Role updated:** {after.mention}\n" +
            "\n".join(changes)
        )


    await bot.process_commands(message)

bot.run('MTM4NzU0MDM1Mjc1MTM3MDQxMQ.Ggjpr7.Wc9IV21LaZW_jffco_SRSipyFGjQR0KSzdfYvY')