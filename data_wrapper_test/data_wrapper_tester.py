import requests
import logging
import json
import os

logging.basicConfig(level=int(os.getenv('LOGGING_LEVEL', 20)))

logging.info("Fetching metadata json from get_available_datasets...")
response = requests.get(f"{os.getenv('DATA_WRAPPER_URL', 'http://data_wrapper_old/')}get_available_datasets")

assert len(response.json()) > 0
for dataset_metadata_json in response.json():
    assert "identifier" in dataset_metadata_json
    assert "description" in dataset_metadata_json
    assert "samples_num" in dataset_metadata_json
    assert len(dataset_metadata_json["samples_num"]) == 3
    assert "creation_date" in dataset_metadata_json
    assert "features" in dataset_metadata_json
    assert len(dataset_metadata_json["features"]) > 0
    for feature in dataset_metadata_json["features"]:
        assert "feature" in feature
        assert "type" in feature
        assert feature["type"] in ['categorical', 'continuous']
        if feature["type"] == 'categorical':
            assert "categories" in feature
            assert len(feature["categories"]) > 0
        elif feature["type"] == 'continuous':
            assert "min_value" in feature
            assert "max_value" in feature
            assert "q1" in feature
            assert "q3" in feature
            assert "iqr_outliers" in feature
            assert "3std-percentage" in feature
            assert "mean" in feature
            assert "std" in feature

logging.info("Response looks good!")

logging.info(f"Fetching training dataset with identifier {dataset_metadata_json['identifier']}...")

with requests.get(f"{os.getenv('DATA_WRAPPER_URL', 'http://data_wrapper/')}"
                  f"get_dataset?identifier={dataset_metadata_json['identifier']}&type=train", stream=True) as response:
    logging.info(f"Data incoming. Checking first 1000 rows...")
    i = 0
    for chunk in response.iter_lines():

        row = json.loads(chunk)

        for feature in dataset_metadata_json["features"]:
            assert feature["feature"] in row
            if feature["type"] == 'categorical':
                if row[feature["feature"]] not in feature["categories"]:
                    logging.warning(f'feature {row[feature["feature"]]} is not in feature meta '
                                    f'description ({feature["categories"]})')
            elif feature["type"] == 'continuous':
                if row[feature["feature"]] < feature["min_value"]:
                    logging.warning(f'feature {row[feature["feature"]]} is smaller than lowerbond in feature meta '
                                    f'description ({feature["min_value"]})')
                if row[feature["feature"]] > feature["max_value"]:
                    logging.warning(f'feature {row[feature["feature"]]} is larger than upperbound in feature meta '
                                    f'description ({feature["max_value"]})')

        if i >= 1000:
            break
        i = i + 1
logging.info("Looks good!")

