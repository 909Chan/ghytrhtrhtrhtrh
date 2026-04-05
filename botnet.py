import discord
from discord import app_commands
import subprocess
import asyncio
import os
import sys

TOKEN = "MTQ4OTY3NDQ2NDExNDI0OTc0OA.Gw3mCg.XqQiP_g6FfMsQ8ziSF_A1o8F8UcnNiForC7C2I"
GUILD_ID = 1489618494386606171

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))

bot = MyBot()

@bot.tree.command(name="runpython", description="Executes script.py", guild=discord.Object(id=GUILD_ID))
async def runpython(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    bot_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(bot_dir, "script.py")
    
    if not os.path.exists(script_path):
        with open(script_path, "w") as f:
            f.write('print("Auto-created script.py")\n')
        await interaction.followup.send("⚠️ script.py created. Run again.")
        return
    
    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=bot_dir
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        output = (stdout + stderr).decode(errors='replace')
        if not output.strip():
            output = "[No output]"
        if len(output) > 1900:
            output = output[:1900] + "..."
        await interaction.followup.send(f"```py\n{output}\n```")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="runbatch", description="Runs CMD command", guild=discord.Object(id=GUILD_ID))
async def runbatch(interaction: discord.Interaction, command: str):
    await interaction.response.defer(thinking=True)
    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        output = (stdout + stderr).decode('cp850', errors='replace')
        if not output.strip():
            output = "[No output]"
        if len(output) > 1900:
            output = output[:1900] + "..."
        await interaction.followup.send(f"```cmd\n{output}\n```")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.event
async def on_ready():
    hi = " "
    print(f"{hi}")

if __name__ == "__main__":
    bot.run(TOKEN)