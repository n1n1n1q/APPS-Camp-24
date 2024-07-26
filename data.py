"""
Data module
"""


def load_data(path, data_type):
    """
    Load data
    """
    match data_type:
        case "users":
            with open(path, "r", encoding="utf-8") as file:
                data = file.read().split("\n")
            users = set()
            while data.count(""):
                data.remove("")
            for line in data:
                line = line.split(",COMMA,")
                users.add((int(line[0]), line[1]))
            return users
        case "messages":
            with open(path, "r", encoding="UTF-8") as file:
                data = file.read().split("\n")
            return set(line for line in data if line != "")
        case "questions":
            with open(path, "r", encoding="UTF-8") as file:
                data = file.read().split("\n")
            return set(line for line in data if line != "")
        case _:
            raise ValueError(
                f"Invalid data type! \
Possible options: users, messages. Got: f{data_type}"
            )


def save_data(data, data_type, chat_id):
    """
    Save data
    """
    path = "data/"
    match data_type:
        case "users":
            path += f"users_{chat_id}"
            data = [str(id) + ",COMMA," + name for id, name in data]
        case "messages":
            path += f"chat_{chat_id}"
        case _:
            raise ValueError(
                f"Invalid data type! \
Possible options: users, messages. Got: f{data_type}"
            )
    with open(path, "w", encoding="UTF-8") as file:
        file.write("\n".join(list(data)))
