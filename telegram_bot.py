import telegram

class Telegram:
    def __init__(self, token, channel_id):
        self.token = token
        self.bot = telegram.Bot(token=token)
        self.channel_id = channel_id
    

    async def send_message(self, message: str):
        print(await self.bot.send_message(chat_id=self.channel_id, text=message))
