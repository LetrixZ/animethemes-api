from flask import Blueprint, jsonify

from src.routes.seasons import list_years, list_current_season

android = Blueprint('android', __name__)


@android.route('home')
def get_home_list():
    return jsonify({'year_list': list_years(True), 'current_season': list_current_season(True)})
