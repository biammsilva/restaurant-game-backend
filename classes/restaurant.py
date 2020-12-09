from typing import List

from .exceptions import NoTablesAvailable, TableNotAvailable, LineExceededSize
from .customer import Customer


class Table:
    size = 4
    customers: List(Customer) = []

    def add_customer(self, customers: List(Customer), bulk=False) -> int:
        if bulk:
            self.customers = customers
        else:
            self.customers += customers

    def receive_order(self, customer: Customer, order_id: int) -> None:
        customer.order(order_id)

    def clean(self, paid_bills=False) -> None:
        for customer in self.customers:
            if paid_bills:
                customer.pay_bills()
            customer.leave()


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
        self.line = []
        self.tables = self.setup_tables()

    def setup_tables(self) -> dict:
        pass

    def get_table(self, table_id: int) -> Table:
        return self.tables[table_id]

    def add_costumers_to_table(self, customers: List(Customer),
                               table_id: int) -> None:
        if len(self.tables) >= self.number_of_tables:
            raise NoTablesAvailable()
        elif self.tables.get(table_id) is not None:
            raise TableNotAvailable()

        table = Table()
        table.add_customer(customers, bulk=True)
        self.tables[table_id] = table

    def deliver_order(self, table_id: int, customer: Customer,
                      order_id: int) -> None:
        self.get_table(table_id).receive_order(customer, order_id)

    def bring_bill(self, table_id: int) -> None:
        table = self.get_table(table_id)
        table.clean(paid_bills=True)
        self.tables[table_id] = None

    def please_leave(self, customer: Customer) -> None:
        customer.leave()

    def wait_in_the_line(self, customer: Customer):
        if self.line_number >= len(self.line):
            raise LineExceededSize()
        self.line.append(customer)
