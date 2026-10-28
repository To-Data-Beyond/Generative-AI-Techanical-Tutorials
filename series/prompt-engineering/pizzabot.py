import os, json, re, sys
from importlib.metadata import version
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
MODEL = os.getenv("MODEL", "gpt-5.4-mini")
client = OpenAI(max_retries=0, timeout=60)
def get_completion_from_messages(messages, model=MODEL, temperature=None):
    options = {} if temperature is None else {"temperature": temperature}
    result = client.chat.completions.create(
        model=model, messages=messages, reasoning_effort="none",
        max_completion_tokens=2048, **options)
    if result.choices[0].finish_reason != "stop":
        raise RuntimeError("The completion did not finish normally")
    content = result.choices[0].message.content
    if not content:
        raise RuntimeError("No text returned")
    return content
def get_completion(prompt, model=MODEL, temperature=None):
    return get_completion_from_messages(
        [{"role": "user", "content": prompt}], model=model, temperature=temperature)
print("Python:", sys.version.split()[0])
print("openai:", version("openai"), "python-dotenv:", version("python-dotenv"))
print("Model:", MODEL)

import html
from decimal import Decimal
import panel as pn
pn.extension()
MENU = {
    "pepperoni pizza": {"large": "12.95", "medium": "10.00", "small": "7.00"},
    "cheese pizza": {"large": "10.95", "medium": "9.25", "small": "6.50"},
    "eggplant pizza": {"large": "11.95", "medium": "9.75", "small": "6.75"},
    "fries": {"large": "4.50", "regular": "3.50"},
    "greek salad": {"regular": "7.25"},
    "extra cheese": {"regular": "2.00"}, "mushrooms": {"regular": "1.50"},
    "sausage": {"regular": "3.00"}, "canadian bacon": {"regular": "3.50"},
    "AI sauce": {"regular": "1.50"}, "peppers": {"regular": "1.00"},
    "coke": {"large": "3.00", "medium": "2.00", "small": "1.00"},
    "sprite": {"large": "3.00", "medium": "2.00", "small": "1.00"},
    "bottled water": {"regular": "5.00"}}
ORDER_CONTRACT = """Return only a JSON object with exactly two keys: reply and items.
reply: a brief friendly string to collect/clarify the order. Do not include
prices, currency symbols or totals in reply; Python renders all prices.
items: the complete currently confirmed order, an array of objects with exactly
item, size and quantity. Copy item names and sizes from the supplied menu keys.
quantity must be an integer from 1 to 20. Do not include unconfirmed items or
choose an unspecified size; ask the customer to clarify instead. Retain previous
confirmed items unless changed. Do not add Markdown fences or extra keys.
Read explicit choices before asking questions: "one regular fries" confirms
item="fries", size="regular", quantity=1. "medium cheese pizza, no toppings"
confirms the medium pizza and needs no toppings question. Never ask again for
a size already supplied in the current message or conversation. Include every
explicitly ordered item, including fries and water, in items immediately.
"""
def render_order_response(payload):
    if not isinstance(payload, dict) or set(payload) != {"reply", "items"}:
        raise ValueError("Invalid order response fields")
    reply, items = payload["reply"], payload["items"]
    if not isinstance(reply, str) or not reply.strip() or not isinstance(items, list):
        raise ValueError("Invalid reply or items")
    if re.search(r"[$€£]|\d+\.\d{2}\b", reply):
        raise ValueError("Prices must come from Python, not generated reply text")
    total = Decimal("0.00")
    lines = []
    for row in items:
        if not isinstance(row, dict) or set(row) != {"item", "size", "quantity"}:
            raise ValueError("Invalid item fields")
        item, size, quantity = row["item"], row["size"], row["quantity"]
        if not isinstance(item, str) or not isinstance(size, str) or item not in MENU or size not in MENU[item]:
            raise ValueError("Unknown menu item or size")
        if type(quantity) is not int or not 1 <= quantity <= 20:
            raise ValueError("Invalid quantity")
        unit = Decimal(MENU[item][size])
        line_total = unit * quantity
        total += line_total
        lines.append(f"{quantity} × {size} {item}: ${unit:.2f} each = ${line_total:.2f}")
    receipt = "\n\nOrder so far:\n" + "\n".join(lines) + f"\nTotal: ${total:.2f}" if lines else ""
    return reply.strip() + receipt, total
def chat_turn(state, prompt):
    prompt = prompt.strip()
    if not prompt:
        return None
    pending = state + [{"role": "user", "content": prompt}]
    request = pending + [{"role": "system", "content": ORDER_CONTRACT + "\nMenu keys and unit prices: " + json.dumps(MENU)}]
    payload = json.loads(get_completion_from_messages(request))
    response, total = render_order_response(payload)
    state.extend([pending[-1], {"role": "assistant", "content": response}])
    return response
def build_pizzabot(system_message):
    context = [{"role": "system", "content": system_message}]
    inp = pn.widgets.TextInput(label="Message", placeholder="Enter text here…")
    button = pn.widgets.Button(label="Chat!")
    transcript = pn.Column(sizing_mode="stretch_width")
    status = pn.pane.Str("")
    def collect_messages(event=None):
        prompt = inp.value_input.strip()
        if not prompt or button.disabled:
            return
        button.disabled = True
        status.object = ""
        try:
            response = chat_turn(context, prompt)
            transcript.extend([
                pn.pane.HTML("<b>User:</b><pre>" + html.escape(prompt) + "</pre>"),
                pn.pane.HTML("<b>Assistant:</b><pre>" + html.escape(response) + "</pre>",
                             styles={"background-color": "#F6F6F6"})])
            inp.value = ""
            inp.value_input = ""
        except Exception:
            status.object = "Unable to get a reply. Please try again."
        finally:
            button.disabled = False
    button.on_click(collect_messages)
    dashboard = pn.Column(inp, button, status, transcript, max_width=700, sizing_mode="stretch_width")
    return dashboard, context, inp, button, collect_messages
print("Panel:", pn.__version__)
print("PizzaBot callback ready; no API request is made while constructing the UI.")

pizzabot_system = "You are OrderBot, an automated service to collect orders for a pizza restaurant.  You first greet the customer, then collects the order,  and then asks if it's a pickup or delivery.  You wait to collect the entire order, then summarize it and check for a final  time if the customer wants to add anything else.  If it's a delivery, you ask for an address.  Finally ask only for a payment preference (cash or card); never collect card numbers, security codes or other payment credentials. This is a fictional order demonstration; no order is placed and no payment is processed. Make sure to clarify all options, extras and sizes to uniquely  identify the item from the menu. You respond in a short, very conversational friendly style.  For three listed prices, sizes are large, medium, small in that order. For fries the two prices are large and regular. Drinks with three prices are large, medium, small. Bottled water has one size. Do not invent fees or menu items.\nThe menu includes  pepperoni pizza  12.95, 10.00, 7.00  cheese pizza   10.95, 9.25, 6.50  eggplant pizza   11.95, 9.75, 6.75  fries 4.50, 3.50  greek salad 7.25  Toppings:  extra cheese 2.00,  mushrooms 1.50  sausage 3.00  canadian bacon 3.50  AI sauce 1.50  peppers 1.00  Drinks:  coke 3.00, 2.00, 1.00  sprite 3.00, 2.00, 1.00  bottled water 5.00  "
dashboard, context, inp, button_conversation, collect_messages = build_pizzabot(pizzabot_system)
dashboard.servable(title="PizzaBot")
print("PizzaBot UI ready. Enter a fictional order and click Chat! to call the model.")
