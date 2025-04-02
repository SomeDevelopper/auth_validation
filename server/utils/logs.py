from flask import request
from functools import wraps
import json
import datetime
from kafka import KafkaProducer


def log_request_info(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        try:
            response = route_function(*args, **kwargs)
            raw_data = response.data.decode('utf-8')

            try:
                parsed_data = json.loads(raw_data)
                pretty_response = parsed_data
            except:
                pretty_response = raw_data

            request_infos = {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'route': request.path,
                'ip_address': request.headers.get('X-Forwarded-For', request.remote_addr),
                'response': pretty_response['result']
            }

            producer_log(request_infos)

            return response

        except Exception as e:
            error_message = f"Erreur lors de la journalisation de la requête : {e}"
            print(error_message)
    return wrapper

def producer_log(request_info):
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    producer.send('kafka_log', request_info)