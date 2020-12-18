import asyncio
import json
import logging
import websockets

from classes.restaurant import Restaurant
from classes.customer import Customer
from classes.exceptions import LineExceededSize
from classes.enums import State


logging.basicConfig()

RESTAURANTS = {}
CUSTOMERS = {}


async def game(websocket, path):
    running = True
    while running:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            payload = data.get('payload')
            if data.get('name') == 'restaurant_update':
                if payload['id'] in RESTAURANTS:
                    restaurant = RESTAURANTS[payload['id']]
                else:
                    restaurant = Restaurant()
                restaurant.update(**payload)
                RESTAURANTS[payload['id']] = restaurant
            elif data.get('name') == 'customer_update':
                restaurant_id = payload.get('restaurant_id')
                if restaurant_id is None:
                    # Get most empty restaurant
                    restaurant_id = list(RESTAURANTS.keys())[0]
                restaurant = RESTAURANTS.get(restaurant_id)
                state = payload['state']
                if payload['id'] in CUSTOMERS:
                    customer = CUSTOMERS[payload['id']]
                else:
                    customer = Customer()
                customer.update(**payload)
                CUSTOMERS[customer.id] = customer
                if state == State.left.value:
                    del CUSTOMERS[customer.id]
                if customer.get_message():
                    if customer.get_message() == '#':
                        running = False
                        break
                    await websocket.send(json.dumps(
                        customer.get_message()
                    ))
        except LineExceededSize:
            await websocket.send('#')
        except Exception as e:
            print(e)


start_server = websockets.serve(game, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
