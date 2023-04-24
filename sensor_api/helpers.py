import json

import pandas as pd


def clean_string_values(df):
    """Trim invisible symbols, replace empty strings and white spaces with NaN"""
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df = df.replace(['', ' '], None)
    return df


def get_sensors_df(data_path: str) -> pd.DataFrame:
    with open(data_path, 'r', encoding='utf-8') as f:
        sensors_json = json.load(f)
    sensors_list = []
    for sensor_id, sensor_info in sensors_json.items():
        metrics = sensor_info.pop('metrics')
        for metric_id, metric_data in metrics.items():
            row = {
                'sensor_id': sensor_id,
                'metric_id': metric_id,
                **metric_data,
                **sensor_info,
            }
            sensors_list.append(row)
    sensors_df = pd.json_normalize(sensors_list)
    sensors_df = sensors_df.drop(columns=['t'])
    sensors_df = clean_string_values(sensors_df)
    sensors_df = sensors_df.rename(columns={
        'type': 'sensor_type',
        'variant': 'sensor_version',
        'name': 'sensor_name',
    })
    sensors_df.loc[sensors_df['sensor_name'].isna(), 'sensor_name'] = 'id' + sensors_df['sensor_id']
    return sensors_df


def get_metrics_df(data_path: str) -> pd.DataFrame:
    with open(data_path, 'r', encoding='utf-8') as f:
        metrics_json = json.load(f)
    metrics_json = metrics_json['data']['items']

    metrics_data = []
    for metric in metrics_json:
        row = {**metric}
        metrics_data.append(row)
    metrics_df = pd.json_normalize(metrics_data, meta=['id', 'name'], record_path=['units'], record_prefix='unit_')
    metrics_df = metrics_df.drop(columns=['unit_precision'])
    metrics_df = metrics_df.rename(columns={
        'id': 'metric_id',
        'name': 'metric_name'
    })
    metrics_df = metrics_df[metrics_df.unit_selected == True]
    return metrics_df


def get_types_df(data_path: str) -> pd.DataFrame:
    with open(data_path, 'r', encoding='utf-8') as f:
        types_json = json.load(f)
    types_list = []
    for sensor_type, sensor_info in types_json.items():
        for sensor_version, sensor_version_name in sensor_info.items():
            row = {
                'sensor_type': sensor_type,
                'sensor_version': sensor_version,
                'sensor_type_version_name': sensor_version_name['name']
            }
            types_list.append(row)
    types_df = pd.json_normalize(types_list)
    types_df['sensor_type'] = types_df['sensor_type'].astype('int64')
    types_df['sensor_version'] = types_df['sensor_version'].astype('int64')
    return types_df
