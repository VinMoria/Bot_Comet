from openai import OpenAI
import json
import webbrowser


with open("config.json") as f:
	config_dict = json.load(f)
gpt_client = OpenAI(api_key=config_dict["ai_key"]["chatgpt_key"])
in_prompt = input("Prompt: ")

response = gpt_client.images.generate(
	model="dall-e-3",
	prompt=in_prompt,
	size="1024x1024",
	quality="standard",
	n=1,
)
image_url = response.data[0].url
webbrowser.open(image_url)
print(image_url)
