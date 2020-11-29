FROM python:3.7

RUN mkdir -p /work
WORKDIR /work

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY model ./model
COPY evaluator ./evaluator
COPY bot .

CMD ["python", "bot.py"]
