
from flask import Flask, jsonify, request
from enum import Enum


# Enum for sizes
class Size(Enum):
    SMALL = 'Small'
    MEDIUM = 'Medium'
    LARGE = 'Large'
    MEGA = 'Mega'

    @staticmethod
    def get_price(size):
        prices = {
            Size.SMALL: 1.50,
            Size.MEDIUM: 1.75,
            Size.LARGE: 2.05,
            Size.MEGA: 2.15,
        }
        return prices[size]

# Drink bases enum
class Base(Enum):
    WATER = "Water"
    SPRITE = "Sprite"
    COKE = "Coke"
    DR_PEPPER = "Dr. Pepper"
    PEPSI = "Pepsi"
    LEAF_WINE = "Leaf wine"

# Flavor enums for drinks
class Flavor(Enum):
    LEMON = "lemon"
    CHERRY = "cherry"
    STRAWBERRY = "strawberry"
    MINT = "mint"
    BLUEBERRY = "blueberry"
    LIME = "lime"

# Toppings for food items
class Topping(Enum):
    CHERRY = 0.00
    WHIPPED_CREAM = 0.00
    CARAMEL_SAUCE = 0.50
    CHOCOLATE_SAUCE = 0.50
    NACHO_CHEESE = 0.30
    CHILI = 0.60
    BACON_BITS = 0.30
    KETCHUP = 0.00
    MUSTARD = 0.00

# Food items enum 
class FoodItem(Enum):
    HOTDOG = 2.30
    CORNDOG = 2.00
    ICE_CREAM = 3.00
    ONION_RINGS = 1.75
    FRENCH_FRIES = 1.50
    TATER_TOTS = 1.70
    NACHO_CHIPS = 1.90


# IceStorm class
# Module 4 
class IceStorm:
    FLAVORS = {
        "Mint Chocolate Chip": 4.00,
        "Chocolate": 3.00,
        "Vanilla Bean": 3.00,
        "Banana": 3.50,
        "Butter Pecan": 3.50,
        "S'more": 4.00,
    }

    TOPPINGS = {
        "Cherry": 0.00,
        "Whipped Cream": 0.00,
        "Caramel Sauce": 0.50,
        "Chocolate Sauce": 0.50,
        "Storios": 1.00,
        "Dig Dogs": 1.00,
        "T&T's": 1.00,
        "Cookie Dough": 1.00,
        "Pecans": 0.50,
    }

    def __init__(self):
        self.flavors = []
        self.toppings = []

    def get_flavors(self):
        return self.flavors

    def add_flavor(self, flavor):
        if flavor not in IceStorm.FLAVORS:
            raise ValueError(f"Flavor '{flavor}' is not available.")
        self.flavors.append(flavor)

    def get_base(self):
        # Base is the cost of flavors
        return sum(IceStorm.FLAVORS[flavor] for flavor in self.flavors)

    def get_size(self):
        # Not for Ice Storms
        return None

    def get_total(self):
        base_total = self.get_base()
        toppings_total = sum(IceStorm.TOPPINGS[top] for top in self.toppings)
        return round(base_total + toppings_total, 2)

    def get_num_flavors(self):
        return len(self.flavors)

    def add_topping(self, topping):
        if topping not in IceStorm.TOPPINGS:
            raise ValueError(f"Topping '{topping}' is not available.")
        self.toppings.append(topping)

    def __str__(self):
        flavor_str = ', '.join(self.flavors) if self.flavors else "No flavors"
        topping_str = ', '.join(self.toppings) if self.toppings else "No toppings"
        total = f"${self.get_total():.2f}"
        return f"Ice Storm with: {flavor_str} | Toppings: {topping_str} | Total: {total}"
# IceStorm class

# Drink class
class Drink:
    def __init__(self, base, size):
        base = base.lower()
        found_base = next((b for b in Base if b.value.lower() == base), None)
        if not found_base:
            raise ValueError(f"Invalid base: {base}")
        self.__base = found_base

        size = size.lower()
        found_size = next((s for s in Size if s.value.lower() == size), None)
        if not found_size:
            raise ValueError(f"Invalid size: {size}")
        self.__size = found_size

        self.__flavors = []

    def get_base(self):
        return self.__base

    def get_size(self):
        return self.__size

    def set_size(self, size):
        size = size.lower()
        found_size = next((s for s in Size if s.value.lower() == size), None)
        if not found_size:
            raise ValueError(f"Invalid size: {size}")
        self.__size = found_size

    def get_flavors(self):
        return list(self.__flavors)

    def add_flavor(self, flavor):
        flavor = flavor.lower()
        found_flavor = next((f for f in Flavor if f.value.lower() == flavor), None)
        if not found_flavor:
            raise ValueError(f"Invalid flavor: {flavor}")
        if found_flavor not in self.__flavors:
            self.__flavors.append(found_flavor)

    def get_num_flavors(self):
        return len(self.__flavors)

    def get_total(self):
        base_price = Size.get_price(self.__size)
        flavor_cost = 0.15 * self.get_num_flavors()
        return round(base_price + flavor_cost, 2)

    @property
    def cost(self):
        return self.get_total()

    def __str__(self):
        flavors = ", ".join(f.value for f in self.__flavors) or "none"
        return f"{self.__size.value} {self.__base.value} with {flavors}"


# Food class
class Food:
    def __init__(self, food_type):
        food_type = food_type.upper().replace(" ", "_")
        if food_type not in FoodItem.__members__:
            raise ValueError(f"Invalid food item: {food_type}")
        self.__type = FoodItem[food_type]
        self.__toppings = []

    def get_type(self):
        return self.__type

    def get_price(self):
        return self.__type.value

    def add_topping(self, topping):
        topping = topping.upper().replace(" ", "_")
        if topping not in Topping.__members__:
            raise ValueError(f"Invalid topping: {topping}")
        self.__toppings.append(Topping[topping])

    def get_toppings(self):
        return list(self.__toppings)

    def get_total(self):
        topping_cost = sum(t.value for t in self.__toppings)
        return round(self.__type.value + topping_cost, 2)

    @property
    def cost(self):
        return self.get_total()

    def __str__(self):
        toppings = ", ".join(t.name.replace("_", " ").title() for t in self.__toppings) or "none"
        return f"{self.__type.name.replace('_', ' ').title()} with {toppings}"


# Order class
class Order:
    def __init__(self):
        self.__items = []

    def add_item(self, item):
        if isinstance(item, (Drink, Food)):
            self.__items.append(item)
        else:
            raise TypeError("Only Drink or Food objects allowed.")

    def get_total(self):
        return round(sum(item.cost for item in self.__items), 2)

    def get_total_with_tax(self):
        subtotal = self.get_total()
        tax = round(subtotal * 0.0725, 2)
        total = round(subtotal + tax, 2)
        return {"subtotal": subtotal, "tax": tax, "total": total}

    def get_receipt(self):
        items_list = []
        for i, item in enumerate(self.__items, 1):
            if isinstance(item, Drink):
                items_list.append({
                    "number": i,
                    "type": "Drink",
                    "base": item.get_base().value,
                    "size": item.get_size().value,
                    "flavors": [f.value for f in item.get_flavors()],
                    "item_total": item.cost
                })
            elif isinstance(item, Food):
                items_list.append({
                    "number": i,
                    "type": "Food",
                    "food_type": item.get_type().name.replace("_", " ").title(),
                    "toppings": [t.name.replace("_", " ").title() for t in item.get_toppings()],
                    "item_total": item.cost
                })
        totals = self.get_total_with_tax()
        return {
            "items": items_list,
            "subtotal": totals["subtotal"],
            "tax": totals["tax"],
            "total": totals["total"]
        }


# Flask setup
app = Flask(__name__)
order = Order()

@app.route('/menu', methods=['GET'])
def menu():
    return jsonify({
        "bases": [b.value for b in Base],
        "flavors": [f.value for f in Flavor],
        "sizes": [s.value for s in Size],
        "foods": [f.name.replace("_", " ").title() for f in FoodItem],
        "toppings": [t.name.replace("_", " ").title() for t in Topping]
    })

@app.route('/drink', methods=['POST'])
def add_drink():
    data = request.json
    try:
        drink = Drink(data['base'], data['size'])
        for flavor in data.get('flavors', []):
            drink.add_flavor(flavor)
        order.add_item(drink)
        return jsonify({"message": "Drink added successfully."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/food', methods=['POST'])
def add_food():
    data = request.json
    try:
        food = Food(data['type'])
        for topping in data.get('toppings', []):
            food.add_topping(topping)
        order.add_item(food)
        return jsonify({"message": "Food added successfully."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/order/receipt', methods=['GET'])
def receipt():
    return jsonify(order.get_receipt())

if __name__ == '__main__':
    app.run(debug=True)
