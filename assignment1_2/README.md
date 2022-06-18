# microservices_redis_streams
Scope of implementation: order capturing service, inventory service and account service.
Framework used: Flask
Choice of asynchronous communication model: Redis / Redis Streams
API Documentation directory: gateway_api/swagger.yaml

## How to use
### Requirement
Docker Engine, Docker Compose and Python3 are required for this project to work.
### Steps to use
1. In project root, start the application with:
``docker-compose up``
2. On a separate terminal, flush all data in Redis:
``docker exec -it microservicesredisstreams_redis_1 redis-cli FLUSHALL``
3. To display domain model datas. On a browser or curl, 
``http://localhost:5000/report``

### Test Calls
Run a http post call to place an order:

Successful order process:
``curl -X POST -H "Content-Type: application/json" \
    -d '{"product_ids": ["201", "204"], "customer_id": "101"}' \
    http://localhost:5000/order
	``

Insufficient fund order process:
``curl -X POST -H "Content-Type: application/json" \
    -d '{"product_ids": ["201","204", "205"], "customer_id": "101"}' \
    http://localhost:5000/order
	``

Out of stock process:
``curl -X POST -H "Content-Type: application/json" \
    -d '{"product_ids": ["201","201", "201", "201", "201", "201"], "customer_id": "101"}' \
    http://localhost:5000/order
	``

## Logging
When application is docker compose up, the logs will be output to stdout or stderr for simplicity.

## Project Details
The domain models for the ordering system application consists of the following entities:

1. Orders
2. Inventory
3. Accounts

Services consists of the following:

1. gateway_api: responsible for all api management
2. msg_service: responsible for notification and messages to client
3. order_service: responsible for order
4. inventory_service: responsible for inventory warehousing
5. account: responsible for accounting and customer relation

RESP HTTP connection exposure are only between gateway_api and order_service. However, the other services (including order_service) uses RESP (Redis Serialization Protocol) via a subscribe handler.
Each event trigger will perform xadd to Redis Streams which will notify all subscribed (xread) to the streams.


## Project architecture improvement points
1. Currently, the data is already segegrated and not related in anyway within it's own domain but it is in a situated in a shared database, Redis. We could futher isolate the data within each service by having it's own database. This enables ease of development between teams in the maintainability perspective. On the other hand, the performance is greatly improved as the database are local to it's own instance.
2. As for the Redis Streams, it is using XREAD where all service types can only be managed with 1 service instance each. This is due to the fact that we will run into duplicated task if more than one service instance of the same type is running simultaneously. This could further be enhanced to use consumer groups for each service type where we could scale by adding more instances to the group and Redis have XGROUPREAD call that could read pending stream list. Once an event is process completely, sending an ACK call will remove the event from the pending stream list of the group. Hence, solving duplicated event processing.
3. XGROUPREAD + ACK call gives a high reliability within the consumer groups. This is due to the fact that in the case if any of the instance encounter disruption or error; if no ACK call are issued, the event will still remain in the pending list queue for the next available instance to pick up.
4. In security view, the exposed API are not protected by any form of AUTH. This could further be enhance with either OAUTH2 or authentication server implementation. As for the calls between the service instance are using Redis RESP and these services can be located in an internal environment without exposing to the public. Redis could futher enable TLS connection to encrypt communication.
