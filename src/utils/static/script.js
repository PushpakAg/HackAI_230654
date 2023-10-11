// script.js

// Function to fetch and display file content
function displayFileContent(evt) {
    fetch('/api')
        .then(response => response.json())
        .then(data => {
            const fileContent = data['return value'];
            document.getElementById('second-country-val').textContent = fileContent;
            
        })

        .catch(error => {
            console.error('Error loading file content:', error);
            //document.getElementById('current_currency_value').textContent = 'Error loading file content.';
        });
}

// Run the function when the page loads
window.addEventListener('load', displayFileContent);

// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const lower_threshold_input = document.getElementById('lower-threshold');
    const upper_threshold_input = document.getElementById('upper-threshold');
    const first_country_input = document.getElementById('first-country');
    const second_country_input = document.getElementById('second-country');
    const email_input = document.getElementById('email');

    const first_country = document.querySelector("#first-country");
    const second_country = document.querySelector("#second-country");

    const saveData = () => {
            const selectedValue1 = first_country.value;
            const selectedValue2 = second_country.value;
            const data = {
                selectedValue1,
                selectedValue2
            };

            fetch('/save_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                console.log ( result.message );
            })
            .catch(error => {
                console.error('Error:', error);
            });
        };

    first_country.addEventListener("change", saveData);
    second_country.addEventListener("change", saveData);

    document.querySelector('#form').onsubmit = function(event) {
        event.preventDefault();
        console.log("Hello World");
        // Get the user input
        const lower_threshold_input_value = lower_threshold_input.value;
        const upper_threshold_input_value = upper_threshold_input.value;
        const first_country_input_value = first_country_input.value;
        const second_country_input_value = second_country_input.value;
        const email_input_value = email_input.value;

        // Make an AJAX request to the Flask server
        fetch('/process', {
            method: 'POST',
            body: JSON.stringify({ lower_threshold: lower_threshold_input_value, 
                                    upper_threshold: upper_threshold_input_value,
                                    first_country: first_country_input_value,
                                    second_country : second_country_input_value, 
                                    email: email_input_value
                                }),

            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Display the response from the server
            outputDiv.innerHTML = `Server Response: ${data.message}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };
});

// draw graph
window.onload = function() {
fetch('static/data.json')
.then(response => response.json())
.then(data => {
    const ctx = document.getElementById('myChart').getContext('2d');

    new Chart(ctx, {
        type: 'line', // Change the chart type to 'line'
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Data from JSON',
                data: data.data,
                fill: true, // Don't fill the area under the line
                borderColor: '#EADBC8',
                backgroundColor: 'rgba(0, 0, 255, 0.2)',
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
})
.catch(error => console.error('Error fetching data:', error));}