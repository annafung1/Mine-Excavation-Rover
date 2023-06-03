import hashlib
import sys
from random import randint
from hashlib import sha256
import pika
import time
import json
start_time = time.time()
j = 1
mine_keys = []


def create_mine_keys(pin_num, serial_num):
    global mine_keys
    for pin, serial in zip(pin_num, serial_num):
        mine_key = pin + serial
        mine_keys.append(mine_key)
    return mine_keys


def disarm_mine():
    global pin
    disarmed = False

    mine_key_ra = str(randint(2, 5))
    sha256_hash = hashlib.sha256(mine_key_ra.encode('utf-8')).hexdigest()

    if (sha256_hash[:6]) != "0000000":
        pin = sha256_hash
        disarmed = True
    if disarmed:

        print("You disarmed the mine. PIN sent to queue")
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='deminer-queue')

        def callback(ch, method, properties, body):
            # Deserialize the JSON --> dictionary
            demining_info = json.loads(body.decode())

            # Extract vars
            serial_num = demining_info["serialNum"]
            coord = f"{demining_info['coordinates_x']},{demining_info['coordinates_y']}"
            id_ = demining_info["id"]

            # concat to create pin
            message = str(serial_num) + str(coord) + str(id_)

            #Publish Pin
            channel.basic_publish(exchange='', routing_key='deminer-queue', body=message)
            print(" [x] Sent PIN: " + str(message))

            # Verify that the function is being runn
            print("Received demining_info: %r" % demining_info)

        channel.basic_consume(queue='deminer-queue', on_message_callback=callback, auto_ack=True)

        print('Waiting for messages...')
        channel.start_consuming()

        message = pin
        channel.basic_publish(exchange='', routing_key='deminer-queue', body=pin)

        print(" [x] Sent PIN: " + str(message))
        connection.close()
        return disarmed
    else:
        print("You failed to disarm the mine. Exploded :( ")
        return False


def run():
    while True:
        deminer_num = int(input("Enter a deminer number (1= disarm mine or 2= don't disarm mine): "))
        if deminer_num == 1:
            disarm_mine()
            break
        elif deminer_num == 2:
            print('Chose not to disarm: exploded')
            sys.exit()
        else:
            print('Invalid option. Please enter 1 to disarm the mine or 2 to not disarm.')


if __name__ == '__main__':
    run()
