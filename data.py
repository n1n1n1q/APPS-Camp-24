"""
Data module
"""


def load_data(path):
    """
    Load data
    """
    with open(path, "r", encoding="UTF-8") as file:
        data = file.read().split("\n")
    return set(line for line in data if line != "")


def save_data(data, data_type, chat_id):
    """
    Save data
    """
    path = "data/"
    match data_type:
        case "users":
            path += f"users-{chat_id}"
        case "messages":
            path += f"chat-{chat_id}"
        case _:
            raise ValueError(
                f"Invalid data type! \
Possible options: users, messages. Got: f{data_type}"
            )
    with open(path, "r", encoding="UTF-8") as file:
        file.write("\n".join(list(data)))
