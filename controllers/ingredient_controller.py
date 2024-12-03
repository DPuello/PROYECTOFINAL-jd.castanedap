from models.ingredient import Ingredient
from models.icecreamshop import IceCreamShop
from database.db import db
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user

ingredient_blueprint = Blueprint("ingredient_bp", __name__)


@ingredient_blueprint.route("/ingredients")
@login_required
def index():
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    ingredients = Ingredient.query.all()
    return render_template("all_ingredients.html", ingredients=ingredients)


@ingredient_blueprint.route("/ingredients/all")
@login_required
def index_json():
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    ingredients = Ingredient.query.all()
    serialized_ingredients = [ingredient.serialize() for ingredient in ingredients]
    
    return jsonify(
        {
            "data": serialized_ingredients,
            "message": "Ingredients fetched successfully",
            "success": True,
        }
    )


@ingredient_blueprint.route("/ingredients/<id>")
@login_required
def show(id):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    ingredient = Ingredient.query.get(id)
    if ingredient is None:
        return jsonify({"error": "Ingredient not found", "message": f"No ingredient found with id: {id}", "success": False}), 404
    serialized_ingredient = ingredient.serialize()
    return jsonify({"data": serialized_ingredient, "message": "Ingredient fetched successfully", "success": True})


@ingredient_blueprint.route("/ingredients/by_name/<name>")
@login_required
def show_by_name(name):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    if "%20" in name:
        name = name.replace("%20", " ")
    ingredient = Ingredient.query.filter_by(name=name).first()
    if ingredient is None:
        return jsonify({"error": "Ingredient not found", "message": f"No ingredient found with name: {name}", "success": False}), 404
    serialized_ingredient = ingredient.serialize()
    return jsonify({"data": serialized_ingredient, "message": "Ingredient fetched successfully", "success": True})


@ingredient_blueprint.route("/<id>/ingredients")
@login_required
def ingredients(id):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return (
            jsonify(
                {
                    "error": "IceCreamShop not found",
                    "message": f"No ice cream shop found with id: {id}",
                }
            ),
            404,
        )
    return render_template(
        "ingredients.html",
        ingredients=icecreamshop.ingredients,
        icecreamshop=icecreamshop,
    )


@ingredient_blueprint.route("/stock/<id_ingredient>")
@login_required
def stock(id_ingredient):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    ingredient = Ingredient.query.filter_by(id=id_ingredient).first()
    if ingredient is None:
        return (
            jsonify(
                {
                    "error": "Ingredient not found",
                    "message": f"No ingredient found with id: {id_ingredient}",
                }
            ),
            404,
        )
    icecreamshop = IceCreamShop.query.filter_by(id=ingredient.id_ice_cream_shop).first()
    if icecreamshop is None:
        return (
            jsonify(
                {
                    "error": "IceCreamShop not found",
                    "message": f"No ice cream shop found with id: {ingredient.id_ice_cream_shop}",
                }
            ),
            404,
        )
    try:
        old_stock = ingredient.stock
        ingredient.stock_up()
        db.session.commit()
        return (
        jsonify(
            {
                "success": True,
                "message": f"Stocked up {ingredient.name}",
                "new_stock": ingredient.stock,
                "old_stock": old_stock,
            }
        ),
            200,
        )
    except Exception as e:
        return (
            jsonify({"error": "Failed to stock up ingredient", "message": str(e)}),
            500,
        )


@ingredient_blueprint.route("/renew/<id_ingredient>")
@login_required
def renew(id_ingredient):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    ingredient = Ingredient.query.filter_by(id=id_ingredient).first()
    if ingredient is None:
        return (
            jsonify(
                {
                    "error": "Ingredient not found",
                    "message": f"No ingredient found with id: {id_ingredient}",
                }
            ),
            404,
        )
    icecreamshop = IceCreamShop.query.filter_by(id=ingredient.id_ice_cream_shop).first()
    if icecreamshop is None:
        return (
            jsonify(
                {
                    "error": "IceCreamShop not found",
                    "message": f"No ice cream shop found with id: {ingredient.id_ice_cream_shop}",
                }
            ),
            404,
        )

    try:
        ingredient.renew_stock()
        db.session.commit()
        return jsonify(
            {
                "success": True,
                "message": f"Renewed {ingredient.name}",
                "new_stock": ingredient.stock,
            }
        )
    except ValueError as e:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Base ingredients cannot be renewed",
                    "message": str(e),
                }
            ),
            400,
        )


@ingredient_blueprint.route("/ingredients/<id_ingredient>/is_healthy")
@login_required
def is_healthy(id_ingredient):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    ingredient = Ingredient.query.get(id_ingredient)
    if ingredient is None:
        return (
            jsonify(
                {
                    "error": "Ingredient not found",
                    "message": f"No ingredient found with id: {id_ingredient}",
                }
            ),
            404,
        )
    return jsonify({"ingredient": ingredient.name, "is_healthy": ingredient.its_healthy()})


@ingredient_blueprint.route("/ingredients/<id_ingredient>/stock_up")
@login_required
def stock_up(id_ingredient):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    ingredient = Ingredient.query.get(id_ingredient)
    if ingredient is None:
        return (
            jsonify(
                {
                    "error": "Ingredient not found",
                    "message": f"No ingredient found with id: {id_ingredient}",
                }
            ),
            404,
        )
    old_stock = ingredient.stock
    ingredient.stock_up()
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "message": f"Stock up: {ingredient.name}",
            "new_stock": ingredient.stock,
            "old_stock": old_stock,
        }
    )


@ingredient_blueprint.route("/ingredients/<id_ingredient>/renew_stock")
@login_required
def renew_stock(id_ingredient):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    ingredient = Ingredient.query.get(id_ingredient)
    if ingredient is None:
        return (
            jsonify(
                {
                    "error": "Ingredient not found",
                    "message": f"No ingredient found with id: {id_ingredient}",
                }
            ),
            404,
        )
    try:
        ingredient.renew_stock()
    except ValueError as e:
        return (
            jsonify({"error": "Base ingredients cannot be renewed", "message": str(e)}),
            400,
        )
    db.session.commit()
    return jsonify(
        {"success": True, "message": f"Renewed ingredient: {ingredient.name}"}
    )


@ingredient_blueprint.route("/<id>/ingredients/new")
@login_required
def new(id):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return (
            jsonify(
                {
                    "error": "IceCreamShop not found",
                    "message": f"No ice cream shop found with id: {id}",
                }
            ),
            404,
        )
    return render_template("new_ingredient.html", icecreamshop=icecreamshop)


@ingredient_blueprint.route("/<id>/ingredients/create", methods=["POST"])
@login_required
def create(id):
    if not current_user.is_admin and not current_user.is_employee:
        return redirect(url_for('user.unauthorized'))
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return (
            jsonify(
                {
                    "error": "IceCreamShop not found",
                    "message": f"No ice cream shop found with id: {id}",
                }
            ),
            404,
        )

    new_ingredient = Ingredient(
        name=request.form["name"],
        category=request.form["category"],
        price=float(request.form["price"]),
        calories=int(request.form["calories"]),
        stock=int(request.form["stock"]),
        vegan=request.form.get("vegan") == "on",
        flavor=request.form.get("flavor", ""),
        id_ice_cream_shop=id,
    )

    db.session.add(new_ingredient)
    db.session.commit()

    return redirect(url_for("ingredient_bp.ingredients", id=id))
