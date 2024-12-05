import json


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def as_list(self):
        return list(self.__dict__.values())


def get_static_messages():
    with open("static_messages.json") as json_file:
        data = json.load(json_file)
        return Struct(**data)


messages = get_static_messages()
