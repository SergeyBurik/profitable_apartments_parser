FROM python:3.10 AS builder

COPY requirements.txt .

WORKDIR . /profitable_apartments_parser
COPY . .
RUN pip install --user -r requirements.txt
CMD ["python", "profitable_apartments_parser/main.py"]