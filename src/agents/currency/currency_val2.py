from messages.current_value import CurrencyVal
from messages.general import agent_response
from uagents import Agent, Context, Protocol, Bureau
from uagents.setup import fund_agent_if_low
import os
import requests
import json

current_currency_file_path = r"C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\user_data2.json"

agent = Agent(
    name= "currency_val_hh",
    seed = "check val"
)
def fetch_exchange_rates(base_currency,api_url):
    response = requests.get(api_url)
    data = response.json()

    base_cr = base_currency
    if base_cr in data["conversion_rates"]:
        currency_val = data["conversion_rates"][base_cr]
    else:
        currency_val = "DONT KNOW"
    return currency_val

fund_agent_if_low(agent.wallet.address())
currency_value_protocol = Protocol("CurrencyValue")

@currency_value_protocol.on_message(model= CurrencyVal,replies= agent_response )
async def get_currency_value(ctx: Context, sender: str, msg: CurrencyVal):
    ctx.logger.info(f"Received message from {sender}, session: {ctx.session}")
    with open(current_currency_file_path,"r") as f:
        data_aa = json.load(f)

    currency = str(data_aa["selectedValue1"])

    api_url = f'https://v6.exchangerate-api.com/v6/f4b4ef0a8c3dc88bf7db4859/latest/{currency}'
    cr_value = fetch_exchange_rates(msg.base_currency,api_url=api_url)
    await ctx.send(
        sender,
        agent_response(
            value= cr_value
            )
        )
agent.include(currency_value_protocol)