from typing import List


class Customer:

    def __init__(self, id: str, restaurant_id: str, state: int,
                 stress_level: int, sit_together: List(str),
                 will_have_dinner: bool, will_have_dessert: bool) -> None:
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
        self.can_leave = False
        self.left = False

    def sit(self, table_id: int) -> None:
        self.table = table_id

    def order(self, order_id: int) -> None:
        self.order = order_id

    def pay_bill(self) -> None:
        self.can_leave = True
        self.leave()

    def leave(self) -> None:
        self.left = True
