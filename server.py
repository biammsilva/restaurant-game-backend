import asyncio
import json
import logging
import websockets

from classes.restaurant import Restaurant
from classes.customer import Customer
from classes.enums import State


logging.basicConfig()

RESTAURANTS = {}
CUSTOMERS = {}


async def game(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            payload = data.get('payload')
            if data.get('name') == 'restaurant_update':
                restaurant = Restaurant()
                restaurant.update(**payload)
                RESTAURANTS[payload['id']] = restaurant
                # await websocket.send(json.dumps(
                #     restaurant.get_message()
                # ))
            elif data.get('name') == 'customer_update':
                if payload['id'] in CUSTOMERS:
                    customer = CUSTOMERS[payload['id']]
                else:
                    customer = Customer()
                restaurant_id = payload.get('restaurant_id')
                if restaurant_id is None:
                    # Get most empty restaurant
                    restaurant_id = list(RESTAURANTS.keys())[0]
                customer.restaurant = RESTAURANTS.get(restaurant_id)
                customer.update(**payload)
                CUSTOMERS[payload['id']] = customer
                # if customer.state == State.left:
                #     del CUSTOMERS[customer.id]
                if customer.get_message():
                    await websocket.send(json.dumps(
                        customer.get_message()
                    ))
        except Exception as e:
            print(e)


start_server = websockets.serve(game, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
