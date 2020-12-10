from .exceptions import NoTablesAvailable, TableNotAvailable, LineExceededSize
from .customer import Customer
from .table import Table


class Restaurant:

    def __init__(self, id: str = None, state: int = None, tables: int = 100,
                 dinner_prepare_time: int = None,
                 dessert_prepare_time: int = None,
                 line_number: int = None) -> None:
        self.id = id
        self.state = state
        self.number_of_tables = tables
        self.dinner_prepare_time = dinner_prepare_time
        self.dessert_prepare_time = dessert_prepare_time
        self.line_number = line_number
        self.line = []
        self.all_customers = []
        self.tables = self.setup_tables()

    def setup_tables(self) -> dict:
        return {i: None for i in range(0, self.number_of_tables)}

    def get_table(self, table_id: int) -> Table:
        return self.tables[table_id]

    def get_customer(self, customer_id: str) -> Customer:
        return next(filter(
            lambda cs: cs.id == customer_id, self.all_customers
        ))

    def please_sit(self, customer: Customer,
                   table_id: int) -> None:
        table = self.tables.get(table_id)
        if len(self.get_occuppied_tables()) >= self.number_of_tables:
            raise NoTablesAvailable()
        elif table is not None and not table.table_closed:
            sit_together = table.customers[0].sit_together
            if customer.id not in sit_together:
                raise TableNotAvailable()

        table = table or Table(table_id)
        self.tables[table_id] = table
        self.line.remove(customer)
        table.add_customer(customer)

    def take_order(self, table_id: int, customer: Customer,
                   order_id: int) -> None:
        self.get_table(table_id).take_order(customer, order_id)

    def deliver_order(self, customer: Customer, table_id: int, order_id: int):
        self.get_table(table_id).deliver_order(order_id, customer)

    def bring_bill(self, customer: Customer) -> None:
        customer.pay_bills()

    def please_leave(self, customer: Customer) -> None:
        if customer.table is not None:
            table = self.get_table(customer.table)
            table.remove_customer(customer)
            if table.is_empty():
                self.tables[customer.table] = None
        customer.leave()

    def get_in_line(self, customer: Customer):
        if self.line_number <= len(self.line):
            raise LineExceededSize()
        self.line.append(customer)
        self.all_customers.append(customer)

    def get_occuppied_tables(self):
        return {id: table for id, table in self.tables.items()
                if table is not None}

    def serialize(self):
        return {
            "id": self.id,
            "state": self.state,
            "number_of_tables": self.number_of_tables,
            "dinner_prepare_time": self.dinner_prepare_time,
            "dessert_prepare_time": self.dessert_prepare_time,
            "line_number": self.line_number,
            "line": [str(customer) for customer in self.line],
            "tables": [tb.serialize() for tb in
                       self.get_occuppied_tables().values()],
        }
