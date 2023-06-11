FROM python:3.7.3

WORKDIR /sf_encoder
COPY . .
RUN pip install -r requirements.txt

EXPOSE 9000

CMD python ./app.py