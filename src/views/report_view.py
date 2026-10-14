"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from queries.read_user import get_users
from queries.read_product import get_products
from queries.read_order import get_best_selling_products, get_highest_spending_users
from views.template_view import get_template, get_param

def show_highest_spending_users():
    """Show the 10 users who spent the most."""
    highest_spending_users = get_highest_spending_users()
    users = {user.id: user.name for user in get_users(99)}

    user_rows = [
    f"<li>{users.get(user_id, f'Utilisateur {user_id}')} - ${total_spent:.2f}</li>"
    for user_id, total_spent in highest_spending_users]

    return get_template(f"""<h2>Les plus gros acheteurs</h2>
    <ul>{" ".join(user_rows)}</ul>""")

def show_best_sellers():
    """Show report of best selling products."""
    best_selling_products = get_best_selling_products()
    products = {product.id: product.name for product in get_products(99)}

    product_rows = [f"<li>{products.get(product_id, f'Produit {product_id}')} - {quantity_sold} vendu(s)</li>"
                    for product_id, quantity_sold in best_selling_products]

    return get_template(f"""<h2>Les articles les plus vendus</h2>
    <ul>{" ".join(product_rows)}</ul>""")