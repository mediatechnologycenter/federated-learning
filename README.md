Requirements:
- docker: 18 or higher
- docker-compose: 1.18 or higher

Installation Node_worker:
1. clone git repo: git clone https://github.com/MTC-ETH/Federated-Learning
2. navigate to dummy_data_wrapper: cd dummy_data_wrapper
3. run docker compose file with environment variables:
    -	AWS_ACCESS_KEY_ID=<id we provided> AWS_SECRET_ACCESS_KEY=<key we provided> LOGGING_LEVEL=20 docker-compose up 
4. navigate to nodeserver: cd ../nodeserver
5. run docker compose file with environment variables:
	-	SERVER_ADDRESS=<server address> PARTNER_NAME=<one of [NZZ,TAMEDIA]> LOGGING_LEVEL=20 docker-compose up 
