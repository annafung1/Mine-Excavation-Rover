import requests
from server import rovers, Rover
from tabulate import tabulate
base_url = "http://localhost:8000"

# uvicorn server:app --reload --port 8000
while True:
    print("Menu Options:")
    print("1. Get map")
    print("2. Update map")
    print("3. List all mines")
    print("4. Get a specific mine using its id ")
    print("5. Create a new mine")
    print("6. Update a mine")
    print("7. Delete a mine")
    print("8. List all rovers")
    print("9. Get a specific rover using id ")
    print("10. Create a new rover")
    print("11. Update a rover commands")
    print("12. Dispatch a rover using id")
    print("0. Exit program")

    selection = input("Select an option: ")

    '''
     elif selection == "8":
         print("Rovers:")
         for rover in rovers:
             print(f"Rover id: {rover.id}")
             print(f"Coordinates: ({rover.pos_x}, {rover.pos_y})")
             print(f"Status: {rover.status}")
     '''

    if selection == "1":
        response = requests.get(f"{base_url}/map")
        print(response.json())
    elif selection == "2":
        row = int(input("Enter the new row: "))
        col = int(input("Enter the new col: "))
        moving_map = [[0 for _ in range(col)] for _ in range(row)]
        response = requests.put(f"{base_url}/map", json={"row": row, "col": col, "moving_map": moving_map})
        print(response.json())
    elif selection == "3":
        response = requests.get(f"{base_url}/mines")
        print(response.json())
    elif selection == "4":
        mine_id = input("Enter the mine ID: ")
        response = requests.get(f"{base_url}/mines/{mine_id}")
        print(response.json())
    elif selection == "5":
        id = int(input("Enter the mine id: "))
        pos_x = int(input("Enter the x coordinate: "))
        pos_y = int(input("Enter the y coordinate: "))
        serialNum = int(input("Enter the serial number: "))
        payload = {"id": id, "serialNum": serialNum, "pos_x": pos_x, "pos_y": pos_y}
        response = requests.post(f"{base_url}/mines", json=payload)
        new_mine = response.json()
        print(
            f"New mine added:\nid: {new_mine['id']}\nSerial Number: {new_mine['serialNum']}\nCoordinates: ({new_mine['pos_x']}, {new_mine['pos_y']})")
    elif selection == "6":
        mine_id = input("Enter the mine id: ")
        pos_x = input("Enter the new x coordinate: ")
        pos_y = input("Enter the new y coordinate: ")
        serial_number = input("Enter the new serial number: ")
        data = {}
        print(f"mine {mine_id } updated")
    elif selection == "7":
        mine_id = input("Enter the mine ID: ")
        response = requests.delete(f"{base_url}/mines/{mine_id}")
        print(response.json())

    elif selection == "8":
        headers = ["rover id", "x-coord", "y-oord", "status"]
        data = [[rover.id, rover.pos_x, rover.pos_y, rover.status] for rover in rovers]
        table = tabulate(data, headers=headers, tablefmt="grid")
        print(table)
    elif selection == "9":
        rover_id = input("Enter the rover ID: ")
        response = requests.get(f"{base_url}/rovers/{rover_id}")
        print(response.json())
    elif selection == "10":
        rover_id = int(input("Enter rover id: "))
        pos_x = int(input("Enter the x coordinate: "))
        pos_y = int(input("Enter the y coordinate: "))
        status = input("Enter rover status: ")
        rover = Rover(id=rover_id, pos_x=pos_x, pos_y=pos_y, status=status)
        rovers.append(rover)
        print(f"Rover {rover_id} added successfully.")
    elif selection == "11":
        rover_id = int(input("Enter the rover id: "))
        commands = input("Enter the new commands: ")
        url = f"{base_url}/rovers/{rover_id}"
        response = requests.put(url, json={"commands": commands})
        print(f"The commands: {commands} have been added for rover {rover_id}")
    elif selection == "12":
        rover_id = input("Enter the rover id to dispatch: ")
        response = requests.post(f"{base_url}/rovers/{rover_id}/dispatch")
        print("rover dispatched..")
        print(response.json())
    elif selection == "0":
        print("Exiting program...")
        break
