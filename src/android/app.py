from flask import Blueprint, jsonify

from src.routes.seasons import list_years

android = Blueprint('android', __name__)


@android.route('home')
def get_home_list():
    return jsonify({'year_list': list_years(True)})
