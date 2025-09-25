import discord
from discord import app_commands
from datetime import datetime
import sqlite3
import json
import time
import logging

with open('config.json') as config_file:
    config = json.load(config_file)

db = sqlite3.connect('xp_database.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Xpusers (
        user_id INTEGER PRIMARY KEY,
        xp INTEGER DEFAULT 0,
        message_count INTEGER DEFAULT 0
    )
''')
db.commit()

xp_threshold = config['XP_THRESHOLD']
xp_per_message = config['XP_PER_MESSAGE']
admin_role_ids = config['ADMIN_ROLE_IDS']
level_up_channel_id = config['LEVEL_UP_CHANNEL_ID']
log_channel_id = config['LOG_CHANNEL_ID']
xp_cooldown = config['XP_COOLDOWN']
last_xp_time = {}


def setup(bot):
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        cursor.execute('INSERT OR IGNORE INTO Xpusers (user_id) VALUES (?)', (message.author.id,))
        db.commit()

        cursor.execute('UPDATE Xpusers SET message_count = message_count + 1 WHERE user_id = ?', (message.author.id,))
        db.commit()

        if message.author.id in last_xp_time and time.time() - last_xp_time[message.author.id] < xp_cooldown:
            return

        last_xp_time[message.author.id] = time.time()

        cursor.execute('SELECT xp FROM Xpusers WHERE user_id = ?', (message.author.id,))
        current_xp = cursor.fetchone()[0]
        new_xp = current_xp + xp_per_message
        new_level = new_xp // xp_threshold
        old_level = current_xp // xp_threshold

        if new_level > old_level:
            level_up_channel = message.guild.get_channel(level_up_channel_id)
            if level_up_channel:
                await level_up_channel.send(
                    f"🎉 **Level Up!** Congratulations {message.author.mention}! You've reached **Level {new_level}**! 🚀"
                )

        cursor.execute('UPDATE Xpusers SET xp = ? WHERE user_id = ?', (new_xp, message.author.id))
        db.commit()
        await bot.process_commands(message)

    @bot.tree.command(name="grant_xp", description="Grant XP to a user (Admin Only).")
    async def grant_xp(interaction: discord.Interaction, member: discord.Member, xp_amount: int):
        current_time = datetime.now().strftime('%m/%d/%Y %I:%M %p')
        admin_role = interaction.guild.get_role(admin_role_ids[0])
        if admin_role not in interaction.user.roles:
            embed = discord.Embed(
                title="⛔ Permission Denied",
                description="You don't have permission to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        cursor.execute('INSERT OR IGNORE INTO Xpusers (user_id) VALUES (?)', (member.id,))
        db.commit()

        cursor.execute('SELECT xp FROM Xpusers WHERE user_id = ?', (member.id,))
        current_xp = cursor.fetchone()[0]
        new_xp = current_xp + xp_amount
        new_level = new_xp // xp_threshold

        cursor.execute('UPDATE Xpusers SET xp = ? WHERE user_id = ?', (new_xp, member.id))
        db.commit()

        log_channel = interaction.guild.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="✅ XP Granted Log",
                description=f"{xp_amount} XP granted to **{member.display_name}** by **{interaction.user.display_name}**.",
                color=discord.Color.green()
            )
            await log_channel.send(embed=embed)

        embed = discord.Embed(
            title="✅ XP Granted",
            description=f"{xp_amount} XP has been added to {member.mention}.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Command issued by {interaction.user.name} on {current_time}")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="remove_xp", description="Remove XP from a user (Admin Only).")
    async def remove_xp(interaction: discord.Interaction, member: discord.Member, xp_amount: int):
        current_time = datetime.now().strftime('%m/%d/%Y %I:%M %p')
        admin_role = interaction.guild.get_role(admin_role_ids[0])
        if admin_role not in interaction.user.roles:
            embed = discord.Embed(
                title="⛔ Permission Denied",
                description="You don't have permission to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        cursor.execute('INSERT OR IGNORE INTO Xpusers (user_id) VALUES (?)', (member.id,))
        db.commit()

        cursor.execute('SELECT xp FROM Xpusers WHERE user_id = ?', (member.id,))
        current_xp = cursor.fetchone()[0]
        new_xp = max(0, current_xp - xp_amount)
        new_level = new_xp // xp_threshold

        cursor.execute('UPDATE Xpusers SET xp = ? WHERE user_id = ?', (new_xp, member.id))
        db.commit()

        log_channel = interaction.guild.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="❌ XP Removal Log",
                description=f"{xp_amount} XP removed from **{member.display_name}** by **{interaction.user.display_name}**.",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)

        embed = discord.Embed(
            title="❌ XP Removed",
            description=f"{xp_amount} XP has been removed from {member.mention}.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Command issued by {interaction.user.name} on {current_time}")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="profilexp", description="Check your XP or another user's.")
    async def check_rank(interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        current_time = datetime.now().strftime('%m/%d/%Y %I:%M %p')

        cursor.execute('INSERT OR IGNORE INTO Xpusers (user_id) VALUES (?)', (member.id,))
        db.commit()

        cursor.execute('SELECT xp, message_count FROM Xpusers WHERE user_id = ?', (member.id,))
        xp, message_count = cursor.fetchone()

        level = xp // xp_threshold

        embed = discord.Embed(
            title="📊 XP Profile",
            description=f"**{member.display_name}** - Level: {level}, XP: {xp}, Messages: {message_count}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Requested on {current_time}")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="leaderboard", description="View the top XP earners.")
    async def leaderboard(interaction: discord.Interaction, top_n: int = 10):
        current_time = datetime.now().strftime('%m/%d/%Y %I:%M %p')

        cursor.execute('SELECT user_id, xp, message_count FROM Xpusers ORDER BY xp DESC LIMIT ?', (top_n,))
        results = cursor.fetchall()

        embed = discord.Embed(
            title="🏆 XP Leaderboard",
            description=f"Top {top_n} XP Earners:",
            color=discord.Color.gold()
        )

        for idx, (user_id, xp, message_count) in enumerate(results, 1):
            user = interaction.guild.get_member(user_id)
            if user:
                level = xp // xp_threshold
                embed.add_field(
                    name=f"{idx}. {user.display_name}",
                    value=f"Level: {level}, XP: {xp}, Messages: {message_count}",
                    inline=False
                )

        embed.set_footer(text=f"Requested on {current_time}")
        await interaction.response.send_message(embed=embed)
