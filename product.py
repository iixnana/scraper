
class Product:
    class Nutrition:

        def __init__(self, energy_kj, energy_kcal, fat, saturated_fatty_acids, monounsaturated_fatty_acids,
                     polyunsaturated_fatty_acids, carbohydrates, sugars, dietary_fiber, protein, sodium):
            self.energy_kj = energy_kj
            self.energy_kcal = energy_kcal
            self.fat = fat
            self.saturated_fatty_acids = saturated_fatty_acids
            self.monounsaturated_fatty_acids = monounsaturated_fatty_acids
            self.polyunsaturated_fatty_acids = polyunsaturated_fatty_acids
            self.carbohydrates = carbohydrates
            self.sugars = sugars
            self.dietary_fiber = dietary_fiber
            self.protein = protein
            self.sodium = sodium

        def get_as_list(self):
            return [self.energy_kj, self.energy_kcal, self.saturated_fatty_acids, self.monounsaturated_fatty_acids,
                    self.polyunsaturated_fatty_acids, self.carbohydrates, self.sugars, self.dietary_fiber, self.protein,
                    self.sodium]

        def get_as_dict(self):
            return {
                "energy kj": self.energy_kj,
                "energy kcal": self.energy_kcal,
                "saturated fatty acids": self.saturated_fatty_acids,
                "monounsaturated fatty acids": self.monounsaturated_fatty_acids,
                "polyunsaturated fatty acids": self.polyunsaturated_fatty_acids,
                "carbohydrates": self.carbohydrates,
                "sugars": self.sugars,
                "dietary fiber": self.dietary_fiber,
                "protein": self.protein,
                "sodium": self.sodium
            }

    def __init__(self, id, path, title, brand, description, currency, price, unit_price, unit, size, delivery_days, ingredients, origin, supplier, expiration, energy_kj, energy_kcal, fat,
                              saturated_fatty_acids, monounsaturated_fatty_acids,polyunsaturated_fatty_acids,
                              carbohydrates, sugars, dietary_fiber, protein, sodium):
        self.id = id
        self.path = path
        self.title = title
        self.brand = brand
        self.description = description
        self.currency = currency
        self.price = price
        self.unit_price = unit_price
        self.unit = unit
        self.size = size
        self.delivery_days = delivery_days
        self.ingredients = ingredients
        self.origin = origin
        self.supplier = supplier
        self.expiration = expiration
        self.nutrition_data = self.Nutrition(energy_kj, energy_kcal, fat,
                              saturated_fatty_acids, monounsaturated_fatty_acids, polyunsaturated_fatty_acids,
                              carbohydrates, sugars, dietary_fiber, protein, sodium)

    def get_as_list(self):
        return [self.id, self.path, self.title, self.brand, self.description, self.currency, self.price, self.unit_price, self.unit, self.size, self.delivery_days, self.ingredients, self.origin, self.supplier, self.expiration, self.nutrition_data]

    def get_as_dict(self):
        self.nutrition_data.get_as_dict()
        return {
            "id": self.id,
            "path": self.path,
            "title": self.title,
            "brand": self.brand,
            "description": self.description,
            "currency": self.currency,
            "price": self.price,
            "unit_price": self.unit_price,
            "unit": self.unit,
            "size": self.size,
            "delivery days": self.delivery_days,
            "ingredients": self.ingredients,
            "origin": self.origin,
            "supplier": self.supplier,
            "expiration": self.expiration,
            "nutrition data": self.nutrition_data.get_as_dict()
        }


