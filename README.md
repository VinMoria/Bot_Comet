# Bot_Comet

将QQ机器人连接到 AI 的 API，ChatGPT 和 Gemini

# 运行前配置

1. 将 config-template.json 复制一份重命名为 config.json，并按需填写其中的内容

2. 安装python库

``` shell
pip install qq-botpy
pip install openai
pip install google-generativeai
```

# 运行

python执行对应的 main_chatgpt.py 或 main_germini.py

> 文件包含一个Dockerfile，可使用docker部署

# Extra
追加了talk.py与gen_image.py，用于简单与chatgpt对话与图片生成
