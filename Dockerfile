FROM python:3.7
WORKDIR /controller
ADD requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python3", "controller.py"]
