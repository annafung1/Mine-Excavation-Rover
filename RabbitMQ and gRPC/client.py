# client.py

import grpc
import pika
import rover_pb2
import rover_pb2_grpc
from random import randint
import json
import string
import random


LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

# M action
move_dict = {
    "N": UP, "E": RIGHT, "S": DOWN, "W": LEFT
}

# Maps old heading to new heading (N, E, S, W)
head_dict = {
    "N": {"L": "W", "R": "E", "M": "N"},
    "E": {"L": "N", "R": "S", "M": "E"},
    "S": {"L": "E", "R": "W", "M": "S"},
    "W": {"L": "S", "R": "N", "M": "W"}
}

# Initialization
pos_x = 0
pos_y = 0
heading = 'S'


def correct_path(pos_x, pos_y, dx, dy, row, col):  # if you hit edge or go beyond boundary
    x = pos_x + dx
    y = pos_y + dy

    if x < 0 or x > row:
        dx = 0
    if y < 0 or y > col:
        dy = 0
    return dx, dy


def traverse_path(moves, row, col, move_dict, head_dict, roverNum):
    pos_x = 0
    pos_y = 0
    heading = 'S'
    moving_map = [[0 for x in range(col)] for y in range(row)]  # declare inside or else it will be overwritten
    # start position: its start spot is considered is traversed
    moving_map[0][0] = "*"
    # mines to disarm

    moving_map[0][1] = "1"
    moving_map[3][6] = "1"
    moving_map[4][6] = "1"
    moving_map[5][7] = "1"
    moving_map[5][8] = "1"

    prev_move = ""

    for moves_ in moves:
        if moves_ == "D":
            prev_move = moves_
        elif moves_ == "M":
            # Update new position
            dx, dy = move_dict[heading]
            dx, dy = correct_path(pos_x, pos_y, dx, dy, row, col)
            pos_x += dx
            pos_y += dy

            # if mine encountered
            if moving_map[pos_x][pos_y] == "1" and (prev_move == 'D'):
                print("Rover " + str(roverNum) + ": found mine at: " + str(pos_x) + " " + str(pos_y))
                length = random.randint(4, 10)
                characters = string.ascii_letters + string.digits
                serial_number= ''.join(random.choice(characters) for _ in range(length))
                id_num = randint(1, 30)

                # Replaced disarming with sending coordinates, id, serial number
                connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                channel = connection.channel()
                channel.queue_declare(queue='deminer-queue')


                demining_info = {
                    "coordinates_x": pos_x,
                    "coordinates_y": pos_y,
                    "id": id_num,
                    "serialNum": serial_number,
                }

                message_body = json.dumps(demining_info)

                channel.basic_publish(exchange='', routing_key='deminer-queue', body=message_body)
                print("Sent demining_info: %r" % demining_info)

                connection.close()

            elif moving_map[pos_x][pos_y] == "1" and (prev_move != 'D'):
                alive = False
                print("Rover " + str(roverNum) + ": found mine at: " + str(pos_x) + " " + str(pos_y))
                print("exploded")
                exit()

        else:  # L, R

            # Update new heading
            heading = head_dict[heading][moves_]
            prev_move = moves_

        moving_map[pos_x][pos_y] = "*"  # Mark traversed path with the *
        file = open("path.txt", "w+")
        for _row in moving_map:
            row_str = " ".join(str(elem) for elem in _row)
            file.write(row_str + "\n")
        file.close()


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = rover_pb2_grpc.RoverServiceStub(channel)

        response = stub.create_files(rover_pb2.getMapRequest())
        row = response.row
        col = response.col
        moving_map = response.moving_map
        # print(f"Moving map: {moving_map}")
        print("check map.txt for your map. Uncomment the previous line if you want to see it in console.")

        roverNum = int(input("Enter rover number: "))

        get_moves_request = rover_pb2.getMovesRequest(roverNum=roverNum)
        response2 = stub.rover_scrape(get_moves_request)
        print("Moves: ", response2.move)

        response = stub.farm_keys(rover_pb2.getSerialNumRequest())
        serial_num = response.serial_num
        # print(f"serial nums: {serial_num}")
        pin_num = response.pin_num
        # print(f"pin nums: {pin_num}")

        traverse_path(response2.move, row, col, move_dict, head_dict, roverNum)


if __name__ == '__main__':
    run()
