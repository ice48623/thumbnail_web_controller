from flask import Flask
import os
import pika
app = Flask(__name__)

@app.route("/")
def main():
    return "hello"

@app.route("/add")
def add_job_to_queue():
    add_one("hello")
    return "added"

@app.route("/addAll")
def add_all():
    return ""

@app.route("/list")
def list():
    return ""

def add_one(message):
    RABBIT_HOST = os.getenv('RABBIT_HOST','localhost')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue')

    channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message)
    connection.close()

if __name__ == '__main__':
    print("Starting Flask ...")
    app.run(host="0.0.0.0", debug=True, port=5000)
