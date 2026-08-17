from flask import Flask

app = Flask(__name__)


class Order:
    pass


class Payment:
    pass


def verify_payment():
    pass


def create_order():
    pass


@app.post("/payment")
@login_required
def payment():

    verify_payment()

    order = Order()

    create_order()

    pay = Payment()

    return "Done"