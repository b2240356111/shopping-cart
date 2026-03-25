import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from typing import Any
cart = {}
special_offer_list = ("coffee", "apple", "cereal", "cheese", "pasta")
coupon_codes = {"WELCOME10": 0.10, "SAVE20": 0.20, "MEGA25": 0.25}
used_coupons = set()

def add_item_to_cart(item_name, quantity, unit_price):
    #this code adds the taken variables to the cart dictionary
    global cart
    if quantity<=0 or unit_price<=0:
        return
    if item_name in cart:
        cart[item_name]["quantity"]+=quantity
    else:
        cart[item_name] = {
            "quantity": quantity,
            "unit_price": unit_price
        }
def remove_item_from_cart(item_name, quantity):
    #this function decreases the quantity of given item if the quantity is bigger then zero
    global cart
    if item_name not in cart:
        return
    if quantity<=0:
        return
    else:
        cart[item_name]["quantity"]-=quantity
        if cart[item_name]["quantity"]<=0:
            del cart[item_name]
def display_cart():
    #this function adds every items features into a list called line and turns the list into a string when returning
    line = []
    if len(cart) == 0:
        return "Your cart is empty."
    else:
        for item_name in cart:
            if item_name in special_offer_list:
                line.append(f"Item: {item_name}* | Quantity: {cart[item_name]['quantity']} | Unit price: {cart[item_name]['unit_price']}")
            else:
                line.append(f"Item: {item_name} | Quantity: {cart[item_name]['quantity']} | Unit price: {cart[item_name]['unit_price']}")
        result = ""
        for i in line:
            result += i + "\n"
        return result
def get_cart_summary():
    unique_item = len(cart)
    total_unit_quantity = 0
    subtotal = 0
    special_count = 0
    for item, data in cart.items():
        total_unit_quantity += cart[item]["quantity"]
        subtotal += cart[item]["quantity"]*cart[item]["unit_price"]
        if item in special_offer_list:
            special_count +=1
    return (f"Total Items: {unique_item}\n"
            f"Total Quantity: {total_unit_quantity}\n"
            f"Total price before discount: {round(subtotal, 2)}\n"
            f"Special Offer Items: {special_count}\n")

def  calculate_total_price(coupon_code):
    total_list = []
    one_items_total = 0
    for item in cart: #this loop calculates the total price and total discounts
        one_items_total = cart[item]["quantity"]* cart[item]["unit_price"]
        total_discount = 0
        if cart[item]["quantity"] > 3:
            total_discount += 0.10
        if item in special_offer_list:
            total_discount += 0.05
        total_list.append(one_items_total*(1-total_discount))
    total = sum(total_list)
    if coupon_code in coupon_codes:#this code checks if the written coupon is avaible and already used or not
        if coupon_code not in used_coupons:
            total = total* float(1 - coupon_codes.get(coupon_code))
            used_coupons.add(coupon_code)
    return round(total, 2)









class ShoppingCartWindow(QWidget):
    """
    You do NOT need to modify this class.
    It uses the functions you implement above to interact with the cart.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Smart Shopping Cart System')
        self.setGeometry(600, 200, 600, 500)
        self.initUI()
        self.applystyles()

    def applystyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f9fc;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #dbe3eb;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
                background-color: #eaf1f8;
                border-radius: 5px;
                color: #2c3e50;
                font-weight: bold;
            }
            QLabel {
                color: #34495e;
            }
            QLineEdit {
                border: 1px solid #bdc3c7;
                padding: 8px;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: #ffffff;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            #StatusLabel {
                color: #7f8c8d;
                font-style: italic;
            }
        """)

    def initUI(self):
        # main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        # --- Title ---
        self.title_label = QLabel("Welcome to the Smart Cart")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # --- Item Management Group ---
        self.item_group = QGroupBox("Manage Items")
        self.item_layout = QFormLayout()

        self.item_name_input = QLineEdit()
        self.item_name_input.setPlaceholderText("e.g., apple")
        self.item_layout.addRow("Item Name:", self.item_name_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("e.g., 2")
        self.item_layout.addRow("Quantity:", self.quantity_input)

        self.unit_price_input = QLineEdit()
        self.unit_price_input.setPlaceholderText("e.g., 10.0")
        self.item_layout.addRow("Unit Price:", self.unit_price_input)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add to Cart")
        self.add_button.clicked.connect(self.handle_add_item)
        self.remove_button = QPushButton("Remove from Cart")
        self.remove_button.clicked.connect(self.handle_remove_item)
        self.remove_button.setStyleSheet(
            "QPushButton { background-color: #e74c3c; } QPushButton:hover { background-color: #c0392b; }")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.remove_button)

        self.item_layout.addRow(self.button_layout)
        self.item_group.setLayout(self.item_layout)
        self.main_layout.addWidget(self.item_group)

        # --- Cart Display and Summary Group ---
        self.cart_group = QGroupBox("Shopping Cart")
        self.cart_layout = QVBoxLayout()

        display_btn = QPushButton("Display Cart Contents")
        self.cart_text = QTextEdit()
        self.cart_text.setReadOnly(True)

        display_btn.clicked.connect(self.handle_display_cart)
        display_btn.setStyleSheet(
            "QPushButton { background-color: #9b59b6; } QPushButton:hover { background-color: #8e44ad; }")

        self.cart_layout.addWidget(display_btn)
        self.cart_layout.addWidget(self.cart_text)

        summary_btn = QPushButton("Show Cart Summary")
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        summary_btn.clicked.connect(self.handle_summary)
        summary_btn.setStyleSheet(
            "QPushButton { background-color: #f39c12; } QPushButton:hover { background-color: #e67e22; }")

        self.cart_layout.addWidget(summary_btn)
        self.cart_layout.addWidget(self.summary_text)

        self.cart_group.setLayout(self.cart_layout)
        self.main_layout.addWidget(self.cart_group)

        # --- Total Price Calculation Group ---
        self.total_group = QGroupBox("Calculate Total Price")
        self.total_layout = QVBoxLayout()

        self.coupon_layout = QHBoxLayout()
        self.coupon_input = QLineEdit()
        self.coupon_input.setPlaceholderText("Enter coupon code (e.g., WELCOME10)")
        self.calculate_total_button = QPushButton("Calculate Total")
        self.calculate_total_button.clicked.connect(
            lambda: self.handle_calculate_total(self.coupon_input.text().strip()))
        self.calculate_total_button.setStyleSheet(
            "QPushButton { background-color: #27ae60; } QPushButton:hover { background-color: #229954; }")

        self.total_display = QLabel("Click 'Calculate Total' to see your summary.")
        self.total_display.setAlignment(Qt.AlignLeft)
        self.total_display.setWordWrap(True)
        self.total_layout.addWidget(self.total_display)

        self.coupon_layout.addWidget(self.coupon_input)
        self.coupon_layout.addWidget(self.calculate_total_button)
        self.total_layout.addLayout(self.coupon_layout)
        self.total_group.setLayout(self.total_layout)
        self.main_layout.addWidget(self.total_group)

        # Set main layout
        self.setLayout(self.main_layout)

    def handle_add_item(self) -> None:
        item_name = self.item_name_input.text().strip().lower()
        quantity = self.quantity_input.text().strip()
        unit_price = self.unit_price_input.text().strip()

        for k, v in {"Item Name": item_name, "Quantity": quantity, "Unit Price": unit_price}.items():
            if not v:
                QMessageBox.warning(self, "Input Error", f"{k} cannot be empty.")
                return

        if not self.is_int(quantity):
            QMessageBox.warning(self, "Input Error", "Quantity must be a integer.")
            return

        if not self.is_float(unit_price):
            QMessageBox.warning(self, "Input Error", "Unit Price must be a number.")
            return

        quantity = int(quantity)
        unit_price = float(unit_price)

        add_item_to_cart(item_name, quantity, unit_price)

        # clear text fields
        self.item_name_input.clear()
        self.quantity_input.clear()
        self.unit_price_input.clear()

    def handle_remove_item(self) -> None:
        item_name = self.item_name_input.text().strip().lower()
        quantity = self.quantity_input.text().strip()

        for k, v in {"Item Name": item_name, "Quantity": quantity}.items():
            if not v:
                QMessageBox.warning(self, "Input Error", f"{k} cannot be empty.")
                return

        if not self.is_int(quantity):
            QMessageBox.warning(self, "Input Error", "Quantity must be a integer.")
            return

        quantity = int(quantity)
        remove_item_from_cart(item_name, quantity)

        # clear text fields
        self.item_name_input.clear()
        self.quantity_input.clear()
        self.unit_price_input.clear()

    def handle_display_cart(self) -> None:
        cart_contents = display_cart()
        self.cart_text.setPlainText(cart_contents)

    def handle_summary(self) -> None:
        summary = get_cart_summary()
        self.summary_text.setPlainText(summary)

    def handle_calculate_total(self, coupon_code: str) -> None:
        total_price = calculate_total_price(coupon_code)
        self.total_display.clear()
        self.total_display.setText(f"Total Price: {total_price:.2f}")

    def is_float(self, value: Any) -> bool:
        if value is None:
            return False
        try:
            float(value)
            return True
        except ValueError:
            return False

    def is_int(self, value: Any) -> bool:
        if value is None:
            return False
        try:
            int(value)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShoppingCartWindow()
    window.show()
    sys.exit(app.exec_())