from enum import Enum


class State(Enum):
    waiting_outside = 0
    waiting_on_full_table = 1
    waiting_for_order = 2
    eating = 3
    waiting_bill = 4
    left = 5


class OrderType(Enum):
    dinner = 0
    dessert = 1
