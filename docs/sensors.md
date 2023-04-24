# The structure of sensors.json

```
{
    "1048609": { // sensor ID
        "metrics": { // sensor metrics
            "1": {    // metrics ID (refers to items id metrics.json)
                "t": 1565155052, // measurement timestamp
                "v": 21.8 // measurement value 
            }
        },
        "name": "Sensor 1", // sensor name
        "type": 1,    // sensor type (refers to sensorTypes.json)
        "variant": 8 // sensor variant (refers to sensorTypes.json)
    }
}
```
