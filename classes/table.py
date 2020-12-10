from typing import List
from .customer import Customer


class Table:

    def __init__(self, id, size=4):
        self.id = id
        self.size = size
        self.customers: List[Customer] = []
        self.table_closed = False
