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
2. Start the dummy_data_wrapper:\
    * To start the old data_wrapper example: \
    `cd dummy_data_wrapper_old`\
       `AWS_ACCESS_KEY_ID=<id we provided> AWS_SECRET_ACCESS_KEY=<key we provided> docker-compose up`
    * To start the new data_wrapper example: \
    `cd dummy_data_wrapper`\
       `AWS_ACCESS_KEY_ID=<id we provided> AWS_SECRET_ACCESS_KEY=<key we provided> docker-compose up` 
3. Start nodeserver:\
    `cd ../nodeserver`\
    `SERVER_PORT=<port> SERVER_ADDRESS=<server address> PARTNER_NAME=<one of [NZZ,TAMEDIA]> CLIENT_SECRET=<secret> docker-compose up`\
**new: for custom data wrapper url define `DATA_WRAPPER_URL`. 
The script will do a get request on `{DATA_WRAPPER_URL}train` (old data wrapper), resp. `{DATA_WRAPPER_URL}get_dataset` (new data wrapper).\
`SERVER_PORT=50000 SERVER_ADDRESS=<server address> DATA_WRAPPER_URL="http://data_wrapper/" PARTNER_NAME=<one of [NZZ,TAMEDIA]> CLIENT_SECRET=<secret> docker-compose up`


### Client Interface
1. If not already running start data wrapper.
2. Start the client interface (Again you can set `DATA_WRAPPER_URL` to define custom data wrapper url):\
    `cd ../client_interface`\
    `PARTNER_NAME="INTERFACE" CLIENT_INTERFACE_PORT="50050" CLIENT_INTERFACE_SERVER_ADDRESS="client_interface"  SERVER="0" SERVER_PORT=50000 SERVER_ADDRESS=<server address> CLIENT_SECRET=<secret> docker-compose up`
4. See example/client_interface_example.py for how to use the client interface.

## Create your own data wrapper:
The node server expects the data wrapper to be callable (by get request) in the docker network `webnet` with name `data_wrapper` on port `80`. The specifications of the expected endpoints are below. You can set `DATA_WRAPPER_URL` to define custom data wrapper url.

See `dummy_data_wrapper/source_code` as an example. Feel free to add your wrapper to this repository.

You can test your wrapper by navigating to `data_wrapper_test` (resp. `data_wrapper_test_old` for the deprecated version) and running `docker-compose up` (if no errors occure then it's all good).

### Specification
**Function endoint**: `<data_wrapper_url>/get_available_datasets`: 
This endpoint returns all available datasets. One dataset can contain up to three subdatasets (splits) i.e. one for training, validation and test. These are callable with the endpoint below.
* _Input_: - 
* _Expection output_: List of metadata jsons for each available dataset . i.e:
  * ```json
    {"identifier":string,
    "description":string,
    "samples_num":[int,int,int], 
    "creation_date":"yyyy-MM-ddTHH:mm:ss.SSSZ",
    "features": [<feature1_json>,<feature2_json>,...]}
    ```
  * _identifier_: Unique and fixed identifier of the dataset. We will call function train with this identifier. 
  * _description_: Meta description of the dataset: Extraction Period, anything extraordinary about the data. 
  * _samples_num_: First integer is the number of samples in the training split of the dataset, the second the number of samples in the validation split and third the number of samples in the test split. This number can be 0 uif for example no test data is present. We will set the batch size/epochs/steps_per_epochs dependent on this number. 
  * _creation_date_: Creation date of the data set (ISO-8601) 
  * _features_: List containing metadata about each feature of the dataset. This is used on the client to add noise to the streamed data. You can create this list with the function `create_feature_metadata_json` we provide here the new data-wrapper dummy `data_wrapper_dummy/source_code/dummy_wrapper.py`. Each element of the list is a json looking as follows:
    ```json
    {"feature":" <feature_name>", 
    "categories": ["<name_of_class_1>","<name_of_class_2>",...], 
    "min_value": <min_value_of_feature_if_continuous>, 
    "max_value": <max_value_of_feature_if_continuous>,
    "q1": <first quartile>,
    "q3": <third quartile>
    "iqr_outliers": <number of 1.5-iqr outliers>
    "3std-percentage": <percentage of data in 3-std>
    "mean": <mean>
    "std":<standard deviation>
    
         }
    
    
    ```


**Function endoint**: `<data_wrapper_url>/get_dataset?identifier=<identifier>&type=<one of train|validation|test>`: 
This endoint streams the train, validation respectively test split of the requested dataset. We expect jsons streamed line by line.
* _Input_:  
    * _identifier_: Identifier of the dataset to return. (Identifier we received from get_available_data_sets)
    * _type_: Whether to return the train, validation or test set split.
* _Expection output_: Stream of random samples as jsons looking as follows:
  * ```json
    {"feature_1":" <feature_value_1>", 
    "feature_2":" <feature_value_2>", 
    ...,
    "label":<one_of_[0,1]>}

    ```
   

Please provide at least one dataset.

