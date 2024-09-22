from flask import Blueprint, request

register_route = Blueprint('register', __name__)

@register_route.route('/', methods=['POST'])
def register():
    pass
