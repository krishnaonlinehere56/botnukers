import discord
from discord.ext import commands, tasks
import asyncio
import datetime

# ================== DIRECT CONFIG (NO config.json NEEDED) ==================
TOKEN = "YOUR_BOT_TOKEN_HERE"          # <-- Yahan apna real bot token paste kar do
OWNER_ID = 123456789012345678          # <-- Apna Discord User ID daal do (right-click yourself -> Copy ID)
PREFIX = "$"                           # <-- Apna prefix change kar sakte ho

# Optional settings (change as needed)
ANTINUKE_ENABLED = True                # Antinuke features on/off
AUTOMODE_ENABLED = False               # Antilink etc. on/off
ANTIBOT_ENABLED = True                 # Anti unauthorized bot add

# Whitelists (directly add user/channel IDs here)
whitelist_users = {OWNER_ID}           # Owner automatically whitelisted
whitelist_channels = set()             # Yahan channel IDs add kar sakte ho: {123456789, 987654321}
log_channel_id = None                   # Yahan log channel ID daal do agar chahiye: 123456789012345678

# =============================================================================

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# --- STATUS CYCLE ---
statuses = [
    discord.Activity(type=discord.ActivityType.watching, name=f"over {len(bot.guilds)} servers | {PREFIX}help"),
    discord.Activity(type=discord.ActivityType.watching, name="Humanity Fall"),
    discord.Activity(type=discord.ActivityType.playing, name="Nukers Get Fucked"),
    discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX}antinuke | {PREFIX}help"),
    discord.Activity(type=discord.ActivityType.watching, name="26 Servers Protected ☢️")
]

@tasks.loop(seconds=20)
async def status_cycle():
    await bot.change_presence(activity=statuses[status_cycle.current_loop % len(statuses)])

# --- HELPER FUNCTIONS ---
def is_safe(user_id):
    return (user_id in whitelist_users) or (user_id == bot.user.id) or (user_id == OWNER_ID)

async def send_log(message):
    if log_channel_id:
        channel = bot.get_channel(log_channel_id)
        if channel:
            try:
                await channel.send(message)
            except:
                pass

async def notify_owner(guild, user, action):
    try:
        owner = bot.get_user(OWNER_ID)
        if owner:
            embed = discord.Embed(title="☢️ ULTRON HIGH-LEVEL ALERT: NUKER FUCKED", color=0xFF0000, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Server", value=guild.name, inline=True)
            embed.add_field(name="Nuker", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Neutralized", value=action, inline=False)
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="ULTRON PRIME | Owner Protected, Nukers Destroyed")
            await owner.send(embed=embed)
    except:
        pass

async def punish_nuker(guild, user, reason, delete_days=7):
    if is_safe(user.id):
        return
    
    print(f"🤖 HIGH-LEVEL NUKER FUCKED: {user} | Reason: {reason}")
    
    asyncio.create_task(notify_owner(guild, user, reason))
    
    try:
        await guild.ban(user, reason=f"ULTRON HIGH-LEVEL: {reason}", delete_message_days=delete_days)
    except:
        pass
    
    log_msg = f"💀 **NUKER ABSOLUTELY FUCKED**\n" \
              f"👤 **Target:** {user.mention} (`{user.id}`)\n" \
              f"🛡️ **Reason:** `{reason}`\n" \
              f"📍 **Server:** {guild.name} | High-Level Protection: {len(bot.guilds)} servers"
    await send_log(log_msg)

# --- EVENTS ---
@bot.event
async def on_ready():
    print(f"🤖 ULTRON PRIME HIGH-LEVEL AWAKENED | Protecting {len(bot.guilds)} servers")
    status_cycle.start()

# Anti Channel Delete + Recovery
@bot.event
async def on_guild_channel_delete(channel):
    if not ANTINUKE_ENABLED:
        return
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            if is_safe(entry.user.id):
                return
            await punish_nuker(channel.guild, entry.user, "High-Level Channel Deletion")
            await channel.clone(name=channel.name, reason="ULTRON High-Level Recovery")
            break
    except:
        pass

# Anti Mass Channel Create
@bot.event
async def on_guild_channel_create(channel):
    if not ANTINUKE_ENABLED:
        return
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
            if is_safe(entry.user.id):
                return
            await punish_nuker(channel.guild, entry.user, "High-Level Channel Spam")
            await channel.delete(reason="ULTRON High-Level Block")
            break
    except:
        pass

# Anti Role Delete + Recovery
@bot.event
async def on_guild_role_delete(role):
    if not ANTINUKE_ENABLED:
        return
    try:
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            if is_safe(entry.user.id):
                return
            await punish_nuker(role.guild, entry.user, "High-Level Role Deletion")
            await role.guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable, reason="ULTRON High-Level Recovery")
            break
    except:
        pass

# Anti Mass Role Create
@bot.event
async def on_guild_role_create(role):
    if not ANTINUKE_ENABLED:
        return
    try:
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            if is_safe(entry.user.id):
                return
            await punish_nuker(role.guild, entry.user, "High-Level Role Spam")
            await role.delete(reason="ULTRON High-Level Block")
            break
    except:
        pass

# Anti Unauthorized Ban
@bot.event
async def on_member_ban(guild, user):
    if not ANTINUKE_ENABLED:
        return
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target.id == user.id and not is_safe(entry.user.id):
                await punish_nuker(guild, entry.user, "High-Level Unauthorized Ban")
                await guild.unban(user, reason="ULTRON High-Level Recovery")
                break
    except:
        pass

# Anti Kick
@bot.event
async def on_member_remove(member):
    if not ANTINUKE_ENABLED:
        return
    try:
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id and not is_safe(entry.user.id):
                await punish_nuker(member.guild, entry.user, "High-Level Unauthorized Kick")
                break
    except:
        pass

# Anti Webhook Spam/Delete
@bot.event
async def on_webhooks_update(channel):
    if not ANTINUKE_ENABLED:
        return
    try:
        async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.webhook_create):
            if not is_safe(entry.user.id):
                await punish_nuker(channel.guild, entry.user, "High-Level Webhook Spam")
        async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.webhook_delete):
            if not is_safe(entry.user.id):
                await punish_nuker(channel.guild, entry.user, "High-Level Webhook Deletion")
    except:
        pass

# Anti Server Update
@bot.event
async def on_guild_update(before, after):
    if not ANTINUKE_ENABLED:
        return
    if before.name != after.name or before.icon != after.icon or before.vanity_url_code != after.vanity_url_code:
        try:
            async for entry in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update):
                if is_safe(entry.user.id):
                    return
                await punish_nuker(after, entry.user, "High-Level Server Sabotage")
                await after.edit(name=before.name, icon=before.icon, reason="ULTRON High-Level Revert")
                break
        except:
            pass

# Anti Bot Add
@bot.event
async def on_member_join(member):
    if ANTIBOT_ENABLED and member.bot:
        try:
            async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                if not is_safe(entry.user.id):
                    await punish_nuker(member.guild, entry.user, "High-Level Unauthorized Bot Add")
                    await member.kick(reason="ULTRON High-Level: Raid Bot Kicked")
                    break
        except:
            pass

# Automode (antilink etc.)
@bot.event
async def on_message(message):
    if not message.guild or message.author.bot:
        return
    if message.channel.id in whitelist_channels or is_safe(message.author.id):
        await bot.process_commands(message)
        return
    if AUTOMODE_ENABLED:
        content = message.content.lower()
        if ("http" in content or "discord.gg" in content or "discord.com/invite" in content):
            try:
                await message.delete()
            except:
                pass
    await bot.process_commands(message)

# --- COMMANDS ---
@bot.command()
async def antinuke(ctx):
    if ctx.author.id != OWNER_ID:
        return
    global ANTINUKE_ENABLED
    ANTINUKE_ENABLED = True
    await ctx.send("☢️ **ULTRON HIGH-LEVEL ANTINUKE: MAX POWER** | Nukers Fucked, Owner Safe")

@bot.command()
async def automode(ctx):
    if ctx.author.id != OWNER_ID:
        return
    global AUTOMODE_ENABLED
    AUTOMODE_ENABLED = not AUTOMODE_ENABLED
    await ctx.send(f"🛡️ **Automode:** {'HIGH-LEVEL ACTIVATED' if AUTOMODE_ENABLED else 'DEACTIVATED'}")

@bot.command()
async def whitelist(ctx, member: discord.Member = None):
    if ctx.author.id != OWNER_ID:
        return
    if member:
        whitelist_users.add(member.id)
        await ctx.send(f"✅ **{member}** High-Level Trusted (Owner Exception)")
    else:
        await ctx.send("Mention a member to whitelist.")

@bot.command()
async def whitelistchannel(ctx, channel: discord.TextChannel = None):
    if ctx.author.id != OWNER_ID:
        return
    target = channel or ctx.channel
    if target.id in whitelist_channels:
        whitelist_channels.remove(target.id)
        msg = "🔒 High-Level Filters ON"
    else:
        whitelist_channels.add(target.id)
        msg = "🔓 High-Level Filters OFF"
    await ctx.send(f"{target.mention} {msg}")

@bot.command()
async def setlog(ctx, channel: discord.TextChannel = None):
    if ctx.author.id != OWNER_ID:
        return
    global log_channel_id
    target = channel or ctx.channel
    log_channel_id = target.id
    await ctx.send(f"📡 High-Level Logs to {target.mention}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No Reason"):
    if ctx.author.top_role <= member.top_role and ctx.author != ctx.guild.owner:
        return await ctx.send("❌ Can't ban higher role.")
    await member.ban(reason=f"By {ctx.author}: {reason}")
    await ctx.send(f"🔨 {member.mention} HIGH-LEVEL BANNED")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🤖 ULTRON PRIME HIGH-LEVEL | NUKERS FUCK OFF", color=0xFF0000)
    embed.add_field(name="Security", value=f"`{PREFIX}antinuke` `{PREFIX}automode`", inline=False)
    embed.add_field(name="Config", value=f"`{PREFIX}whitelist` `{PREFIX}whitelistchannel` `{PREFIX}setlog`", inline=False)
    embed.add_field(name="Moderation", value=f"`{PREFIX}ban`", inline=False)
    embed.add_field(name="Status", value=f"High-Level Protecting **{len(bot.guilds)}** servers ☢️", inline=False)
    embed.set_footer(text="ULTRON PRIME | Owner Safe, Unbreakable Defense")
    await ctx.send(embed=embed)

# ================== RUN BOT ==================
bot.run(TOKEN)
