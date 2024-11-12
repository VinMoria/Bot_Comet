FROM python
RUN pip install openai
RUN pip install qq-botpy
WORKDIR /app
COPY . .
CMD ["python", "/app/main_chatgpt.py"]