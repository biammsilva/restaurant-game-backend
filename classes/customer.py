from typing import List, Any
from datetime import datetime

from .enums import State, OrderType


class Customer:

    def __init__(self, id: str, state: int, stress_level: int, restaurant: Any,
                 restaurant_id: int = None, sit_together: List[str] = None,
                 will_have_dinner: bool = None,
                 will_have_dessert: bool = None):
        self.id = id
        self.restaurant_id = restaurant_id
        self.restaurant = restaurant
        self.stress_level = stress_level
        self.sit_together = sit_together
        self.will_have_dessert = will_have_dessert
        self.will_have_dinner = will_have_dinner
        self.satisfied = True
        self.state = state

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def state(self):
        return self.state

    @state.setter
    def state(self, value):
        if self.restaurant.state == 0:
            self.return_message = None
            if value == State.waiting_outside.value:
                if not self.will_have_dessert and not self.will_have_dinner:
                    self.please_leave()
                    return
                table = self.restaurant.find_table(self)
                if table is not None:
                    self.please_sit(table)
                else:
                    self.restaurant.add_to_line(self)
            elif value == State.waiting_on_full_table.value:
                if self.will_have_dinner:
                    self.order_id = OrderType.dinner.value
                    self.will_have_dinner = False
                    self.take_order()
                    self.last_order_time = datetime.now()
                elif self.will_have_dessert:
                    customers_table = self.restaurant.tables[self.table]
                    for customer in customers_table:
                        if not customer.ate_dinner():
                            self.return_message = '#'
                            return
                    self.order_id = OrderType.dessert.value
                    self.will_have_dessert = False
                    self.take_order()
                    self.last_order_time = datetime.now()
            elif value == State.waiting_for_order.value:
                if not self.restaurant.is_order_time_ok(self.last_order_time):
                    self.return_message = '#'
                    return
                if self.order_id is not None:
                    self.deliver_order()
            elif value == State.eating.value:
                pass
            elif value == State.waiting_bill.value:
                customers_table = self.restaurant.tables[self.table]
                for customer in customers_table:
                    if not customer.ate_dessert():
                        self.return_message = '#'
                self.return_message = {
                    "name": "bring_bill",
                    "payload": {
                        "customer_id": self.id,
                        "table_id": self.table
                    }
                }
            elif value == State.left.value:
                table = self.table
                self.restaurant.remove_customer(self)
                if self.restaurant.has_empty_tables():
                    customer = self.restaurant.next_in_line()
                    if customer:
                        customer.please_sit(table)

    def please_sit(self, table_id: int):
        self.table = table_id
        self.return_message = {
            "name": "please_sit",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
            }
        }

    def please_leave(self):
        self.return_message = {
            "name": "please_leave",
            "payload": {
                "customer_id": self.id,
            }
        }

    def take_order(self):
        self.return_message = {
            "name": "take_order",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
                "order_id": self.order_id
            }
        }

    def deliver_order(self):
        self.return_message = {
            "name": "deliver_order",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
                "order_id": self.order_id
            }
        }
        self.order_id = None

    def ate_dessert(self):
        return not self.will_have_dessert

    def ate_dinner(self):
        return not self.will_have_dinner

    def get_message(self):
        return self.return_message
