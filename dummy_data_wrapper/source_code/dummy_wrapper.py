# Copyright 2019 MTC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Dummy Data Wrapper to stream training data to the node client

This scripts provides an endpoint callable by all containers in the docker network "webnet" via tcp.
On startup, it fetches the dummy train & test data from an S3 bucket and transforms it into jsonlines.
The the callable routes '/train' & '/test' stream the fetched data line by line (i.e. json by json).
"""

from flask import Response, Flask
import json
import os
import boto3
import io

app = Flask(__name__)

s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), region_name='eu-central-1')



def get_s3_file(client, url):
    bytes_buffer = io.BytesIO()
    client.download_fileobj('federated-learning-dummy-data', url, Fileobj=bytes_buffer)
    byte_value = bytes_buffer.getvalue()
    return json.loads(byte_value.decode())


# Fetch data from s3 and transform to jsonlines
def get_data():
    x_train = get_s3_file(s3, 'new/x_train.json')
    y_train = get_s3_file(s3, 'new/y_train.json')
    train = [x_train[i] + [y_train[i]] for i in range(len(y_train))]
    for i in range(len(train)):
        train[i] = json.dumps({f"column{k}": value for k, value in enumerate(train[i])})

    x_test = get_s3_file(s3, 'new/x_test.json')
    y_test = get_s3_file(s3, 'new/y_test.json')
    test = [x_test[i] + [y_test[i]] for i in range(len(y_test))]
    for i in range(len(test)):
        test[i] = json.dumps({f"column{k}": value for k, value in enumerate(test[i])})
    return train, test


# Fetch Data
train, test = get_data()


# Route to stream the training data
@app.route('/train')
def stream_train_data():
    def generate():
        for row in train:
            yield row + '\n'

    return Response(generate(), mimetype='text/json')


# Route to stream the test data
@app.route('/test')
def stream_test_data():
    def generate():
        for row in test:
            yield row + '\n'
    return Response(generate(), mimetype='text/json')


if __name__ == '__main__':
    app.run()
