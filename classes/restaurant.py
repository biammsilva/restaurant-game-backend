from typing import List

from .customer import Customer


class Table:
    size = 4
    customers: List(Customer) = []

    def add_customer(self, customers: List(Customer), bulk=False) -> int:
        if bulk:
            self.customers = customers
        else:
            self.customers += customers


class Restaurant:

    def __init__(self, id: str, state: int, tables: int,
                 dinner_prepare_time: int, dessert_prepare_time: int,
                 line_number: int) -> None:
        self.id = id
        self.state = state
        self.number_of_tables = tables
        self.dinner_prepare_time = dinner_prepare_time
        self.dessert_prepare_time = dessert_prepare_time
        self.line_number = line_number
        self.tables = {}

    def add_costumers_to_table(self, customers: List(Customer),
                               table_id: int) -> None:
        table = Table()
        table.add_customer(customers, bulk=True)
        self.tables[table_id] = table
