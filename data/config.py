import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    __BOT_TOKEN = os.getenv("BOT_TOKEN")
    __admins = [
        469606979,
    ]

    __allowed_users = []

    __ip = os.getenv("ip")

    __schedule_data = {}
    __group_data = {}
    __group_names = []

    @classmethod
    def get_bot_token(cls):
        return cls.__BOT_TOKEN

    @classmethod
    def get_admins(cls):
        return cls.__admins

    @classmethod
    def get_allowed_users(cls):
        return cls.__allowed_users

    @classmethod
    def get_ip(cls):
        return cls.__ip

    @classmethod
    def get_schedule_data(cls):
        return cls.__schedule_data
    
    @classmethod
    def set_schedule_data(cls, data):
        cls.__schedule_data = data

    @classmethod
    def get_group_data(cls):
        return cls.__group_data
    
    @classmethod
    def set_group_data(cls, data):
        cls.__group_data = data

    @classmethod
    def get_group_names(cls):
        return cls.__group_names
    
    @classmethod
    def set_group_names(cls, data):
        cls.__group_names = data
