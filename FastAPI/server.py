from urllib.request import urlopen
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from typing import List
from typing import Optional

app = FastAPI()
rovers = []
mines = {}  # changed array to dict to store mine's id, pos_x, pos_y, and serial_num


class Map(BaseModel):
    row: int
    col: int
    moving_map: list[list[int]]  # for 2D array


class Mine(BaseModel):
    id: int
    serialNum: int
    pos_x: int
    pos_y: int


class Rover(BaseModel):
    id: int
    pos_x: int
    pos_y: int
    status: str
    commands: Optional[str] = None


@app.get('/map')
def getMap():
    with open("map.txt") as file:
        row, col = map(int, file.readline().split())
        moving_map = [[int(x) for x in line.split()] for line in file]
    return Map(row=row, col=col, moving_map=moving_map)


@app.put('/map')
def updateMap(map_data: Map):
    with open("map.txt", "w") as file:
        file.write(f"{map_data.row} {map_data.col}\n")
        for line in map_data.moving_map:
            file.write(" ".join(str(x) for x in line) + "\n")
    return {"message": "Map successfully updated"}


@app.get("/mines")
async def get_mines():
    return [mine for mine in mines.values()]


@app.get("/mines/{id}")
async def get_mine(id: int):
    mine = mines.get(f"mine{id}")
    if mine:
        return mine
    else:
        return {"message": f"Mine {id} not found :( "}


@app.delete("/mines/{id}")
async def delete_mine(id: int):
    key = f"mine{id}"
    if key not in mines:
        raise HTTPException(status_code=404, detail="Mine not found")
    del mines[key]
    return {"message": "Mine is deleted!"}


@app.post("/mines")
async def create_mine(mine: Mine):
    if f"mine{mine.id}" in mines:
        return {"error": "Mine with given id already exists"}
    new_mine = Mine(
        id=mine.id,
        serialNum=mine.serialNum,
        pos_x=mine.pos_x,
        pos_y=mine.pos_y
    )
    mines[f"mine{mine.id}"] = new_mine.dict()  # puts the mine into the dict
    return new_mine.dict()


# Requires: a mine to already exist to update it ofc
# looks to see if the id in the mine dictionary
# if yes -> update
# if no -> throw error

@app.put("/mines/{id}")
async def update_mine(id: int, mine: Mine):
    if id not in mines:
        raise HTTPException(status_code=404, detail="Mine not found")
    if mine.pos_x:
        mines[id]["pos_x"] = mine.pos_x
    if mine.pos_y:
        mines[id]["pos_y"] = mine.pos_y
    if mine.serialNum:
        mines[id]["serial_num"] = mine.serialNum

    return mines[id]


@app.get("/rovers")
def get_rovers():
    return rovers


@app.get("/rovers/{rover_id}")
def get_rover(rover_id: int):
    for rover in rovers:
        if rover.id == rover_id:
            return rover
    raise HTTPException(status_code=404, detail="Rover not found")


@app.post("/rovers")
def create_rover(id: int, pos_x: int, pos_y: int, status: str):
    rover = Rover(id=id, pos_x=pos_x, pos_y=pos_y, status=status)  # create a new Rover instance
    rovers.append(rover)
    return {"message": "Rover created successfully"}


@app.delete("/mines/{mine_id}")
def delete_mine(mine_id: int):
    if f"mine{mine_id}" in mines:
        del mines[f"mine{mine_id}"]
        return f"Mine {mine_id} deleted"
    else:
        raise HTTPException(status_code=404, detail=f"Mine {mine_id} not found")


@app.put("/rovers/{rover_id}")
def send_commands(rover_id: int, commands: str):
    for rover in rovers:
        if rover.id == rover_id:
            rover.commands = commands
            return rover.json()
    return {"error": "Rover not found"}


def correct_path(pos_x, pos_y, dx, dy, row, col):  # if you hit edge or go beyond boundary
    x = pos_x + dx
    y = pos_y + dy

    if x < 0 or x > row:
        dx = 0
    if y < 0 or y > col:
        dy = 0
    return dx, dy


@app.post("/rovers/{rover_id}/dispatch")
def dispatch_rover(rover_id: int):
    rover_data = rovers[rover_id - 1]  # Get the data for chosen rover

    row, col, pos_x, pos_y, heading, moves = rover_data

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

    moving_map = [[0 for x in range(col)] for y in range(row)]
    moving_map[0][0] = "*"  # mark starting position as traversed

    for move in moves:
        if move == "D":
            continue
        elif move == "M":
            # Update new position
            dx, dy = move_dict[heading]
            dx, dy = correct_path(pos_x, pos_y, dx, dy, row, col)
            pos_x += dx
            pos_y += dy
            if moving_map[pos_x][pos_y] == "1":
                print(f"Rover {rover_id}: disarmed the mine found at mine at: {pos_x} {pos_y}")
        else:
            # Update new heading
            heading = head_dict[heading][move]

        # Mark traversed path with the *
        moving_map[pos_x][pos_y] = "*"

        with open(f"path{rover_id}.txt", "w") as file:
            for _row in moving_map:
                row_str = "".join(str(elem) for elem in _row)
                file.write(row_str + "\n")

    return {"message": "rover made is successfully."}
