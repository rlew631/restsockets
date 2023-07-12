FROM python:3.10

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD [ "python", "server.py"]
