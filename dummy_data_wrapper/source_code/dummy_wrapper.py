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
import random

app = Flask(__name__)

s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), region_name='eu-central-1')

import codecs


def get_s3_file(client, url):
    obj = client.get_object(Bucket='federated-learning-dummy-data', Key=url)
    body = obj['Body']

    data = []
    i = 0
    for ln in codecs.getreader('utf-8')(body):
        if i < 100000:
            data.append(ln)

    return data


# Fetch Data
train = get_s3_file(s3, 'new/train.json')
train, validation = train[:int(len(train) * 0.9)], train[int(len(train) * 0.9):]

test = get_s3_file(s3, 'new/test.json')


# Route to stream the training data
@app.route('/train')
def stream_train_data():
    random.shuffle(train)

    def generate():
        for row in train:
            yield row + '\n'

    return Response(generate(), mimetype='text/json')


@app.route('/validation')
def stream_validation_data():
    def generate():
        for row in validation:
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
    app.run(host='0.0.0.0')
