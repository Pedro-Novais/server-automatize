class ENDPOINTS(object):
    CREATE_CLIENT = "https://api.mercadopago.com/v1/customers"
    DELETE_CLIENT = "https://api.mercadopago.com/v1/customers/{id}"
    CREATE_PLAN = "https://api.mercadopago.com/preapproval_plan"
    SUBSCRIPTION = "https://api.mercadopago.com/preapproval"
    SUBSCRIPTION_ACTION = "https://api.mercadopago.com/preapproval/{id}"
    CARD = "https://api.mercadopago.com/v1/customers/{customer_id}/cards"
    CARD_ACTION = "https://api.mercadopago.com/v1/customers/{customer_id}/cards/{id}"
    BACK_URL_TEST = "http://127.0.0.1"