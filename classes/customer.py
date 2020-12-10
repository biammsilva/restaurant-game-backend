from typing import List
from .enums import OrderType, State
from .exceptions import OrderDeliveredWrong


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
        self.orders = []
        self.paid_bills = False
        self.left = False

    def sit(self, table_id: int) -> None:
        self.table = table_id
        self.state = State.waiting_on_full_table

    def submit_order(self, order: OrderType) -> None:
        self.orders.append(order)
        self.state = State.waiting_for_order

    def get_order(self, order: OrderType) -> None:
        if order not in self.orders:
            raise OrderDeliveredWrong()
        self.orders.remove(order)
        self.state = State.eating

    def pay_bills(self) -> None:
        self.paid_bills = True

    def leave(self) -> None:
        if self.paid_bills:
            self.satisfied = True
        elif self.table and (
                not self.will_have_dinner and not self.will_have_dessert
             ):
            self.satisfied = True
        else:
            self.satisfied = self.table is None

        self.left = True

    def __str__(self):
        return self.id
