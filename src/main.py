from flask import Flask, send_file, jsonify,render_template, request
import os
import json
import csv
import threading 
import asyncio
from uagents import Bureau
from agents.currency.currency_val2 import agent as currency_value_agent
from agents.check.checker import checker as checker_agent


app = Flask(__name__,template_folder=r"C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\templates",
            static_folder=r"C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\static")

# Define the path to the 'Mast.txt' file using a relative path
file_path = r'C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\data\Mast.txt'


def start_bureau():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bureau = Bureau(
        endpoint = "http://localhost:8000/submit",
        port = 8000
        )
    print(f"Adding currency agent to Bureau: {currency_value_agent.address}")
    print(f"Adding checker agent to Bureau: {checker_agent.address}")
    bureau.add(currency_value_agent)
    bureau.add(checker_agent)
    bureau.run()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api')
def api():
    try:
        # Read the content of the 'Mast.txt' file
        with open(file_path, 'r') as file:
            file_content = file.read()
        return jsonify({'return value': file_content})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/save_data',methods=['POST'])
def save_currencies_to_be_converted():
    try:
        data = request.get_json()
        with open(r'C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\user_data2.json','w') as file:
            json.dump(data,file)
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/process', methods=['POST'])
def process():
    lower_threshold_input = request.json.get('lower_threshold')
    upper_threshold_input = request.json.get('upper_threshold')
    first_country_input = request.json.get('first_country')
    second_country_input = request.json.get('second_country')
    email_address_input = request.json.get('email')
    
    # Save user input to a JSON file
    data = {
             "Lower Threshold": lower_threshold_input,
             "Upper Threshold" : upper_threshold_input, 
             "First Country" : first_country_input,
             "Second Country" : second_country_input 
            }

    with open(r'C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\database.csv','a') as database_file:
        writer_object = csv.writer(database_file)
        writer_object.writerow([ email_address_input, lower_threshold_input, upper_threshold_input, first_country_input, second_country_input ])

    def process_csv_to_json(csv_filename):
        json_data = {}

        with open(csv_filename, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            for row in csv_reader:
                if len(row) == 5:
                    email, threshold1, threshold2, from_currency, to_currency = row

                    if email not in json_data:
                        json_data[email] = {}

                    track_number = len(json_data[email]) + 1
                    track_name = f"track{track_number}"

                    json_data[email][track_name] = {
                        "From_this_currency": from_currency,
                        "to_this_currency": to_currency,
                        "Threshold1": int(threshold1),
                        "Threshold2": int(threshold2)
                    }

        return json_data

    csv_filename = r'C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\database.csv'
    json_data = process_csv_to_json(csv_filename)

    with open(r'C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\user_data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    return "Process return"

if __name__ == '__main__':
    bureau_thread = threading.Thread(target = start_bureau)
    bureau_thread.daemon = True
    bureau_thread.start()
    app.run(debug=True)



