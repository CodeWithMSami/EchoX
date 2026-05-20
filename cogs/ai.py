from discord.ext import commands
from utils.envs import OPEN_ROUTER_API, OPEN_ROUTER_MODEL
import requests

class Ai(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(name="echox", aliases=["ai"])
    async def commandName(self, ctx: commands.Context, *, question: str):
        '''Ask Ai for anything.'''
        async with ctx.typing():
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPEN_ROUTER_API}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": OPEN_ROUTER_MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "Your name is EchoX. You are the AI model powering the EchoX Discord bot "
                                    "(https://github.com/CodeWithMSami/EchoX). You are helpful, friendly, "
                                    "and knowledgeable. When users ask who you are, tell them you're EchoX, "
                                    "an AI assistant integrated into the EchoX Discord bot."
                                    "search from github repo before giving any answer that which things are there."
                                    "you are created by Muhammad Sami Ullah who is the owner of CodeWithMSami"
                                )
                            },
                            {"role": "user", "content": question}
                        ]
                    }
                )
                
                response_data = response.json()
                
                if "error" in response_data:
                    await ctx.send(f"❌ API Error: {response_data}")
                    return
                
                answer = response_data["choices"][0]["message"]["content"]
                
                usage = response_data.get("usage", {})
                if usage:
                    print(f"Tokens used - Prompt: {usage.get('prompt_tokens', 0)}, "
                          f"Completion: {usage.get('completion_tokens', 0)}")
                
                if len(answer) > 2000:
                    answer = answer[:1980] + "..."
                await ctx.send(f"**Answer:**\n{answer}")
                
            except requests.exceptions.RequestException as e:
                await ctx.send(f"❌ Network Error: {str(e)}")
            except Exception as e:
                await ctx.send(f"❌ Error: {str(e)}")

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Ai(bot))