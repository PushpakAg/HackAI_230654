# Currency Alert Pro
Currency Alert Pro is your go-to solution for staying on top of currency exchange rates. With the ability to select your base currency and multiple foreign currencies, it connects to real-time exchange rate data via API. You can set your own custom thresholds for alerts, and whenever your specified exchange rates cross those limits, it promptly sends notifications directly to your device. Stay in control and make informed currency exchange decisions with Currency Alert Pro.

## Prerequisites
```bash
pip install uagents
pip install poetry
```
#### Exchangerate-api
* Visit [Exchangerate-api](https://www.exchangerate-api.com/)

## Run the main Script
* To run the project and its agents:
```bash
cd src
poetry run python main.py
```
* You will see in your terminal
```bash
Adding currency agent to Bureau: {currency_agent_address}
Adding checker agent to Bureau: {checker_agent_address}
```
 ## Run the Client Script
 Now keep the main.py script running and open a new terminal and then run client.py
 ```bash
poetry run python client.py
```
This script will send request to get the currency value requested by the user. The currency agent sends value to client agent.

* Upon successful execution you can access the website on you localhost server. You can access it on local flask development server.
* The terminal where client.py was executed you can see the current currency exchange rate being displayed as requested by the user.
* The user has to select the currency from the website and set the thresholds accordingly and enter their email.
* We have created a alert agent using uAgents which constantly monitors the thresholds set by the user and send email as soon as thresholds are met.

## Special Considerations
* Since the Javascript compiles faster than the python running the uagents the shown value on the frontend comes with an latency. Meaning it repreasents the values selected on the currencies selected prior to what is currently selected
* Unfortunately we could not complete the Graph we planned for historical value as that API came was paid.

