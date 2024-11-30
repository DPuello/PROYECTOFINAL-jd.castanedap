from models.icecreamshop import IceCreamShop
from database.db import db
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user

icecreamshop_blueprint = Blueprint("icecreamshop_bp", __name__)


@icecreamshop_blueprint.route("/")
@login_required
def index():
    icecreamshops = IceCreamShop.query.all()
    return render_template("index.html", icecreamshops=icecreamshops)


@icecreamshop_blueprint.route("/<id>/best_product")
@login_required
def best_product(id):
    if not current_user.is_admin:
        return redirect(url_for('user_bp.unauthorized'))
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404
    return icecreamshop.get_best_product()


@icecreamshop_blueprint.route("/<id>/sales")
@login_required
def sales(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    return (
        f"Sales of {icecreamshop.name}: {icecreamshop.day_sales} | "
        f"Total sold: {icecreamshop.day_total_sold}"
    )


@icecreamshop_blueprint.route("/new")
@login_required
def new():
    return render_template("new_icecreamshop.html")


@icecreamshop_blueprint.route("/create", methods=["POST"])
@login_required
def create():
    try:
        new_shop = IceCreamShop(
            name=request.form['name']
        )
        db.session.add(new_shop)
        db.session.commit()
        return redirect(url_for('icecreamshop_bp.index'))
    except Exception as e:
        return jsonify({
            "error": "Error creating ice cream shop",
            "message": str(e)
        }), 400
