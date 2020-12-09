class NoTablesAvailable(Exception):
    def __init__(self):
        super().__init__('No Tables available now')


class TableNotAvailable(Exception):
    def __init__(self):
        super().__init__('This table is not available')


class LineExceededSize(Exception):
    def __init__(self):
        super().__init__('The line exceeded maximum size')


class OrderDeliveredWrong(Exception):
    def __init__(self, table_id, order):
        super().__init__(f'The order {order} do not \
                         belong to the table {table_id}')
