import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=5))  # UTC+5 Almaty

# ─── CONFIG ───────────────────────────────────────────────────────────────────
GUILD_ID       = 1362847208977862726
SOURCE_CHANNEL = 1449039384690032753
LOG_CHANNEL    = 1512895444097695914
BOT_TOKEN      = "your-token-here"
# ──────────────────────────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.members         = True
intents.presences       = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
online_sessions: dict[int, dict] = {}

def status_label(s: discord.Status) -> str:
    return {
        discord.Status.online:    "online 🟢",
        discord.Status.idle:      "idle 🌙",
        discord.Status.dnd:       "do not disturb 🔴",
        discord.Status.offline:   "offline",
        discord.Status.invisible: "invisible",
    }.get(s, str(s))

def fmt_duration(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s   = divmod(rem, 60)
    parts  = []
    if h: parts.append(f"{h} hour{'s' if h != 1 else ''}")
    if m: parts.append(f"{m} minute{'s' if m != 1 else ''}")
    parts.append(f"{s} second{'s' if s != 1 else ''}")
    return " ".join(parts)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return print("ERROR: guild not found")
    for member in guild.members:
        if member.bot:
            continue
        if member.status not in (discord.Status.offline, discord.Status.invisible):
            online_sessions[member.id] = {"since": datetime.now(TZ), "message_id": None}
    print(f"Tracking {len(online_sessions)} members online.")

@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    if after.bot or after.guild.id != GUILD_ID:
        return

    log_chan   = bot.get_channel(LOG_CHANNEL)
    was_online = before.status not in (discord.Status.offline, discord.Status.invisible)
    is_online  = after.status  not in (discord.Status.offline, discord.Status.invisible)

    if not was_online and is_online:
        msg = await log_chan.send(f"user **{after.name}** is online")
        online_sessions[after.id] = {"since": datetime.now(TZ), "message_id": msg.id}

    elif was_online and not is_online:
        session = online_sessions.pop(after.id, None)
        if not session:
            return
        now   = datetime.now(TZ)
        since = session["since"]
        if session["message_id"]:
            try:
                await (await log_chan.fetch_message(session["message_id"])).delete()
            except discord.NotFound:
                pass
        await log_chan.send(
            f"user **{after.name}** was online "
            f"`{since.strftime('%H:%M:%S')}` — `{now.strftime('%H:%M:%S')}` "
            f"({fmt_duration((now - since).total_seconds())})"
        )

bot.run(BOT_TOKEN)
