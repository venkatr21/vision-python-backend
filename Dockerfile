FROM python:3.7
RUN apt-get update && apt-get -y install ffmpeg
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8000
ENV NAME visionstt
CMD ["python", "app.py"]

