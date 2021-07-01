FROM python:3
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install -r requirements.txt
COPY . /app
CMD [ "python", "timer.py" ]