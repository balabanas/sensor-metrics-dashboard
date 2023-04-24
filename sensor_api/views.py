import json

import pandas as pd
from django.http import JsonResponse

from smd.settings import *
from .helpers import clean_string_values, get_sensors_df, get_metrics_df, get_types_df

DATA_PATH_SENSORS = 'data/sensors.json'
DATA_PATH_METRICS = 'data/metrics.json'
DATA_PATH_TYPES = 'data/sensorTypes.json'


def sensors(request):
    """Read json files and prepare JSON response"""

    # sensors.json
    sensors_df = get_sensors_df(DATA_PATH_SENSORS)

    # metrics.json
    metrics_df = get_metrics_df(DATA_PATH_METRICS)

    # sensorTypes.json
    types_df = get_types_df(DATA_PATH_TYPES)

    # join sensors with types
    sensors_types_df = pd.merge(sensors_df, types_df, how='left', on=['sensor_type', 'sensor_version'])
    sensors_types_df['sensor_type_version_name'] = sensors_types_df['sensor_type_version_name'].fillna(value='n/a')

    # join metrics from sensors with units' names
    sensors_metrics_types_df = pd.merge(sensors_types_df, metrics_df, on='metric_id')

    # name and keep only necessary columns
    sensors_metrics_types_df['metric_view'] = \
        sensors_metrics_types_df['metric_name'] + ' ' + sensors_metrics_types_df['unit_name']
    sensors_metrics_types_df = sensors_metrics_types_df.loc[:, ['sensor_id',
                                                                'v',
                                                                'sensor_name',
                                                                'sensor_type_version_name',
                                                                'metric_view']]

    # transform and export to JSON
    sensors_metrics_types_df = sensors_metrics_types_df.pivot(
        index=['sensor_id', 'sensor_name', 'sensor_type_version_name'], columns=['metric_view'], values='v')
    sensors_metrics_types_df = sensors_metrics_types_df.reset_index()
    sensors_metrics_types_df = sensors_metrics_types_df.drop(columns=['sensor_id'])
    # create separate columns, metrics, types lists to ease data manipulation in frontend
    columns = sensors_metrics_types_df.columns.to_list()
    metrics = [x for x in columns if x not in ['sensor_name', 'sensor_type_version_name']]
    types = list(sensors_metrics_types_df['sensor_type_version_name'].unique())
    types.insert(0, "ALL")  # put ALL at the top of the list
    try:  # move n/a to the end if exists
        types.remove('n/a')
        types.append('n/a')
    except ValueError:
        pass
    response = JsonResponse({"data": json.loads(sensors_metrics_types_df.to_json(orient='records')),
                             "columns": columns,
                             "types": types,
                             "metrics": metrics})
    return response
