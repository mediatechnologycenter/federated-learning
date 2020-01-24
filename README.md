# Node server for Partners 

This repository contains the docker-compose files to set up a node server on our partners side.

## Requirements:
### Software:
- docker: 18 or higher
- docker-compose: 1.18 or higher
### Hardware:
- 16 Gib Memory
- 4 CPUs
- Internet Access



## Installation:
1. Clone git repo:\
`git clone https://github.com/MTC-ETH/Federated-Learning`
2. Navigate to dummy_data_wrapper:\
`cd dummy_data_wrapper`
3. Run docker compose file with environment variables:\
`AWS_ACCESS_KEY_ID=<id we provided> AWS_SECRET_ACCESS_KEY=<key we provided> docker-compose up` 
4. Navigate to nodeserver:\
`cd ../nodeserver`
5. Run docker compose file with environment variables:\
`SERVER_PORT=50000 SERVER_ADDRESS=<server address> PARTNER_NAME=<one of [NZZ,TAMEDIA]> CLIENT_SECRET=<secret> docker-compose up`\
**new: for custom data wrapper url define `DATA_WRAPPER_URL`. The script will do a get request on `{DATA_WRAPPER_URL}train`, resp. `{DATA_WRAPPER_URL}test`.\
`SERVER_PORT=50000 SERVER_ADDRESS=<server address> DATA_WRAPPER_URL="http://data_wrapper/" PARTNER_NAME=<one of [NZZ,TAMEDIA]> CLIENT_SECRET=<secret> docker-compose up`


### Client Interface
1. If not already running start data wrapper:
`AWS_ACCESS_KEY_ID=<id we provided> AWS_SECRET_ACCESS_KEY=<key we provided> docker-compose up` 
2. Navigate to client_interface:\
`cd ../client_interface`
3. Run client_interface docker-compose (Again you can set `DATA_WRAPPER_URL` to define custom data wrapper url):
`PARTNER_NAME="INTERFACE" CLIENT_INTERFACE_PORT="50050" CLIENT_INTERFACE_SERVER_ADDRESS="client_interface"  SERVER="0" SERVER_PORT=50000 SERVER_ADDRESS=<server address> CLIENT_SECRET=<secret> docker-compose up`
4. See example/client_interface_example.py for how to use the client interface.

## Create your own data wrapper:
The current node server expects the data wrapper to be callable in the docker network `webnet` with name `data_wrapper` on port `80` at route `/train` resp. `/test`. The server expects to get a stream of jsonlines i.e. each line is a valid json.
See `dummy_data_wrapper/source_code` as an example. Feel free to add your wrapper to this repository.

You can test your wrapper by navigating to `data_wrapper_test` and running `docker-compose up` (if no errors occure then it's all good). Again you can set `DATA_WRAPPER_URL` to define custom data wrapper url.
