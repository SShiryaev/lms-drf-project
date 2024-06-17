import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_product(payment):
    """Создание продукта для оплаты"""

    payment_product = None
    if payment.course:
        payment_product = payment.course.name
    else:
        if payment.lesson:
            payment_product = payment.lesson.name

    stripe_product = stripe.Product.create(name=payment_product)
    product_id = stripe_product.get('id')
    return product_id


def create_stripe_price(amount, product):
    """Создание цены для оплаты."""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product,
    )
    return price


def create_stripe_session(price):
    """Создание сессии для оплаты."""

    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/',
        line_items=[{'price': price.get('id'), 'quantity': 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
