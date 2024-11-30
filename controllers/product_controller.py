from models.product import Product
from models.icecreamshop import IceCreamShop
from models.ingredient import Ingredient
from database.db import db
from flask import (
    Blueprint, jsonify, render_template,
    request, redirect, url_for
)
from flask_login import login_required, current_user

product_blueprint = Blueprint("product_bp", __name__)


@product_blueprint.route("/products")
def index():
    products = Product.query.all()
    return render_template("all_products.html", products=products)

@product_blueprint.route("/products/all")
@login_required
def index_json():
    products = Product.query.all()
    serialized_products = [product.serialize() for product in products]
    return jsonify(
        {
            "data": serialized_products,
            "message": "Products fetched successfully",
            "success": True,
        }
    )

@product_blueprint.route("/products/<id>")
@login_required
def show(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify({"error": "Product not found", "message": f"No product found with id: {id}", "success": False}), 404
    serialized_product = product.serialize()
    return jsonify({"data": serialized_product, "message": "Product fetched successfully", "success": True})

@product_blueprint.route("/products/by_name/<name>")
@login_required
def show_by_name(name):
    product = Product.query.filter_by(name=name).first()
    if product is None:
        return jsonify({"error": "Product not found", "message": f"No product found with name: {name}", "success": False}), 404
    serialized_product = product.serialize()
    return jsonify({"data": serialized_product, "message": "Product fetched successfully", "success": True})


@product_blueprint.route("/<id>/products")
@login_required
def products(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404
    return render_template(
        "products.html",
        products=icecreamshop.products,
        icecreamshop=icecreamshop
    )


@product_blueprint.route("/<id>/products/new")
@login_required
def new(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    if not icecreamshop.can_add_product:
        return jsonify({
            "error": "Maximum products reached",
            "message": f"Maximum number of products ({IceCreamShop.MAX_PRODUCTS}) reached"
        }), 400

    return render_template(
        "new_product.html",
        icecreamshop=icecreamshop
    )


@product_blueprint.route("/<id>/products/create", methods=["POST"])
@login_required
def create(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    if not icecreamshop.can_add_product:
        return jsonify({
            "error": "Maximum products reached",
            "message": f"Maximum number of products ({IceCreamShop.MAX_PRODUCTS}) reached"
        }), 400

    form_data = {
        'name': request.form['name'],
        'price': float(request.form['price']),
        'category': request.form['category'],
        'ingredients': request.form.getlist('ingredients'),
    }

    try:
        new_product = Product(
            name=form_data['name'],
            price=form_data['price'],
            category=form_data['category'],
            id_ice_cream_shop=id,
        )

        ingredient_ids = [int(id) for id in form_data['ingredients']]
        ingredients = Ingredient.query.filter(
            Ingredient.id.in_(ingredient_ids)).all()
        new_product.ingredients.extend(ingredients)

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('product_bp.products', id=id))
    except ValueError as e:
        return str(e), 400


@product_blueprint.route("/sell/<id_product>")
@login_required
def sell(id_product):
    product = Product.query.filter_by(id=id_product).first()
    if product is None:
        return jsonify({
            "error": "Product not found",
            "message": f"No product found with id: {id_product}"
        }), 404
    icecreamshop = IceCreamShop.query.filter_by(id=product.id_ice_cream_shop).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {product.id_ice_cream_shop}"
        }), 404
    result = icecreamshop.sell(int(id_product))
    if result is True:
        db.session.commit()
        return jsonify({"success": True, "message": f"Sold product!: {product.name}"})
    else:
        return jsonify({
            "success": False,
            "error": "Error selling product",
            "message": result
        }), 400


@product_blueprint.route("/products/calculate_calories/<id>")
@login_required
def calculate_calories(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify({
            "error": "Product not found",
            "message": f"No product found with id: {id}"
        }), 404
    return jsonify({"name": product.name, "calories": product.calc_calories()})


@product_blueprint.route("/products/calculate_cost/<id>")
@login_required
def calculate_cost(id):
    if not current_user.is_admin:
        return redirect(url_for('user.unauthorized'))
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify({
            "error": "Product not found",
            "message": f"No product found with id: {id}"
        }), 404
    return jsonify({"name": product.name, "cost": product.calc_cost()})


@product_blueprint.route("/products/calculate_earnings/<id>")
@login_required
def calculate_earnings(id):
    if not current_user.is_admin:
        return redirect(url_for('user.unauthorized'))
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify({
            "error": "Product not found",
            "message": f"No product found with id: {id}"
        }), 404
    return jsonify({"name": product.name, "earnings": product.calc_earnings()})

@product_blueprint.route("/product/earnings/<id>")
@login_required
def earnings(id):
    if not current_user.is_admin:
        return redirect(url_for('user.unauthorized'))
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify({
            "error": "Product not found",
            "message": f"No product found with id: {id}"
        }), 404
    return render_template("product_earnings.html", product=product)

