from typing import List
from .enums import OrderType
from .customer import Customer
from .exceptions import OrderDeliveredWrong


class Table:

    def __init__(self, id, size=4):
        self.id = id
        self.size = size
        self.customers: List[Customer] = []
        self.orders: List[OrderType] = []
        self.table_closed = False

    def add_customer(self, customer: Customer) -> int:
        self.customers.append(customer)
        customer.sit(self.id)

    def remove_customer(self, customer: Customer) -> int:
        self.customers.remove(customer)

    def take_order(self, customer: Customer, order_id: int) -> None:
        order = OrderType(order_id)
        customer.submit_order(order)
        self.orders.append(order)
        self.table_closed = True

    def deliver_order(self, order_id: int, customer: Customer) -> None:
        order = OrderType(order_id)
        customer.get_order(order)
        if order in self.orders:
            self.orders.remove(order)
        else:
            raise OrderDeliveredWrong(order, self.id)

    def pay_bills(self) -> None:
        for customer in self.customers:
            customer.pay_bills()

    def clean(self) -> None:
        for customer in self.customers:
            customer.leave()

    def is_empty(self) -> bool:
        return len(self.customers) == 0

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "customers": [str(cs) for cs in self.customers],
            "orders": [order.name for order in self.orders]
        }
