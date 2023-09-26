import json

data: dict = None
with open("constants.json", "r") as file:
    data = json.load(file)

# constants
fieldsize: int = data["size"]
shapes: list = data["shapes"]
shapesize: int = data["shapesize"]