import botpy
from botpy.message import Message
import json
from botpy import logging

with open("config.json") as f:
	config_dict = json.load(f)

_log = logging.get_logger()

class MyClient(botpy.Client):
	async def on_at_message_create(self, message: Message):
		await self.api.post_dms(guild_id="1123174024", content="hello")
		
	async def on_ready(self):
		messageResult = await self.api.post_group_message(
		group_openid="54FF644A2CB05A0AEF1517BF99E5A25B",
		msg_type=0, 
		content="hello")
		_log.info(messageResult)


intents = botpy.Intents(public_guild_messages=True)
client = MyClient(intents=intents, is_sandbox=True)
client.run(appid=config_dict["bot_info"]["test_bot_id"], secret=config_dict["bot_info"]["test_bot_secret"])

