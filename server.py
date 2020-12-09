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
        message = await websocket.recv()
        data = json.loads(message)
        payload = data.get('payload')
        if data.get('name') == 'restaurant_update':
            restaurant = restaurant_update(payload)
            await websocket.send(json.dumps(
                restaurant.serialize()
            ))
        else:
            if data.get('name') == 'customer_update':
                customer = Customer(**payload)
                if payload.get('restaurant_id') is None:
                    restaurant = get_restaurant(list(RESTAURANTS.keys())[0])
                    customer.restaurant_id = restaurant.id
                else:
                    restaurant = get_restaurant(payload['restaurant_id'])
                CUSTOMERS[payload['id']] = customer
                restaurant.get_in_line(customer)
                await websocket.send(json.dumps(
                    restaurant.serialize()
                ))
            elif data.get('name') == 'please_sit':
                customer = CUSTOMERS[payload['customer_id']]
                restaurant = get_restaurant(customer.restaurant_id)
                restaurant.please_sit(
                    payload.get('customer_id'),
                    payload.get('table_id')
                )
                await websocket.send(json.dumps(
                    restaurant.serialize()
                ))

start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
