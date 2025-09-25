# 🚀 DISCORD-XP-BOT
*Ignite Engagement, Reward Activity, Elevate Your Community!*

🔹 ![Last Commit](https://img.shields.io/github/last-commit/kirilt2/Discord-XP-Bot?color=blue&style=for-the-badge)  
🔹 ![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python&logoColor=white)  
🔹 ![Discord.py](https://img.shields.io/badge/discord.py-7289DA?style=for-the-badge&logo=discord&logoColor=white)  
🔹 ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)  
🔹 ![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)  

---

## 📌 Overview
Discord XP Bot is a lightweight and customizable bot designed to reward activity and engagement in your Discord server.  
Admins can grant XP, the bot stores data in SQLite, and users can view levels and leaderboards.  

---

## ✨ Features
- 🎯 Grant XP manually to users (admin only)  
- 📊 Tracks XP and calculates levels automatically  
- 📝 Logs XP events in a dedicated channel  
- 🔒 Role-based permissions (only admins can grant XP)  
- ⚡ No external hosting needed – runs on Python with SQLite  

---

## 📂 Project Structure
- **Main.py** – Entry point  
- **Leadbord.py** – XP and leaderboard logic  
- **config.json** – Bot token and settings  
- **xp_database.db** – SQLite database  
- **README.md** – Documentation  
- **__pycache__/** – Auto-generated cache  

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/kirilt2/Discord-XP-Bot.git
cd Discord-XP-Bot
```

2️⃣ Install Dependencies
```bash 
pip install -r requirements.txt
```
```bash 
3️⃣ Configure config.json

{
  "token": "YOUR_DISCORD_BOT_TOKEN",
  "admin_role_ids": ["ROLE_ID"],
  "log_channel_id": "CHANNEL_ID"
}
```

```
▶️ Usage

python Main.py
````


## 📊 Example Commands

- /grant_xp @user 50 – Grants 50 XP to a user (Admin only)

- /leaderboard – Shows the top XP users (Everyone)

- /level @user – Shows the level and XP of a user (Everyone)


## 📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it with credit.

