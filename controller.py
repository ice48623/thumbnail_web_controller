from flask import Flask, request
import os
import pika
import json
import requests
app = Flask(__name__)

def add_one(message):
    RABBIT_HOST = os.getenv('RABBIT_HOST','localhost')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue')

    channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message)
    connection.close()

@app.route("/add", methods=['POST'])
def add_job_to_queue():
    video_host = os.getenv('STORAGE_HOST','localhost')
    video_bucket_name = request.args.get('bucket')
    video_object_name = request.args.get('object')
    target_host = video_host
    target_bucket_name = request.args.get('t_bucket')
    target_object_name = request.args.get('t_object')
    order = {
        "video_host": video_host,
        "video_bucket_name": video_bucket_name,
        "video_object_name": video_object_name,
        "gif_host": target_host,
        "gif_target_bucket_name": target_bucket_name,
        "gif_target_object_name": target_object_name
    }
    j_order = json.dumps(order)
    add_one(j_order)
    return j_order

@app.route("/addAll", methods=['POST'])
def add_all():
    video_host = os.getenv('STORAGE_HOST','localhost')
    video_bucket_name = request.args.get('bucket')
    r = get_all_object_in_bucket(video_host, video_bucket_name)

    sended = []
    for object in r.get('objects'):
        name = object.get('name')
        order = {
            "video_host": video_host,
            "video_bucket_name": video_bucket_name,
            "video_object_name": name,
            "gif_host": video_host,
            "gif_target_bucket_name": video_bucket_name,
            "gif_target_object_name": name.split(".")[0] + ".gif"
        }
        j_order = json.dumps(order)
        add_one(j_order)
        sended.append(name)
    return str(sended)

def get_all_object_in_bucket(host, bucket, port = "8080"):
    url = "http://" + host + ":" + port + '/' + bucket + "?list"
    r = requests.get(url)
    return r.json()

@app.route("/list", methods=['GET'])
def list():
    return ""



if __name__ == '__main__':
    print("Starting Flask ...")
    app.run(host="0.0.0.0", debug=True, port=5000)
