from src.messages.current_value import CurrencyVal
from src.messages.general import agent_response
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
import os
import json

client = Agent(
    name="client",
    port=8008,
    seed="secret phase",
    endpoint=["http://127.0.0.1:8008/submit"],
)#http://localhost:8008/submit
fund_agent_if_low(client.wallet.address())

file_path = r"C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\user_data2.json"

@client.on_interval(period=5.0)
async def send_message(ctx: Context):
    
    with open(file_path,"r") as f:
        value = json.load(f)

    cr_val = str(value["selectedValue2"])

    currency_val_request = CurrencyVal(base_currency=cr_val)
    recepient_Add = "agent1qw6wwuvwnes0920d0wl05s0psx84vjtjct4ls50prxykyahzlt9pzmwdkyy"

    await ctx.send(recepient_Add, currency_val_request)

@client.on_message(model=agent_response)
async def message_handler(ctx: Context, _: str, msg: agent_response):
    # ctx.logger.info("hello client is receiving vals ")
    f = open(r"C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\data\Mast.txt", "w")
    f.write(str(msg.value))
    f.close()
    ctx.logger.info(f"Received the value as : {str(msg.value)}")


if __name__ == "__main__":
    client.run()

#agent1qvv0e9y47fkgcd6ys0l5az08decls0y4vvpxr3cyqrc59fcczad9w9ks0qm
