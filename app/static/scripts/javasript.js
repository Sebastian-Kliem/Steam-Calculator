/*
Copyright (c) [2024] [Sebastian Kliem]
*/

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('calculation_variables').addEventListener('submit', function (e) {
        e.preventDefault();

        let calculation_mode_setting = document.querySelector('input[name="calculation_method"]:checked').value === '1';
        let temperature = document.getElementById('temperature').value;
        let temperature_setting = document.querySelector('input[name="temperature_setting"]:checked').value;
        let max_flow_in = document.getElementById('max_flow_in').value;
        let humidity = document.getElementById('humidity').value;
        let high_temperature = document.getElementById('high_temperature').checked;

        let host = window.location.hostname;
        let port = window.location.port;
        let protocol = window.location.protocol;
        let pfad = `${protocol}//${host}:${port}/calculation`;


        let data = {
            calculation_mode_setting: calculation_mode_setting,
            temperature: temperature,
            temperature_setting: temperature_setting,
            max_flow_in: max_flow_in,
            humidity: humidity,
            high_temperature: high_temperature
        };

        fetch(pfad, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                const result = data;
                const used_water_per_minute = result.used_water_per_minute;
                const used_water_per_hour = result.used_water_per_hour;

                document.getElementById('calculated_water_per_minute').innerText = used_water_per_minute;
                document.getElementById('calculated_water_per_hour').innerText = used_water_per_hour;
            })
            .catch((error) => {
                console.error('Fehler:', error);
            });
    });
});