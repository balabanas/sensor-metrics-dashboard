const config = {
    // API URL to get sensor data
    apiUrl: 'http://django:8000/api/sensors/',


    // For default selected metrics specification of 'All' takes precedence, then 'None', then any specific metric
    selectedMetricDefault: ['Battery voltage V', 'Temperature °C'],
}

export default config
