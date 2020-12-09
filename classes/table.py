from typing import List
from .enums import OrderType
from .customer import Customer
from .exceptions import OrderDeliveredWrong


class Table:
    customers: List[Customer] = []
    orders: List[OrderType] = []

    def __init__(self, id, size=4):
        self.id = id
        self.size = size

    def add_customer(self, customer: Customer) -> int:
        self.customers.append(customer)

    def take_order(self, customer: Customer, order_id: int) -> None:
        customer.order(order_id)
        self.orders.append(OrderType(order_id))

    def deliver_order(self, order_id: int) -> None:
        order = OrderType(order_id)
        if order in self.orders:
            self.orders.remove(order)
        else:
            raise OrderDeliveredWrong(order, self.id)

    def clean(self, paid_bills=False) -> None:
        for customer in self.customers:
            if paid_bills:
                customer.pay_bills()
            customer.leave()

    def serialize(self) -> dict:
        return {
            self.id: [str(cs) for cs in self.customers]
        }
