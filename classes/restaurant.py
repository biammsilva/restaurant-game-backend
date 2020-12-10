from typing import Dict, List, Optional
from datetime import datetime

from .customer import Customer
from .exceptions import LineExceededSize
from .enums import OrderType


class Restaurant:

    def __init__(self):
        self.tables_list: Dict[int, List[Customer]] = {}
        self.customers: Dict[str, Customer] = {}
        self.line: List[Customer] = set()
        self.tables = 0

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'tables' in kwargs:
            self.tables_list = self.setup_tables()

    def setup_tables(self) -> dict:
        return {i: [] for i in range(0, self.tables)}

    def has_empty_tables(self) -> bool:
        return len(self.get_empty_table()) > 0

    def get_empty_table(self) -> dict:
        return [id for id, customers in self.tables_list.items()
                if not customers]

    def find_table(self, customer: Customer) -> Optional[int]:
        if hasattr(customer, 'sit_together') and customer.sit_together:
            customers = [self.customers[customer_id]
                         for customer_id in customer.sit_together
                         if customer_id in self.customers.keys()]
            if customers:
                self.customers[customer.id] = customer
                self.tables_list[customers[0].table].append(customer)
                return customers[0].table
        empty_tables = self.get_empty_table()
        if empty_tables:
            self.customers[customer.id] = customer
            self.tables_list[empty_tables[0]].append(customer)
            return empty_tables[0]

    def remove_customer(self, customer: Customer) -> None:
        if customer.table is not None:
            self.tables_list[customer.table].remove(customer)
        del self.customers[customer.id]

    def add_to_line(self, customer: Customer) -> None:
        if len(self.line) >= self.line_number:
            raise LineExceededSize()
        self.line.add(customer)

    def next_in_line(self) -> Optional[Customer]:
        sorted_line = sorted(
            self.line, key=lambda cs: cs.stress_level, reverse=True
        )
        if sorted_line:
            return sorted_line[0]

    def is_order_time_ok(self, last_order_time, order):
        if order == OrderType.dinner.value:
            comparator = self.dinner_prepare_time
        if order == OrderType.dessert.value:
            comparator = self.dessert_prepare_time
        return (datetime.now - last_order_time).total_seconds() <= comparator
