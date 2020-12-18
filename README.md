# Restaurant Challenge

## Description

This is a streaming application using websocket to manage the backend of a restaurant game. The client will send the restaurants and customers statuses, and the websocket will take a decision about what the customer should do:

Each customers state can receive a limited list of events from the client:

* Waiting outside
    - please_sit
    - please_leave
* Waiting on full table
    - take_order
* Waiting for order
    - deliver_order
* Eating
    - N/A
* Waiting for the bill
    - bring_bill
* Left
    - N/A