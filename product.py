from dict_value import get_value, get_list


class Product:

    class Nutrition:
        def __init__(self, output):
            energy_kj, energy_kcal = get_list("energy", output, "/\n")
            self.energy_kj = energy_kj.strip() if energy_kj is not None else None
            self.energy_kcal = energy_kcal.strip() if energy_kcal is not None else None
            self.fat = get_value("fat", output)
            self.saturated_fatty_acids = get_value("saturated_fatty_acids", output)
            self.monounsaturated_fatty_acids = get_value("monounsaturated_fatty_acids", output)
            self.polyunsaturated_fatty_acids = get_value("polyunsaturated_fatty_acids", output)
            self.carbohydrates = get_value("carbohydrates", output)
            self.sugars = get_value("sugars", output)
            self.dietary_fiber = get_value("dietary_fiber", output)
            self.protein = get_value("protein", output)
            self.salt = get_value("salt", output)
            self.sodium = get_value("sodium", output)

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
                "salt": self.salt,
                "sodium": self.sodium
            }

    def __init__(self, id, category, path, title, extra_details, brand, description, currency, price, unit_price, unit,
                 output):
        self.id = id
        self.category = category
        self.path = path
        self.title = title
        self.extra_details = extra_details
        self.brand = brand
        self.description = description
        self.currency = currency
        self.price = price
        self.unit_price = unit_price
        self.unit = unit
        self.size = get_value("size", output)
        self.delivery_days = get_value("delivery_days", output)
        self.ingredients = get_value("ingredients", output)
        self.country_of_origin = get_value("country_of_origin", output)
        self.place_of_origin = get_value("place_of_origin", output)
        self.supplier = get_value("supplier", output)
        self.expiration = get_value("expiration", output)
        self.pant = get_value("pant", output)
        self.storage = get_value("storage", output)
        self.variable_weight = get_value("variable_weight", output)
        self.characteristics = get_value("characteristics", output)
        self.extra_tender = get_value("extra_tender", output)
        self.requirements = get_value("requirements", output)
        self.nutrition_data = self.Nutrition(output)

    def get_as_dict(self):
        nutrition_data = self.nutrition_data.get_as_dict()
        prod_data = {
            "id": self.id,
            "category": self.category,
            "path": self.path,
            "title": self.title,
            "extra_details": self.extra_details,
            "brand": self.brand,
            "description": self.description,
            "currency": self.currency,
            "price": self.price,
            "unit_price": self.unit_price,
            "unit": self.unit,
            "size": self.size,
            "delivery_days": self.delivery_days,
            "ingredients": self.ingredients,
            "country_of_origin": self.country_of_origin,
            "place_of_origin": self.place_of_origin,
            "supplier": self.supplier,
            "expiration": self.expiration,
            #"nutrition data": self.nutrition_data.get_as_dict(),
            "pant": self.pant,
            "storage": self.storage,
            "variable_weight": self.variable_weight,
            "extra_tender": self.extra_tender,
            "characteristics": self.characteristics,
            "requirements": self.requirements
        }
        for key in nutrition_data.keys():
            prod_data[key] = nutrition_data[key]
        return prod_data

