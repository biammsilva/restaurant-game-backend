class NoTablesAvailable(Exception):
    def __init__(self):
        super().__init__('No Tables available now')


class TableNotAvailable(Exception):
    def __init__(self):
        super().__init__('This table is not available')


class LineExceededSize(Exception):
    def __init__(self):
        super().__init__('The line exceeded maximum size')
