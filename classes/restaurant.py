from typing import Dict, List
from .customer import Customer


class Restaurant:

    def __init__(self):
        self.tables_list: Dict[int, List[Customer]] = {}
        self.customers: Dict[str, Customer] = {}

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'tables' in kwargs:
            self.tables_list = self.setup_tables()

    def setup_tables(self) -> dict:
        return {i: [] for i in range(0, self.tables)}

    def get_empty_table(self) -> dict:
        return [id for id, customers in self.tables_list.items()
                if not customers]

    def find_table(self, customer: Customer) -> int:
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
        if customer.table:
            self.tables_list[customer.table].remove(customer)
        del self.customers[customer.id]
