# EchoX 🤖

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.0%2B-blue.svg)](https://github.com/Rapptz/discord.py)

**EchoX** is a versatile Discord Bot built with `discord.py`. It aims to provide essential moderation tools, AI-powered interactions, and an intuitive help system to enhance your server experience.

---

## ✨ Features

- **🤖 AI Integration** – Engage with AI-powered chat features.
- **🛡️ Moderation Commands** – Keep your server safe with kick, ban, mute, clear, lockdown, and slowmode commands.
- **❓ Dynamic Help Cog** – Easily discover all commands with an organized help menu.
- **⚙️ Modular Cog Structure** – Clean and scalable code with separate cogs for different functionalities.
- **📁 Utility Tools** – Extra utility commands for everyday server management.

---

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8 or higher** installed on your system.
- A **Discord Bot Token**. Get one from the [Discord Developer Portal](https://discord.com/developers/applications).
- Your bot invited to a server with the necessary permissions:
  - `Send Messages`
  - `Manage Messages`
  - `Kick Members`
  - `Ban Members`
  - `Use Slash Commands`

---

## 🚀 Installation & Setup

Follow these steps to get EchoX running:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/CodeWithMSami/EchoX.git
cd EchoX
```

### 2️⃣ Create a Virtual Environment (Recommended)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory and add:

```env
DISCOR_BOT_TOKEN=your-discord-bot-token
OPEN_ROUTER_API=your-open-router-api-key
OPEN_ROUTER_MODEL=your-open-router-model
```

### 5️⃣ Run the Bot

```bash
python app.py
```

---

## 📁 Project Structure

```text
EchoX/
├── app.py                 # Main bot entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .gitignore
├── README.md
├── cogs/                  # Modular command categories
│   ├── help.py
│   ├── moderation.py
│   ├── ai.py
└── utils/                 # Helper functions and utilities
    ├── database.py
    ├── embeds.py
    └── envs.py
```

---

## 🛠️ Example Commands

| Command | Description |
|--------|-------------|
| `!help` | Displays all available commands |
| `!kick` | Kicks a member from the server |
| `!ban` | Bans a member |
| `!mute` | Mutes a member |
| `!clear` | Clears messages in a channel |
| `!ai` | Chat with the AI system |

---

## 🤝 Contributing

Contributions are welcome!

Feel free to:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is currently not under a specific open-source license.

All rights are reserved by the author [**CodeWithMSami**](https://codewithmsami.netlify.app/).

---

## 🙏 Acknowledgements

- – The powerful API wrapper for Discord.
- All contributors and users of EchoX.

---

## 🌟 Support

If you like this project, consider giving it a ⭐ on GitHub!

Made with ❤️ by [**CodeWithMSami**](https://codewithmsami.netlify.app/)