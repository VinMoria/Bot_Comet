# -*- coding: utf-8 -*-
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
from openai import OpenAI
import json
import re

with open("config.json") as f:
	config_dict = json.load(f)

_log = logging.get_logger()
history_context = []

# def receive_and_gen(in_str):
# 	in_str = in_str.strip()
# 	# 指令模式
# 	if in_str[0] == "~":
# 		#  修改chatgpt人设
# 		if in_str[0:2] == "~s":
# 			role_text = in_str[3:]
# 			chatgpt_system_set(role_text)
# 			res = f"修改chatgpt人设: [{role_text}]"
# 		# 清楚上下文
# 		elif in_str[0:2] == "~c":
# 			chatgpt_clean_history()
# 			res = "清除 chatgpt 上下文记忆"
# 		elif in_str[0:2] == "~i":
# 			image_prompt = in_str[3:]
# 		else:
# 			res = "指令不存在"
# 	# 对话模式
# 	else:
# 		res = chatgpt_talk(in_str)
# 	return res

def chatgpt_system_set(role_text):
	history_context.append({"role": "system", "content": role_text})
	return chatgpt_gen()

def chatgpt_clean_history():
	history_context = []

def chatgpt_talk(q):
	history_context.append({"role": "user","content": q})
	return chatgpt_gen()

def chatgpt_gen():
	global client
	completion = gpt_client.chat.completions.create(
		model=config_dict["ai_key"]["chatgpt_model"],
		messages=history_context
	)
	assistant_reply = completion.choices[0].message.content
	assistant_reply = assistant_reply.replace("*","")
	# block发送的url，qq不允许
	url_pattern = r'https?://\S+|www\.\S+'
	assistant_reply = re.sub(url_pattern, '[url blocked]', assistant_reply)
	
	# 将助手的回复添加到对话历史
	history_context.append({"role": "assistant", "content": assistant_reply})
	
	# 返回助手的回复
	return assistant_reply

def chatgpt_gen_image(in_prompt):
	response = gpt_client.images.generate(
	model="dall-e-3",
	prompt=in_prompt,
	size="1024x1024",
	quality="standard",
	n=1,
	)
	image_url = response.data[0].url
	print(image_url)
	return image_url

class MyClient(botpy.Client):
	async def on_ready(self):
		_log.info(f"robot 「{self.robot.name}」 on_ready!")

	async def on_group_at_message_create(self, message: GroupMessage):
		in_str = message.content.strip()
		# 指令模式
		if in_str[0] == "~":
			#  修改chatgpt人设
			if in_str[0:2] == "~s":
				role_text = in_str[3:]
				chatgpt_system_set(role_text)
				await self.send_text(message, f"修改chatgpt人设: [{role_text}]")
			# 清楚上下文
			elif in_str[0:2] == "~c":
				chatgpt_clean_history()
				await self.send_text(message, "清除 chatgpt 上下文记忆")
			# 图片生成
			elif in_str[0:2] == "~i":
				image_prompt = in_str[3:]
				await self.send_image(message, image_prompt)
			else:
				await self.send_text(message, "指令不存在")
		# 对话模式
		else:
			await self.send_text(message, chatgpt_talk(in_str))

	async def send_text(self, message, send_content):
		messageResult = await message._api.post_group_message(
			group_openid=message.group_openid,
			msg_type=0, 
			msg_id=message.id,
			content=send_content)
		_log.info(messageResult)

	async def send_image(self, message, image_prompt):
		image_url = chatgpt_gen_image(image_prompt)

		uploadMedia = await message._api.post_group_file(
			group_openid=message.group_openid,
			file_type=1,
			url=image_url
		)

		await message._api.post_group_message(
			group_openid=message.group_openid,
			msg_type=7,
			msg_id=message.id,
			msg_seq=1,
			media=uploadMedia
		)

if __name__ == "__main__":
	# Chatgpt
	gpt_client = OpenAI(api_key = config_dict["ai_key"]["chatgpt_key"])
	print("GPT init")
	# qq-bot
	intents = botpy.Intents(public_messages=True)
	client = MyClient(intents=intents, is_sandbox=True)
	client.run(appid=config_dict["bot_info"]["bot_id"], secret=config_dict["bot_info"]["bot_secret"])
