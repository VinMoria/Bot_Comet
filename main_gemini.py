# -*- coding: utf-8 -*-
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
import google.generativeai as genai
import re
import json

with open("config.json") as f:
	config_dict = json.load(f)

_log = logging.get_logger()

def ask_gemini(q):
    global model
    r = model.generate_content(q)
    raw_text = r.candidates[0].content.parts[0].text
    raw_text = raw_text.replace("*","")
    # block发送的url，qq不允许
    url_pattern = r'https?://\S+|www\.\S+'
    new_text = re.sub(url_pattern, '[url blocked]', raw_text)

    return new_text

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0, 
              msg_id=message.id,
              content=f"Gemini: {ask_gemini(message.content)}")
        _log.info(messageResult)


if __name__ == "__main__":
	#Gemini

    genai.configure(api_key=config_dict["ai_key"]["gemini_key"])
    model = genai.GenerativeModel(config_dict["ai_key"]["gemini_model"])

	# qq-bot
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid=config_dict["bot_info"]["bot_id"], secret=config_dict["bot_info"]["bot_secret"])

