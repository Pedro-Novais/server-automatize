from flask import Blueprint, request
project_route = Blueprint('project', __name__)

@project_route.route('/', methods=['POST'])
def create_project():
    pass