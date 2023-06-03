# server.py

import grpc
from concurrent import futures
import rover_pb2
import rover_pb2_grpc
import time
from random import randint
from urllib.request import urlopen
import pika

map_dimensions = []


class RoverServicer(rover_pb2_grpc.RoverServiceServicer):
    def create_files(self, request, context):
        rows = 10
        cols = 10

        with open("mine.txt", "w+") as file:  # create mine file
            file.write("000 d2\n")
            file.write("03 1e \n")
            file.write("00 8AD1 \n")
            file.write("123 2F95")

        with open("map.txt", "w+") as file:  # create map.txt file, generates 2 numbers: val 1= row, val 2= column
            for i in range(2):
                file.write(str(randint(30, 30)) + " ")

        with open("map.txt", "r") as file:  # create moving_map to use for traversal
            for i in file:
                map_dimensions.extend(map(int, i.split()))  # extend will add items 1 by 1 and split for whitespace
                rows = map_dimensions[0]
                cols = map_dimensions[1]

        with open("map.txt", "a") as file:
            file.write("\n")
            for j in range(rows):
                file.write("".join("0" for j in range(cols)))
                file.write("\n")

        with open("path.txt", "w+") as file:
            for j in range(rows):
                file.write("".join("0" for j in range(cols)))
                file.write("\n")

        moving_maps = [[0 for x in range(cols)] for y in range(rows)]
        flattened_map = [x for row in moving_maps for x in row]

        response = rover_pb2.getMapResponse()
        response.row = rows
        response.col = cols
        response.moving_map.extend(flattened_map)

        return response

    def get_moves(self,roverNum):
        url = "https://coe892.reev.dev/lab1/rover/" + str(roverNum)
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        moves = (html.strip('{"result":true,"data":{"moves":""}}'))
        return moves

    def rover_scrape(self, request, context):
        print(f"Received request for rover number {request.roverNum}")
        moves = self.get_moves(request.roverNum)
        return rover_pb2.getMovesResponse(move=moves)

    def farm_keys(self, request, context):
        pin = []
        serial = []

        with open("mine.txt", "r") as file:
            for i in file.readlines():
                pin_num, serial_nums = i.split()
                pin.append(str(pin_num))
                serial.append(str(serial_nums))

        response = rover_pb2.getSerialNumResponse()
        response.serial_num.extend(serial)
        response.pin_num.extend(pin)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rover_pb2_grpc.add_RoverServiceServicer_to_server(RoverServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started, using port 50051.")

    # Start RabbitMQ connection & channel
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #Queue
    channel.queue_declare(queue='deminer-queue')

    # Start Consuming messages
    def callback(ch, method, properties, body):
        print("Received PIN: %r" % body)

    channel.basic_consume(queue='deminer-queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages...')
    channel.start_consuming()

    try:
        while True:
            time.sleep(2023)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()