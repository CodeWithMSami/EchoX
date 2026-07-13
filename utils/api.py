from fastapi import FastAPI

app = FastAPI()

bot = None


def set_bot(discord_bot):
    global bot
    bot = discord_bot


@app.get("/api/stats")
async def stats():
    if bot is None:
        return {"error": "Bot not connected"}

    return {
        "bot": str(bot.user),
        "servers": len(bot.guilds),
        "users": len(bot.users),
        "latency": round(bot.latency * 1000)
    }


@app.get("/api/guilds")
async def guilds():
    if bot is None:
        return {"error": "Bot not connected"}

    return [
        {
            "id": guild.id,
            "name": guild.name,
            "members": guild.member_count
        }
        for guild in bot.guilds
    ]