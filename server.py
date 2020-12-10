import asyncio
import json
import logging
import websockets

from classes.restaurant import Restaurant
from classes.customer import Customer


logging.basicConfig()

RESTAURANTS = {}
CUSTOMERS = {}


def restaurant_update(payload: dict):
    restaurant = Restaurant(**payload)
    RESTAURANTS[payload['id']] = restaurant
    return restaurant


def get_restaurant(restaurant_id: str):
    return RESTAURANTS.get(restaurant_id)


async def counter(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            # data = json.loads(message)
            for message in message.split('___'):
                data = json.loads(message)
                payload = data.get('payload')
                if data.get('name') == 'restaurant_update':
                    restaurant = restaurant_update(payload)
                else:
                    if data.get('name') == 'customer_update':
                        customer = Customer(**payload)
                        if payload.get('restaurant_id') is None:
                            restaurant = get_restaurant(
                                list(RESTAURANTS.keys())[0]
                            )
                            customer.restaurant_id = restaurant.id
                        else:
                            restaurant = get_restaurant(
                                payload['restaurant_id']
                            )
                        CUSTOMERS[payload['id']] = customer
                        restaurant.get_in_line(customer)
                    else:
                        customer = CUSTOMERS[payload['customer_id']]
                        restaurant = get_restaurant(customer.restaurant_id)

                        if data.get('name') == 'please_sit':
                            restaurant.please_sit(customer, payload['table_id'])
                        elif data.get('name') == 'take_order':
                            restaurant.take_order(
                                payload['table_id'],
                                customer,
                                payload['order_id']
                            )
                        elif data.get('name') == 'deliver_order':
                            restaurant.deliver_order(
                                customer,
                                payload['table_id'],
                                payload['order_id']
                            )
                        elif data.get('name') == 'bring_bill':
                            restaurant.bring_bill(customer)
                        elif data.get('name') == 'please_leave':
                            restaurant.please_leave(customer)
                await websocket.send(json.dumps(
                    restaurant.serialize()
                ))
        except Exception as e:
            print(e)


start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
