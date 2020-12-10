from .enums import State, OrderType


class Customer:

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key == 'state':
                continue
            setattr(self, key, value)
        self.state = kwargs['state']

    @property
    def state(self):
        return self.state

    def please_sit(self):
        return {
            "name": "please_sit",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
            }
        }

    def please_leave(self):
        return {
            "name": "please_leave",
            "payload": {
                "customer_id": self.id,
            }
        }

    def take_order(self):
        return {
            "name": "take_order",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
                "order_id": self.order_id
            }
        }

    def deliver_order(self):
        message = {
            "name": "deliver_order",
            "payload": {
                "customer_id": self.id,
                "table_id": self.table,
                "order_id": self.order_id
            }
        }
        self.order_id = None
        return message

    @state.setter
    def state(self, value):
        if value == State.waiting_outside.value:
            table = self.restaurant.find_table(self)
            if table is not None:
                self.table = table
                self.return_message = self.please_sit()
            else:
                self.return_message = self.please_leave()
        elif value == State.waiting_on_full_table.value:
            if self.will_have_dinner:
                self.order_id = OrderType.dinner.value
                self.will_have_dinner = False
                self.return_message = self.take_order()
            elif self.will_have_dessert:
                self.order_id = OrderType.dessert.value
                self.will_have_dessert = False
                self.return_message = self.take_order()
            else:
                self.return_message = self.please_leave()
        elif value == State.waiting_for_order.value:
            if self.order_id is not None:
                self.return_message = self.deliver_order()
        elif value == State.eating.value:
            self.return_message = None
            pass
        elif value == State.waiting_bill.value:
            self.return_message = {
                "name": "bring_bill",
                "payload": {
                    "customer_id": self.id,
                    "table_id": self.table
                }
            }
        elif value == State.left.value:
            self.restaurant.remove_customer(self)

    def get_message(self):
        return self.return_message
