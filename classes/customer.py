from typing import List
from .enums import OrderType


class Customer:

    def __init__(self, id: str = None, restaurant_id: str = None,
                 state: int = None, stress_level: int = None,
                 sit_together: List[str] = [], will_have_dinner: bool = None,
                 will_have_dessert: bool = None) -> None:
        self.id = id
        self.restaurant_id = restaurant_id
        self.state = state
        self.stress_level = stress_level
        self.sit_together = sit_together
        self.will_have_dinner = will_have_dinner
        self.will_have_dessert = will_have_dessert
        self.satisfied = True
        self.table = None
        self.order = None
        self.paid_bills = False
        self.left = False

    def sit(self, table_id: int) -> None:
        self.table = table_id

    def order(self, order_id: int) -> None:
        self.order = order_id
        if OrderType(order_id).name == 'dinner':
            self.will_have_dinner = True
        elif OrderType(order_id).name == 'dessert':
            self.will_have_dessert = True

    def pay_bills(self) -> None:
        self.paid_bills = True

    def leave(self) -> None:
        if self.paid_bills:
            self.satisfied = True
        else:
            self.satisfied = self.table is None

        self.left = True

    def __str__(self):
        return self.id
