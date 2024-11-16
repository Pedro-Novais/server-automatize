from flask import Blueprint, request
from Services import PaymentService

from auth.middleware import token_required

payment_route = Blueprint('payments', __name__)

@payment_route.route('/plans', methods=['GET'])
@token_required
def get_plan(userId):
    response = PaymentService.get_plan(user=userId)
    return response

@payment_route.route('/plans', methods=['POST'])
@token_required
def create_plan(userId):
    response = PaymentService.create_plan(user=userId, request=request)
    return response

@payment_route.route('/subscriptions', methods=['POST'])
@token_required
def create_subscription(userId):
    response = PaymentService.create_subscription(user=userId, request=request)
    return response

@payment_route.route('/subscriptions/<subscription>', methods=['DELETE'])
@token_required
def cancel_subscription(userId, subscription):
    response = PaymentService.cancel_subscription(user=userId, request=request)
    return response
