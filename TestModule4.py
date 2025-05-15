import unittest
from Module2Assignment import Drink, Food, Order, IceStorm

class TestCinosOrderSystem(unittest.TestCase):
#module 1 
    def test_create_drink_basic(self):
        drink = Drink("Coke", "Small")
        self.assertEqual(drink.get_base().value, "Coke")
        self.assertEqual(drink.get_size().value, "Small")
        self.assertEqual(drink.get_flavors(), [])
        self.assertEqual(drink.get_total(), 1.50)
#module 2 
    def test_add_flavors_to_drink(self):
        drink = Drink("Sprite", "Medium")
        drink.add_flavor("cherry")
        drink.add_flavor("mint")
        self.assertEqual(drink.get_num_flavors(), 2)
        self.assertIn("cherry", [f.value for f in drink.get_flavors()])
        self.assertAlmostEqual(drink.get_total(), 1.75 + (0.15 * 2), places=2)

    def test_invalid_flavor_raises(self):
        drink = Drink("Pepsi", "Large")
        with self.assertRaises(ValueError):
            drink.add_flavor("banana")
#Module 3 
    def test_create_food_item(self):
        food = Food("Hotdog")
        self.assertEqual(food.get_type().name, "HOTDOG")
        self.assertEqual(food.get_toppings(), [])
        self.assertEqual(food.get_total(), 2.30)

    def test_add_toppings_to_food(self):
        food = Food("French Fries")
        food.add_topping("chili")
        food.add_topping("bacon bits")
        self.assertEqual(len(food.get_toppings()), 2)
        self.assertAlmostEqual(food.get_total(), 1.50 + 0.60 + 0.30, places=2)

    def test_invalid_food_raises(self):
        with self.assertRaises(ValueError):
            Food("Pizza")

    def test_invalid_topping_raises(self):
        food = Food("Nacho Chips")
        with self.assertRaises(ValueError):
            food.add_topping("mayo")

    def test_order_with_drinks_and_food(self):
        order = Order()

        d1 = Drink("Dr. Pepper", "Mega")
        d1.add_flavor("lemon")
        d1.add_flavor("cherry")

        f1 = Food("Onion Rings")
        f1.add_topping("ketchup")

        order.add_item(d1)
        order.add_item(f1)

        total = round(d1.cost + f1.cost, 2)
        self.assertAlmostEqual(order.get_total(), total, places=2)

        receipt = order.get_receipt()
        self.assertEqual(len(receipt["items"]), 2)
        self.assertIn("subtotal", receipt)
        self.assertIn("tax", receipt)
        self.assertIn("total", receipt)

        # Check types in receipt
        self.assertEqual(receipt["items"][0]["type"], "Drink")
        self.assertEqual(receipt["items"][1]["type"], "Food")
        
        # ice storm test module 4 
    def setUp(self):
        self.ice_storm = IceStorm()
    
    def test_add_valid_flavor(self):
        self.ice_storm.add_flavor("Chocolate")
        self.assertIn("Chocolate", self.ice_storm.get_flavors())
        self.assertEqual(self.ice_storm.get_num_flavors(), 1)

    def test_add_invalid_flavor(self):
        with self.assertRaises(ValueError):
            self.ice_storm.add_flavor("Strawberry")

    def test_add_multiple_flavors(self):
        self.ice_storm.add_flavor("Banana")
        self.ice_storm.add_flavor("S'more")
        self.assertEqual(self.ice_storm.get_base(), 3.5 + 4.0)
        self.assertEqual(self.ice_storm.get_num_flavors(), 2)

    def test_add_valid_toppings(self):
        self.ice_storm.add_flavor("Vanilla Bean")
        self.ice_storm.add_topping("Cherry")
        self.ice_storm.add_topping("Cookie Dough")
        self.assertEqual(self.ice_storm.get_total(), 3.00 + 0.00 + 1.00)

    def test_add_invalid_topping(self):
        with self.assertRaises(ValueError):
            self.ice_storm.add_topping("Gummy Bears")

    def test_get_size_returns_none(self):
        self.assertIsNone(self.ice_storm.get_size())

    def test_str_output(self):
        self.ice_storm.add_flavor("Mint Chocolate Chip")
        self.ice_storm.add_topping("Pecans")
        expected = "Ice Storm with: Mint Chocolate Chip | Toppings: Pecans | Total: $4.50"
        self.assertEqual(str(self.ice_storm), expected)


if __name__ == '__main__':
    unittest.main()