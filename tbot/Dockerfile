FROM python:3.12

WORKDIR /Project

COPY . /Project

EXPOSE 5432



COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]