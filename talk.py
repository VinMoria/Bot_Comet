from openai import OpenAI
import json
from datetime import datetime

SAVE_PATH = "history"
	
def create_and_write_md(file_path, content):
    # 写入markdown
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
	# 加载配置文件
	with open("config.json") as f:
		config_dict = json.load(f)

	# 实例化gpt对象
	gpt_client = OpenAI(api_key=config_dict["ai_key"]["chatgpt_key"])

	# 获取时间作为笔记默认名称
	now = datetime.now()
	timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
	filename = f"{SAVE_PATH}/{timestamp}.md"

	# 进入对话
	print(f"Welcome, using {config_dict["ai_key"]['chatgpt_model']}. type in 'bye' to end")
	history_context = []
	while True:
		print("---------------------------------------------------")
		q = input("Me >> ")
		if q == "bye":
			break
		history_context.append({"role": "user", "content": q})
		completion = gpt_client.chat.completions.create(
			model=config_dict["ai_key"]["chatgpt_model"],
			messages=history_context
        )
		assistant_reply = completion.choices[0].message.content
		history_context.append({"role": "assistant", "content": assistant_reply})
		print(f"AI >> {assistant_reply}")

	# 存储对话历史
	content = ""
	for line in history_context:
		if line["role"] == "user":
			content += "# User: \n\n"
		else:
			content += "# GPT: \n\n"
		content += line["content"] + "\n\n"
	create_and_write_md(filename, content)
	print(f"save in {filename}")
	