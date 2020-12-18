from typing import List, Any
from datetime import datetime

from .enums import State, OrderType
from .exceptions import LineExceededSize


class Customer:

    def __init__(self, restaurant: Any):
        self.restaurant = restaurant
        self.satisfied = True

    def update(self, **kwargs) -> None:
        state = kwargs.pop('state')
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.set_state(state)

    def set_state(self, value: int) -> None:
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
                    try:
                        self.restaurant.add_to_line(self)
                    except LineExceededSize:
                        self.return_message = '#'
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
                        # self.return_message = '#'
                        return
                self.return_message = {
                    "name": "bring_bill",
                    "payload": {
                        "customer_id": self.id,
                        "table_id": self.table
                    }
                }
                if self.restaurant.had_all_customers_on_table_done_eating():
                    customers = self.restaurant.tables[self.table]
                    for customer in customers:
                        customer.please_leave()
            elif value == State.left.value:
                table = self.table
                self.restaurant.remove_customer(self)
                if table:
                    self.restaurant.ask_next_client_to_sit()

    def please_sit(self, table_id: int) -> None:
        self.table = table_id
        self.return_message = {
            "name": "please_sit",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
            }
        }

    def please_leave(self) -> None:
        if self.table:
            self.restaurant.ask_next_client_to_sit()
        self.return_message = {
            "name": "please_leave",
            "payload": {
                "customer_id": self.id,
            }
        }

    def take_order(self) -> None:
        self.return_message = {
            "name": "take_order",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
                "order_id": self.order_id
            }
        }

    def deliver_order(self) -> None:
        self.return_message = {
            "name": "deliver_order",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
                "order_id": self.order_id
            }
        }
        self.order_id = None

    def ate_dessert(self) -> bool:
        return not self.will_have_dessert

    def ate_dinner(self) -> bool:
        return not self.will_have_dinner

    def get_message(self) -> str:
        return self.return_message
