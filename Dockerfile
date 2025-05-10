FROM python:3.13.3-alpine
WORKDIR /code
RUN python -m venv .venv
RUN source ./.venv/bin/activate
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . . 
RUN pip install --editable .
CMD ["python", "-m", "src"]