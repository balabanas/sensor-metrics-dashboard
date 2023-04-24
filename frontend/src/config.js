const config = {
    // API URL to get sensor data. For prod the port should coincide with frontend's port,
    // as it will be proxied by nginx anyway. For test the port should be Django dev server's port
    // apiUrl: 'http://' + process.env.FRONTEND_HOST + ':' + process.env.FRONTEND_PORT + '/api/sensors/',
    apiUrl: 'http://localhost:8000/api/sensors/',


    // For default selected metrics specification of 'All' takes precedence, then 'None', then any specific metric
    selectedMetricDefault: ['Battery voltage V', 'Temperature °C'],
}

export default config
