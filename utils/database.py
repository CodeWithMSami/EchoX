import sqlite3
import discord
from discord.ext import commands

connection = sqlite3.connect("bot.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS utility(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property TEXT NOT NULL,
        value TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

def get_command_prefix(*args):
    '''When called it returns the command prefix.'''
    cursor.execute("SELECT * FROM utility WHERE property = ?", ("prefix",))
    prefix = cursor.fetchone()
    
    if prefix is None or len(prefix) < 0:
        cursor.execute("INSERT INTO utility(property, value) VALUES (?, ?)", ("prefix", "!"))
        connection.commit()
        return "!"
    
    return str(prefix["value"])