class ENDPOINTS(object):
    CREATE_CLIENT = "https://api.mercadopago.com/v1/customers"
    DELETE_CLIENT = "https://api.mercadopago.com/v1/customers/{id}"
    CREATE_PLAN = "https://api.mercadopago.com/preapproval_plan"
    CREATE_PREAPPROVAL = "https://api.mercadopago.com/preapproval"
    CARD = "https://api.mercadopago.com/v1/customers/{customer_id}/cards"
    BACK_URL_TEST = "http://127.0.0.1"