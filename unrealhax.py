import asyncio
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from keep_alive import keep_alive
import aiohttp

keep_alive()

TELEGRAM_BOT_TOKEN = '8043788530:AAHCqV0TcIA3Mx_0Kf5AewB5GQsCBMD6Iuw'
ADMIN_USER_ID = 7903853982
USERS_FILE = 'users.txt'
attack_in_progress = False

# List of proxies
proxies = [
    "198.23.239.134:6540:hhtggivt:1m1zhqrwi6xi",
    "207.244.217.165:6712:hhtggivt:1m1zhqrwi6xi",
    "107.172.163.27:6543:hhtggivt:1m1zhqrwi6xi",
    "64.137.42.112:5157:hhtggivt:1m1zhqrwi6xi",
    "173.211.0.148:6641:hhtggivt:1m1zhqrwi6xi",
    "161.123.152.115:6360:hhtggivt:1m1zhqrwi6xi",
    "167.160.180.203:6754:hhtggivt:1m1zhqrwi6xi",
    "154.36.110.199:6853:hhtggivt:1m1zhqrwi6xi",
    "173.0.9.70:5653:hhtggivt:1m1zhqrwi6xi",
    "173.0.9.209:5792:hhtggivt:1m1zhqrwi6xi",
]

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

# Function to get a random proxy
def get_proxy():
    return random.choice(proxies)

async def proxy_rotator():
    while True:
        current_proxy = get_proxy()
        print(f"Switching to proxy: {current_proxy}")
        await asyncio.sleep(60)  # Change proxy every 1 minute

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🇮🇳 𓆩 𝐕𝐄𝐍𝐎𝐌&𝐄𝐗𝐓𝐄𝐍𝐁𝐎𝐓 𓆪 🇮🇳*\n\n"
        "*𖤍 𝐔𝐬𝐞 /𝐚𝐭𝐭𝐚𝐜𝐤 <𝐢𝐩> <𝐩𝐨𝐫𝐭> <𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧> 𖤍*\n"
        "*🔥 𝐑𝐄𝐀𝐃𝐘 𝐓𝐎 𝐅𝐔𝐂𝐊 𝐁𝐆𝐌𝐈 🔥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Example of using the current proxy with aiohttp
async def run_attack(chat_id, ip, port, duration, context):
    global attack_in_progress
    attack_in_progress = True
    current_proxy = get_proxy()
    proxy_url = f"http://{current_proxy.split(':')[2]}:{current_proxy.split(':')[3]}@{current_proxy.split(':')[0]}:{current_proxy.split(':')[1]}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://example.com', proxy=proxy_url) as response:
                print(await response.text())

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*📵 Proxy Error: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed!*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*🔥 You need to be approved to use this bot.*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*📵 Another attack is already in progress.*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*✅ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*✅ Attack Launched!*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*🈲 Enjoy and dominate!*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    
    # Start proxy rotation task
    asyncio.create_task(proxy_rotator())

    application.run_polling()

if __name__ == '__main__':
    main()