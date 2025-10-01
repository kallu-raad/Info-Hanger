import telebot
import requests
import json
import time
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Bot Configuration
BOT_TOKEN = "7598822927:AAE02xG2cdcpWEZOpFIlo6XiwKnCuf6Bk5U"
bot = telebot.TeleBot(BOT_TOKEN)

# Admin and Moderator IDs
ADMIN_ID = 6403299013
MODERATOR_ID = 7043969661

# Database simulation (in production, use SQLite or PostgreSQL)
users_db = {}
admins_db = {ADMIN_ID: {"username": "CEO_KCL_BD"}}
moderators_db = {MODERATOR_ID: {"username": "raad0909"}}

# Coin offers
COIN_OFFERS = [
    {"coins": 50, "price": 45},
    {"coins": 100, "price": 80},
    {"coins": 150, "price": 100},
    {"coins": 250, "price": 150},
    {"coins": 500, "price": 250}
]

# User stats
user_stats = {
    "total_users": 0,
    "active_users": 0,
    "referred_users": 0,
    "total_info_requests": 0,
    "total_bkash_requests": 0,
    "total_ff_requests": 0
}

# Helper functions
def create_keyboard():
    """Create main keyboard with all buttons (2 per row)"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🔍 BKASH Info"),
        KeyboardButton("🎮 FF Player Info")
    )
    markup.add(
        KeyboardButton("💰 Buy Coins"),
        KeyboardButton("👤 Profile")
    )
    markup.add(
        KeyboardButton("👥 Referral"),
        KeyboardButton("🎁 Bonus")
    )
    markup.add(
        KeyboardButton("❓ Help"),
        KeyboardButton("📞 Contact")
    )
    return markup

def create_admin_keyboard():
    """Create admin panel keyboard with 2 buttons per row"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📊 Stats"),
        KeyboardButton("👥 Users")
    )
    markup.add(
        KeyboardButton("👁️ See User"),
        KeyboardButton("🚫 Ban User")
    )
    markup.add(
        KeyboardButton("✅ Unban User"),
        KeyboardButton("💰 Give Coins")
    )
    markup.add(
        KeyboardButton("📢 Broadcast"),
        KeyboardButton("📤 Send Message")
    )
    markup.add(
        KeyboardButton("🔙 Back")
    )
    return markup

def create_moderator_keyboard():
    """Create moderator panel keyboard with 2 buttons per row"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📊 Stats"),
        KeyboardButton("🔍 User Monitoring")
    )
    markup.add(
        KeyboardButton("🔙 Back")
    )
    return markup

def format_bkash_info(data):
    """Format BKASH info into a beautifully designed message"""
    if not data or "error" in data:
        return "❌ No information found for this BKASH number."

    name = data.get("name", "N/A")
    operator = data.get("operator", "N/A")
    account_type = data.get("account_type", "N/A")
    status = data.get("status", "N/A")

    message = f"""
✨✨✨ BKASH INFORMATION REPORT ✨✨✨

📱 NUMBER: {data.get('number', 'N/A')}
👤 NAME: {name}
📡 OPERATOR: {operator}
💳 ACCOUNT TYPE: {account_type}
✅ STATUS: {status}

📅 REPORT GENERATED: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}

🧾 DETAILED INFORMATION:
🔸 Account Holder: {name}
🔸 Service Provider: {operator}
🔸 Account Type: {account_type}
🔸 Verification Status: {status}
"""
    return message

def format_ff_info(data):
    """Format Free Fire info into a beautifully designed message"""
    if not data or "error" in data:
        return "❌ No information found for this player."

    # Basic Info
    basic_info = data.get("basicinfo", [{}])[0]
    clan_info = data.get("claninfo", [{}])[0]
    clan_admin = data.get("clanadmin", [{}])[0]

    # Extract fields
    username = basic_info.get("username", "N/A")
    level = basic_info.get("level", "N/A")
    region = basic_info.get("region", "N/A")
    exp = basic_info.get("Exp", "N/A")
    bio = basic_info.get("bio", "N/A")
    likes = basic_info.get("likes", "N/A")
    last_login = basic_info.get("lastlogin", "N/A")
    create_at = basic_info.get("createat", "N/A")
    server_used = data.get("server_used", "N/A")

    # Clan Info
    clan_name = clan_info.get("clanname", "N/A")
    clan_id = clan_info.get("clanid", "N/A")
    guild_level = clan_info.get("guildlevel", "N/A")
    live_member = clan_info.get("livemember", "N/A")

    # Clan Admin
    admin_name = clan_admin.get("adminname", "N/A")
    admin_level = clan_admin.get("level", "N/A")

    # Format dates
    try:
        login_date = datetime.fromtimestamp(int(last_login)).strftime('%Y-%m-%d %I:%M:%S %p') if last_login != "N/A" else "N/A"
        create_date = datetime.fromtimestamp(int(create_at)).strftime('%Y-%m-%d %I:%M:%S %p') if create_at != "N/A" else "N/A"
    except:
        login_date = "N/A"
        create_date = "N/A"

    message = f"""
🎮 FREE FIRE PLAYER REPORT 🎮

╔═════ 👤 BASIC INFO ═════╗

👤 PLAYERNAME: {username}

🏅 LEVEL: {level}

🌍 REGION: {region}

📈 EXPERIENCE: {exp}

❤️ LIKES: {likes}

🗓️ CREATED AT: {create_date}

⏰ LAST LOGIN: {login_date}


📝 BIO: {bio}

****⚔️ CLAN INFORMATION****

🏢 CLAN NAME: {clan_name}
🆔 CLAN ID: {clan_id}
🏆 GUILD LEVEL: {guild_level}
👥 LIVE MEMBERS: {live_member}

*****👑 CLAN ADMIN:*****

👤 ADMIN NAME: {admin_name}
🏅 ADMIN LEVEL: {admin_level}

📅 REPORT GENERATED: {datetime.now().strftime('%I:%M:%S | %d-%m-%Y')}

 ╚═════ 🔧 TECHNICAL ═════╝

🌐 SERVER USED: {server_used} 🖥️

Coins used: 1 💎 |
Epic stats! Share with friends. 🎉
(Requested on: [Date] | [Time] BDT)

"""
    return message

def get_user_info(user_id):
    """Get user info from database"""
    return users_db.get(user_id, {})

def update_user_info(user_id, info):
    """Update user info in database"""
    if user_id not in users_db:
        users_db[user_id] = {
            "first_name": "",
            "username": "",
            "coins": 0,
            "total_info_requests": 0,
            "total_bkash_requests": 0,
            "total_ff_requests": 0,
            "referred_by": None,
            "referrals": [],
            "bonus_time": None,
            "is_banned": False,
            "join_date": datetime.now()
        }

    # Merge new info with existing
    current = users_db[user_id]
    for key, value in info.items():
        if key == "coins":
            current[key] = current.get(key, 0) + value
        elif key == "referrals":
            current[key] = current.get(key, []) + value
        else:
            current[key] = value

    users_db[user_id] = current

def send_to_moderator(message):
    """Send message to moderator"""
    try:
        bot.send_message(MODERATOR_ID, message)
    except Exception as e:
        print(f"Error sending to moderator: {e}")

# Bot Commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "No Username"

    # Check if user is admin or moderator
    if user_id == ADMIN_ID:
        # Admin welcome
        welcome_msg = f"""
🎉🎉🎉 WELCOME ADMIN! 🎉🎉🎉
👋 {first_name}!
🤖 You are now logged in as Administrator.
🔐 Admin Panel Access Granted.

📊 YOUR ROLE: Admin
🔗 USERNAME: @{username}
🆔 USER ID: `{user_id}`
🔐 ACCESS: Full Control
✅ STATUS: Active

*****📘 ADMIN PANEL FEATURES:*****

📊 View Statistics
👥 Manage Users
🚫 Ban Users
✅ Unban Users
💰 Give Coins
📢 Broadcast Messages
📤 Send Direct Messages

⚡ TIP: Use the buttons below to access admin features!
"""
        bot.send_message(user_id, welcome_msg)
        bot.send_message(user_id, "📋 Select an option:", reply_markup=create_admin_keyboard())
        return

    elif user_id == MODERATOR_ID:
        # Moderator welcome
        welcome_msg = f"""
🛡️🛡️🛡️ WELCOME MODERATOR! 🛡️🛡️🛡️
👋 {first_name}!
🔧 You are now logged in as Moderator.
👁️ Monitoring Access Granted.

🛡️ YOUR ROLE: Moderator
🔗 USERNAME: @{username}
🆔 USER ID: `{user_id}`
👁️ ACCESS: Live Monitoring
✅ STATUS: Active

📘 MODERATOR FEATURES:
📊 View Statistics
🔍 Monitor User Activities

⚡ TIP: Use the buttons below to monitor users!
"""
        bot.send_message(user_id, welcome_msg)
        bot.send_message(user_id, "📋 Select an option:", reply_markup=create_moderator_keyboard())
        return

    # Check if user is banned
    user_data = get_user_info(user_id)
    if user_data.get('is_banned', False):
        ban_msg = f"""
🚫🚫 ACCOUNT BANNED 🚫🚫

Dear {first_name},

Your account has been banned by the administrator.

Reason: Unauthorized activity or violation of terms.

To resolve this issue, please contact the administrator:
📲 @CEO_KCL_BD

You cannot use any features of this bot until unbanned.
"""
        bot.send_message(user_id, ban_msg)
        return

    # Regular user welcome
    welcome_msg = f"""
🎮 INFO HANGER 🔍
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ _ _ _ _ _ _ _
✨ Welcome, {first_name}! ✨
🎯 Your Ultimate Free Fire & BKASH Information Finder!

📌 FEATURES:
🔹 Free Fire Player Info 🎮
🔹 BKASH Number Lookup 🔍
🔹 Coin System 💰
🔹 Referral Program 👥
🔹 Daily Bonuses 🎁
🔹 Premium Support  📞
---------------------------------------------------------------------

💰 YOUR BALANCE: {get_user_info(user_id).get('coins', 0)} Coins
👥 REFERRALS: {len(get_user_info(user_id).get('referrals', []))} Users
📊 TOTAL REQUESTS: {get_user_info(user_id).get('total_info_requests', 0)}
---------------------------------------------------------------------
📘 USE THE BUTTONS BELOW TO START EXPLORING!

=>Powered by @CEO_KCL_BD | Let's hang out with info! 🔥
"""

    bot.send_message(user_id, welcome_msg, reply_markup=create_keyboard())

    # Check if user was referred
    if message.text.startswith('/start'):
        ref_code = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
        if ref_code and ref_code.isdigit() and int(ref_code) != user_id:
            referrer_id = int(ref_code)
            if referrer_id in users_db:
                update_user_info(referrer_id, {"referrals": [user_id]})
                update_user_info(user_id, {"referred_by": referrer_id})
                bot.send_message(referrer_id, f"🎉 New referral! User @{message.from_user.username} joined using your link!")

    # Update stats - Only increment if new user
    if user_id not in users_db:
        user_stats["total_users"] += 1
        user_stats["active_users"] += 1
    update_user_info(user_id, {"first_name": first_name, "username": username})

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
📖📖📖 HOW TO USE THIS BOT 📖📖📖

🔍 BKASH INFO:
1. Press "🔍 BKASH Info" button
2. Enter a valid 11-digit Bangladeshi number (e.g., 01712345678)
3. Get detailed information about the number

🎮 FREE FIRE PLAYER INFO:
1. Press "🎮 FF Player Info" button
2. Enter a valid player UID (unique identifier)
3. Get comprehensive player profile information

💰 COIN SYSTEM:
- 1 Coin = 1 FF Info Request
- 2 Coins = 1 BKASH Info Request
- Buy more coins via "💰 Buy Coins"

👥 REFERRAL PROGRAM:
- Earn 10 Coins for every referral
- Share your unique referral link to earn more!

🎁 BONUS:
- Claim 5 free coins daily
- Must wait 24 hours between claims

📞 CONTACT SUPPORT:
For issues or suggestions, contact: @CEO_KCL_BD

📌 NOTE: All information is provided for educational purposes only.
"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    stats_msg = f"""
📊📊📊 BOT STATISTICS 📊📊📊

👥 TOTAL USERS: {user_stats['total_users']}
🟢 ACTIVE USERS: {user_stats['active_users']}
🔗 REFERRED USERS: {user_stats['referred_users']}
📊 TOTAL INFO REQUESTS: {user_stats['total_info_requests']}
🔍 BKASH REQUESTS: {user_stats['total_bkash_requests']}
🎮 FF REQUESTS: {user_stats['total_ff_requests']}

📅 GENERATED AT: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}
"""
    bot.send_message(message.chat.id, stats_msg)

@bot.message_handler(func=lambda message: message.text == "🔍 BKASH Info")
def ask_bkash_number(message):
    if message.from_user.id in admins_db or message.from_user.id in moderators_db:
        bot.reply_to(message, "⚠️ Admin/Moderator cannot use this feature")
        return

    # Check if user is banned
    user_data = get_user_info(message.from_user.id)
    if user_data.get('is_banned', False):
        bot.reply_to(message, "🚫 Your account has been banned. You cannot use this feature.")
        return

    msg = bot.reply_to(message, "📱 Please enter a 11-digit Bangladeshi BKASH number (e.g., 01712345678):")
    bot.register_next_step_handler(msg, process_bkash_request)

def process_bkash_request(message):
    user_id = message.from_user.id
    number = message.text.strip()

    # Validate number
    if not number.isdigit() or len(number) != 11 or not number.startswith('01'):
        bot.reply_to(message, "❌ Invalid number format. Please enter a valid 11-digit Bangladeshi number starting with 01.")
        return

    # Deduct coins
    user_data = get_user_info(user_id)
    if user_data.get('coins', 0) < 2:
        bot.reply_to(message, "❌ Not enough coins! BKASH info costs 2 coins.")
        return

    # Deduct coins
    update_user_info(user_id, {"coins": -2, "total_info_requests": 1, "total_bkash_requests": 1})
    user_stats["total_bkash_requests"] += 1

    # Send processing status
    processing_msg = "🔄 Processing your request... Please wait while we fetch the information."
    bot.reply_to(message, processing_msg)

    # Fetch data from API
    try:
        api_url = f"https://api.myani.top/bkash.php?number={number}"
        response = requests.get(api_url, timeout=10)
        data = response.json()

        # Send to moderator
        mod_msg = f"""
🔔 NEW BKASH REQUEST 🔔

👤 USER: {message.from_user.first_name}
🔗 USERNAME: @{message.from_user.username}
🆔 ID: {user_id}
📱 NUMBER: {number}
💰 COINS DEDUCTED: 2
🕒 TIME: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}
"""
        send_to_moderator(mod_msg)

        # Format and send response
        formatted_response = format_bkash_info(data)
        bot.reply_to(message, formatted_response)

    except Exception as e:
        error_msg = "❌ Error fetching BKASH information. Please try again later."
        bot.reply_to(message, error_msg)
        print(f"Error: {e}")

@bot.message_handler(func=lambda message: message.text == "🎮 FF Player Info")
def ask_ff_uid(message):
    if message.from_user.id in admins_db or message.from_user.id in moderators_db:
        bot.reply_to(message, "⚠️ Admin/Moderator cannot use this feature")
        return

    # Check if user is banned
    user_data = get_user_info(message.from_user.id)
    if user_data.get('is_banned', False):
        bot.reply_to(message, "🚫 Your account has been banned. You cannot use this feature.")
        return

    msg = bot.reply_to(message, "🎮 Please enter a Free Fire player UID:")
    bot.register_next_step_handler(msg, process_ff_request)

def process_ff_request(message):
    user_id = message.from_user.id
    uid = message.text.strip()

    # Validate UID
    if not uid.isdigit():
        bot.reply_to(message, "❌ Invalid UID format. Please enter a valid numeric UID.")
        return

    # Deduct coins
    user_data = get_user_info(user_id)
    if user_data.get('coins', 0) < 1:
        bot.reply_to(message, "❌ Not enough coins! FF info costs 1 coin.")
        return

    # Deduct coins
    update_user_info(user_id, {"coins": -1, "total_info_requests": 1, "total_ff_requests": 1})
    user_stats["total_ff_requests"] += 1

    # Send processing status
    processing_msg = "🔄 Processing your request... Please wait while we fetch the information."
    bot.reply_to(message, processing_msg)

    # Fetch data from API
    try:
        api_url = f"https://momin-bot-info.vercel.app/{uid}"
        response = requests.get(api_url, timeout=10)
        data = response.json()

        # Send to moderator
        mod_msg = f"""
🔔 NEW FF PLAYER REQUEST 🔔

👤 USER: {message.from_user.first_name}
🔗 USERNAME: @{message.from_user.username}
🆔 ID: {user_id}
🎮 UID: {uid}
💰 COINS DEDUCTED: 1
🕒 TIME: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}
"""
        send_to_moderator(mod_msg)

        # Format and send response
        formatted_response = format_ff_info(data)
        bot.reply_to(message, formatted_response)

    except Exception as e:
        error_msg = "❌ Error fetching Free Fire information. Please try again later."
        bot.reply_to(message, error_msg)
        print(f"Error: {e}")

@bot.message_handler(func=lambda message: message.text == "💰 Buy Coins")
def show_coin_offers(message):
    if message.from_user.id in admins_db or message.from_user.id in moderators_db:
        bot.reply_to(message, "⚠️ Admin/Moderator cannot use this feature")
        return

    # Check if user is banned
    user_data = get_user_info(message.from_user.id)
    if user_data.get('is_banned', False):
        bot.reply_to(message, "🚫 Your account has been banned. You cannot use this feature.")
        return

    offers_msg = """
💸💸💸 COIN OFFERS 💸💸💸

🎁 SPECIAL DEALS:
🔹 50 Coins - 45 Taka
🔹 100 Coins - 80 Taka
🔹 150 Coins - 100 Taka
🔹 250 Coins - 150 Taka
🔹 500 Coins - 250 Taka

📩 HOW TO BUY:
To purchase coins, contact our developer:
📲 @CEO_KCL_BD

💰 PAYMENT METHODS:
• BKASH
• Nagad
• Bank Transfer
• Cash on Delivery

🕒 NOTE: All transactions are processed manually.
"""

    bot.send_message(message.chat.id, offers_msg)

@bot.message_handler(func=lambda message: message.text == "👤 Profile")
def show_profile(message):
    # Check if user is banned
    user_data = get_user_info(message.from_user.id)
    if user_data.get('is_banned', False):
        bot.reply_to(message, "🚫 Your account has been banned. You cannot access this feature.")
        return

    user_id = message.from_user.id
    user_data = get_user_info(user_id)

    # Determine if user is banned
    status = "🚫 BANNED" if user_data.get('is_banned', False) else "✅ ACTIVE"

    profile_msg = f"""
  ***👤👤 USER PROFILE 👤👤***
|=================================|
👤 NAME: {message.from_user.first_name}
🔗 USERNAME: @{message.from_user.username}
🆔 USER ID: `{user_id}`
💰 AVAILABLE COINS: {user_data.get('coins', 0)}
📊 TOTAL INFO REQUESTS: {user_data.get('total_info_requests', 0)}
🔍 BKASH REQUESTS: {user_data.get('total_bkash_requests', 0)}
🎮 FF REQUESTS: {user_data.get('total_ff_requests', 0)}
👥 REFERRED USERS: {len(user_data.get('referrals', []))}
📅 JOIN DATE: {user_data.get('join_date', 'Unknown').strftime('%Y-%m-%d %I:%M:%S %p')}
🚫 STATUS: {status}

📊 STATISTICS:
🔸 Total Info Requests: {user_data.get('total_info_requests', 0)}
🔸 BKASH Requests: {user_data.get('total_bkash_requests', 0)}
🔸 FF Requests: {user_data.get('total_ff_requests', 0)}
🔸 Total Referrals: {len(user_data.get('referrals', []))}
"""

    bot.send_message(message.chat.id, profile_msg)

@bot.message_handler(func=lambda message: message.text == "👥 Referral")
def show_referral(message):
    # Check if user is banned
    user_data = get_user_info(message.from_user.id)
    if user_data.get('is_banned', False):
        bot.reply_to(message, "🚫 Your account has been banned. You cannot use this feature.")
        return

    user_id = message.from_user.id
    user_data = get_user_info(user_id)

    referral_msg = f"""
🔗🔗🔗 REFERRAL PROGRAM 🔗🔗🔗

🎯 YOUR REFERRAL LINK:
https://t.me/INFO_HANGER_BOT?start={user_id}

💰 EARN 10 COINS FOR EACH REFERRAL!
👥 TOTAL REFERRALS: {len(user_data.get('referrals', []))}

📊 YOUR REFERRAL HISTORY:
"""

    if user_data.get('referrals'):
        for i, ref_id in enumerate(user_data['referrals'], 1):
            ref_data = get_user_info(ref_id)
            referral_msg += f"{i}. {ref_data.get('first_name', 'Unknown')} (@{ref_data.get('username', 'No Username')})\n"
    else:
        referral_msg += "No referrals yet. Start sharing your link!"

    bot.send_message(message.chat.id, referral_msg)

@bot.message_handler(func=lambda message: message.text == "🎁 Bonus")
def claim_bonus(message):
    # Check if user is banned
    user_data = get_user_info(message.from_user.id)
    if user_data.get('is_banned', False):
        bot.reply_to(message, "🚫 Your account has been banned. You cannot use this feature.")
        return

    user_id = message.from_user.id
    user_data = get_user_info(user_id)

    # Check if user already claimed today
    last_bonus = user_data.get('bonus_time')
    if last_bonus:
        last_bonus_time = datetime.strptime(last_bonus, '%Y-%m-%d %I:%M:%S %p')
        if datetime.now() - last_bonus_time < timedelta(hours=24):
            remaining = timedelta(hours=24) - (datetime.now() - last_bonus_time)
            bot.reply_to(message, f"⏳ You already claimed your bonus today. Wait {remaining}")
            return

    # Give bonus
    update_user_info(user_id, {"coins": 5, "bonus_time": datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')})
    bot.reply_to(message, "🎉 Congratulations! You've received 5 bonus coins!")

@bot.message_handler(func=lambda message: message.text == "❓ Help")
def show_help(message):
    send_help(message)

@bot.message_handler(func=lambda message: message.text == "📞 Contact")
def contact_developer(message):
    # Check if user is banned
    user_data = get_user_info(message.from_user.id)
    if user_data.get('is_banned', False):
        bot.reply_to(message, "🚫 Your account has been banned. You cannot use this feature.")
        return

    contact_msg = """
📞📞📞 CONTACT DEVELOPER 📞📞📞

For support, suggestions, or issues:
📧 Email: support@infohanger.com
💬 Telegram: @CEO_KCL_BD

🕒 SUPPORT HOURS:
Monday-Friday: 9 AM - 6 PM
Saturday-Sunday: 10 AM - 4 PM

🛠️ TECHNICAL SUPPORT:
- Bot Issues
- API Problems
- Feature Requests
- Bug Reports

We'll respond within 24 hours!
"""
    bot.send_message(message.chat.id, contact_msg)

@bot.message_handler(func=lambda message: message.text == "📊 Stats")
def admin_stats(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    stats_msg = f"""
📊📊📊 ADMIN STATISTICS 📊📊📊

👥 TOTAL USERS: {user_stats['total_users']}
🟢 ACTIVE USERS: {user_stats['active_users']}
🔗 REFERRED USERS: {user_stats['referred_users']}
📊 TOTAL INFO REQUESTS: {user_stats['total_info_requests']}
🔍 BKASH REQUESTS: {user_stats['total_bkash_requests']}
🎮 FF REQUESTS: {user_stats['total_ff_requests']}

📅 GENERATED AT: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}
"""
    bot.send_message(message.chat.id, stats_msg)

@bot.message_handler(func=lambda message: message.text == "👥 Users")
def list_all_users(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    users_list = []
    for user_id, data in users_db.items():
        if user_id in [ADMIN_ID, MODERATOR_ID]:
            continue
        users_list.append(f"👤 {data.get('first_name', 'Unknown')} (`{user_id}`)")

    if not users_list:
        bot.send_message(message.chat.id, "No users found.")
        return

    # Paginate results
    page_size = 5
    total_pages = (len(users_list) + page_size - 1) // page_size
    current_page = 0

    def send_page(page_num):
        start_idx = page_num * page_size
        end_idx = min((page_num + 1) * page_size, len(users_list))
        page_users = users_list[start_idx:end_idx]

        page_msg = f"""
👥👥👥 USERS LIST (Page {page_num + 1}/{total_pages}) 👥👥👥

{chr(10).join(page_users)}

Use buttons to navigate pages
"""

        markup = InlineKeyboardMarkup()
        if page_num > 0:
            markup.add(InlineKeyboardButton("◀️ Previous", callback_data=f"prev_users_{page_num}"))
        if page_num < total_pages - 1:
            markup.add(InlineKeyboardButton("Next ▶️", callback_data=f"next_users_{page_num}"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_admin"))

        bot.send_message(message.chat.id, page_msg, reply_markup=markup)

    send_page(current_page)

@bot.message_handler(func=lambda message: message.text == "👁️ See User")
def ask_user_id(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    msg = bot.reply_to(message, "🔍 Please enter the User ID to view details:")
    bot.register_next_step_handler(msg, show_user_details)

def show_user_details(message):
    try:
        user_id = int(message.text.strip())
        user_data = users_db.get(user_id, {})

        if not user_data:
            bot.reply_to(message, "❌ User not found.")
            return

        # Determine if user is banned
        status = "🚫 BANNED" if user_data.get('is_banned', False) else "✅ ACTIVE"

        details_msg = f"""
    <<<<👤👤 USER DETAILS 👤👤>>>>
=========================================
👤 NAME: {user_data.get('first_name', 'Unknown')}
🔗 USERNAME: @{user_data.get('username', 'No Username')}
🆔 USER ID: `{user_id}`
💰 COINS: {user_data.get('coins', 0)}
📊 TOTAL REQUESTS: {user_data.get('total_info_requests', 0)}
🔍 BKASH REQUESTS: {user_data.get('total_bkash_requests', 0)}
🎮 FF REQUESTS: {user_data.get('total_ff_requests', 0)}
👥 REFERRED BY: {user_data.get('referred_by', 'None')}
📅 JOIN DATE: {user_data.get('join_date', 'Unknown').strftime('%Y-%m-%d %I:%M:%S %p')}
🚫 STATUS: {status}

📊 USER STATISTICS:
🔸 Total Referrals: {len(user_data.get('referrals', []))}
🔸 Total Info Requests: {user_data.get('total_info_requests', 0)}
🔸 BKASH Requests: {user_data.get('total_bkash_requests', 0)}
🔸 FF Requests: {user_data.get('total_ff_requests', 0)}
"""

        bot.send_message(message.chat.id, details_msg)

    except ValueError:
        bot.reply_to(message, "❌ Invalid User ID format.")

@bot.message_handler(func=lambda message: message.text == "🚫 Ban User")
def ban_user_start(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    msg = bot.reply_to(message, "🚫 Please enter the User ID to ban:")
    bot.register_next_step_handler(msg, ban_user)

def ban_user(message):
    try:
        user_id = int(message.text.strip())
        if user_id in [ADMIN_ID, MODERATOR_ID]:
            bot.reply_to(message, "❌ Cannot ban admin/moderator")
            return

        user_data = users_db.get(user_id, {})
        if not user_data:
            bot.reply_to(message, "❌ User not found.")
            return

        update_user_info(user_id, {"is_banned": True})
        bot.reply_to(message, f"✅ User {user_id} has been banned.")

        # Notify user of ban
        try:
            ban_msg = f"""
🚫🚫🚫 ACCOUNT BANNED 🚫🚫🚫

Dear User,

Your account has been banned by the administrator.

Reason: Unauthorized activity or violation of terms.

To resolve this issue, please contact the administrator:
📲 @CEO_KCL_BD

You cannot use any features of this bot until unbanned.
"""
            bot.send_message(user_id, ban_msg)
        except:
            pass  # Ignore if user blocked bot

    except ValueError:
        bot.reply_to(message, "❌ Invalid User ID format.")

@bot.message_handler(func=lambda message: message.text == "✅ Unban User")
def unban_user_start(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    msg = bot.reply_to(message, "✅ Please enter the User ID to unban:")
    bot.register_next_step_handler(msg, unban_user)

def unban_user(message):
    try:
        user_id = int(message.text.strip())
        if user_id in [ADMIN_ID, MODERATOR_ID]:
            bot.reply_to(message, "❌ Cannot unban admin/moderator")
            return

        user_data = users_db.get(user_id, {})
        if not user_data:
            bot.reply_to(message, "❌ User not found.")
            return

        update_user_info(user_id, {"is_banned": False})
        bot.reply_to(message, f"✅ User {user_id} has been unbanned.")

        # Notify user of unban
        try:
            unban_msg = f"""
🎉🎉🎉 ACCOUNT UNBANNED 🎉🎉🎉

Dear User,

Good news! Your account has been unbanned by the administrator.

You can now use all features of this bot.

Thank you for your cooperation.
"""
            bot.send_message(user_id, unban_msg)
        except:
            pass  # Ignore if user blocked bot

    except ValueError:
        bot.reply_to(message, "❌ Invalid User ID format.")

@bot.message_handler(func=lambda message: message.text == "💰 Give Coins")
def give_coins_start(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    msg = bot.reply_to(message, "💰 Please enter the User ID to give coins:")
    bot.register_next_step_handler(msg, ask_coin_amount)

def ask_coin_amount(message):
    try:
        user_id = int(message.text.strip())
        if user_id in [ADMIN_ID, MODERATOR_ID]:
            bot.reply_to(message, "❌ Cannot give coins to admin/moderator")
            return

        user_data = users_db.get(user_id, {})
        if not user_data:
            bot.reply_to(message, "❌ User not found.")
            return

        msg = bot.reply_to(message, f"💰 How many coins to give to user {user_id}?")
        bot.register_next_step_handler(msg, process_coin_giving, user_id)

    except ValueError:
        bot.reply_to(message, "❌ Invalid User ID format.")

def process_coin_giving(message, user_id):
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            bot.reply_to(message, "❌ Amount must be positive")
            return

        user_data = users_db.get(user_id, {})
        current_coins = user_data.get('coins', 0)
        new_coins = current_coins + amount

        update_user_info(user_id, {"coins": amount})
        user_stats["total_info_requests"] += 1

        # Send confirmation to admin
        admin_msg = f"""
  ✅✅✅ COIN TRANSFER CONFIRMED ✅✅✅
|==========================================|

👤 ADMIN: {message.from_user.first_name}
🆔 ADMIN ID: {message.from_user.id}
💰 AMOUNT SENT: {amount} coins
👤 RECIPIENT: {user_id}
📊 NEW BALANCE: {new_coins} coins
📅 TIME: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
📊 USER STATISTICS:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

👥 Total Referrals: {len(user_data.get('referrals', []))}
📊 Total Requests: {user_data.get('total_info_requests', 0)}
🔍 BKASH Requests: {user_data.get('total_bkash_requests', 0)}
🎮 FF Requests: {user_data.get('total_ff_requests', 0)}

🎉 USER SUCCESSFULLY NOTIFIED!
"""
        bot.reply_to(message, admin_msg)

        # Send confirmation to user
        user_msg = f"""
🎉🎉🎉 COINS RECEIVED! 🎉🎉🎉

💰 You've received {amount} coins from admin!
📊 Your new balance: {new_coins} coins

Thank you for using Info Hanger!
"""
        try:
            bot.send_message(user_id, user_msg)
        except:
            pass  # Ignore if user blocked bot

    except ValueError:
        bot.reply_to(message, "❌ Invalid amount format.")

@bot.message_handler(func=lambda message: message.text == "📢 Broadcast")
def broadcast_start(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    msg = bot.reply_to(message, "📢 Please enter the message to broadcast to all users:")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    broadcast_msg = message.text
    sent_count = 0

    for user_id in users_db:
        if user_id in [ADMIN_ID, MODERATOR_ID]:
            continue
        try:
            bot.send_message(user_id, broadcast_msg)
            sent_count += 1
        except:
            pass  # Ignore errors for individual users

    bot.reply_to(message, f"✅ Broadcast sent to {sent_count} users")

@bot.message_handler(func=lambda message: message.text == "📤 Send Message")
def send_message_start(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Access Denied")
        return

    msg = bot.reply_to(message, "📤 Please enter the User ID to send message:")
    bot.register_next_step_handler(msg, ask_message_content)

def ask_message_content(message):
    try:
        user_id = int(message.text.strip())
        if user_id in [ADMIN_ID, MODERATOR_ID]:
            bot.reply_to(message, "❌ Cannot send message to admin/moderator")
            return

        user_data = users_db.get(user_id, {})
        if not user_data:
            bot.reply_to(message, "❌ User not found.")
            return

        msg = bot.reply_to(message, f"📤 Please enter the message to send to user {user_id}:")
        bot.register_next_step_handler(msg, process_direct_message, user_id)

    except ValueError:
        bot.reply_to(message, "❌ Invalid User ID format.")

def process_direct_message(message, user_id):
    try:
        content = message.text
        bot.send_message(user_id, content)
        bot.reply_to(message, f"✅ Message sent to user {user_id}")
    except Exception as e:
        bot.reply_to(message, f"❌ Failed to send message: {str(e)}")

@bot.message_handler(func=lambda message: message.text == "🔙 Back")
def go_back(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "📋 Select an option:", reply_markup=create_admin_keyboard())
    elif message.from_user.id == MODERATOR_ID:
        bot.send_message(message.chat.id, "📋 Select an option:", reply_markup=create_moderator_keyboard())
    else:
        bot.send_message(message.chat.id, "📋 Select an option:", reply_markup=create_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data.startswith("prev_users_") or call.data.startswith("next_users_"):
        page_num = int(call.data.split("_")[2])
        if call.data.startswith("prev_users_"):
            page_num -= 1
        else:
            page_num += 1

        # Re-send page
        bot.delete_message(call.message.chat.id, call.message.message_id)
        # Note: In a real implementation, we would implement pagination logic here
        # For simplicity, we'll just show the first page again
        bot.send_message(call.message.chat.id, "Pagination not implemented in this demo version")

    elif call.data == "back_to_admin":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "📋 Select an option:", reply_markup=create_admin_keyboard())

# Handle all other messages with a simple error message
@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message):
    # Check if user is banned
    user_data = get_user_info(message.from_user.id)
    if user_data.get('is_banned', False):
        bot.reply_to(message, "🚫 Your account has been banned. You cannot use this feature.")
        return

    if message.from_user.id == ADMIN_ID:
        # Admin should not use regular commands
        bot.reply_to(message, "⚠️ You are logged in as Admin. Please use Admin Panel buttons.")
    elif message.from_user.id == MODERATOR_ID:
        # Moderator should not use regular commands
        bot.reply_to(message, "⚠️ You are logged in as Moderator. Please use Moderator Panel buttons.")
    else:
        # Regular user
        bot.reply_to(message, "❌ Unknown command. Please use the buttons below.")

# Run the bot
if __name__ == "__main__":
    print("Bot started...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error running bot: {e}")