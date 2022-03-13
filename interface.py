from kombu import Connection, Exchange, Producer, Queue
from colorama import Fore, Style

import time

rabbit_url = 'amqp://guest:guest@localhost:5672//'

conn = Connection(rabbit_url)
channel = conn.channel()

exchange = Exchange("message", type="direct", delivery_mode=1)

producer = Producer(exchange=exchange, channel=channel)

queue = Queue(name="messages", exchange=exchange, durable=True, exclusive=False, auto_delete=False) 
queue.maybe_bind(conn)
queue.declare()

command_line_text = ""
while True:
    command_line_text = input("Entry message to send: ")

    producer.publish(command_line_text)

    if command_line_text != "quit()":
        print(f"{Fore.GREEN}Message was successfully sent {Style.RESET_ALL}\n")
    else:
        break

    time.sleep(0.001)

conn.close()