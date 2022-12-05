# encoding: utf-8

class Photo:
    def __init__(self, name: str, city: str, dt: str, order: str):
        self.file_name = name
        self.city = city.replace('/', '-') if city != '' else 'unknown'

        self.date = dt.replace(':', '-')
        self.order = order

    def build_name(self, num: int) -> str:
        return f'{self.city}_{num:04d}'

    def dir_name(self) -> str:
        return f'{self.date}'

    def __repr__(self):
        return f"<Photo(file='{self.file_name}', city='{self.city}' date='{self.date}')>"
