FROM python:3.8-alpine

# Install necessary build dependencies
RUN apk --no-cache add git build-base

COPY . /asca
WORKDIR /asca

# Install Python packages from requirements.txt
RUN pip install -r requirements.txt

# Install the spaCy model
RUN python -m spacy download en_core_web_sm

CMD python manage.py runserver
