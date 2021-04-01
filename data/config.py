import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

admins = [
    469606979,
]

allowed_users = []

ip = os.getenv("ip")

schedule_data_name = 'schedule.json'
group_data_name = 'groups.json'
group_names_name = 'group_names.txt'
