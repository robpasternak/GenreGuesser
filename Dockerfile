FROM python:3.8.6-buster

COPY api /api
COPY GenreGuesser /GenreGuesser
COPY knn.joblib /knn.joblib
COPY svm.joblib /svm.joblib
COPY requirements.txt /requirements.txt
COPY affable-elf-337812-4c0a2ddc2c08.json /credentials.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
