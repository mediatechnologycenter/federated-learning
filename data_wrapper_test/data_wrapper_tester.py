import requests
import logging
import json
import os

logging.basicConfig(
    level=int(os.getenv('LOGGING_LEVEL', 20)),
    handlers=[logging.StreamHandler()])

logging.info("Fetching first responses of /test and /train stream...")
for url in ['test', 'train']:
    with requests.get(f"http://data_wrapper/{url}", stream=True) as response:
        logging.info("Connection established!")

        logging.info(f"Data incoming from {url}:")
        for chunk in response.iter_lines():
            logging.info(json.loads(chunk))
            break
logging.info("Looks good!")
