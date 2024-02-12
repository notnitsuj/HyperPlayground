FROM python:3.9

COPY . .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "localhost", "--port", "8000"]