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

