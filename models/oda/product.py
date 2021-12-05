from models.dict_value import get_value, get_list, clean_str, clean_html


class Product:
    class Nutrition:
        def __init__(self, prod_data):
            energy_kj, energy_kcal = get_list("energy", prod_data, "/\n")
            self.energy_kj = energy_kj.strip() if energy_kj is not None else None
            self.energy_kcal = energy_kcal.strip() if energy_kcal is not None else None
            self.fat = get_value("fat", prod_data)
            self.saturated_fatty_acids = get_value("saturated_fatty_acids", prod_data)
            self.monounsaturated_fatty_acids = get_value("monounsaturated_fatty_acids", prod_data)
            self.polyunsaturated_fatty_acids = get_value("polyunsaturated_fatty_acids", prod_data)
            self.carbohydrates = get_value("carbohydrates", prod_data)
            self.sugars = get_value("sugars", prod_data)
            self.dietary_fiber = get_value("dietary_fiber", prod_data)
            self.protein = get_value("protein", prod_data)
            self.salt = get_value("salt", prod_data)
            self.sodium = get_value("sodium", prod_data)
            self.polyols = get_value("polyols", prod_data)
            self.starch = get_value("starch", prod_data)

        def get_data(self):
            return {
                "energy_kj": self.energy_kj,
                "energy_kcal": self.energy_kcal,
                "saturated_fatty_acids": self.saturated_fatty_acids,
                "monounsaturated_fatty_acids": self.monounsaturated_fatty_acids,
                "polyunsaturated_fatty_acids": self.polyunsaturated_fatty_acids,
                "carbohydrates": self.carbohydrates,
                "sugars": self.sugars,
                "dietary_fiber": self.dietary_fiber,
                "protein": self.protein,
                "salt": self.salt,
                "sodium": self.sodium,
                "polyols": self.polyols,
                "starch": self.starch
            }

    def __init__(self, prod_data):
        self.id = get_value("id", prod_data)
        self.category = get_value("category", prod_data)
        self.path = get_value("path", prod_data)
        self.title = get_value("title", prod_data)
        self.extra_details = get_value("extra_details", prod_data)
        self.brand = get_value("brand", prod_data)
        self.description = clean_html(get_value("description", prod_data))
        self.currency = get_value("currency", prod_data)
        self.price = get_value("price", prod_data)
        self.unit_price = get_value("unit_price", prod_data)
        self.unit = get_value("unit", prod_data)
        self.size = get_value("size", prod_data)
        self.delivery_days = get_value("delivery_days", prod_data)
        self.ingredients = clean_str(get_value("ingredients", prod_data))
        self.country_of_origin = get_value("country_of_origin", prod_data)
        self.place_of_origin = get_value("place_of_origin", prod_data)
        self.supplier = get_value("supplier", prod_data)
        self.expiration = get_value("expiration", prod_data)
        self.pant = get_value("pant", prod_data)
        self.storage = get_value("storage", prod_data)
        self.variable_weight = get_value("variable_weight", prod_data)
        self.characteristics = get_value("characteristics", prod_data)
        self.extra_tender = get_value("extra_tender", prod_data)
        self.requirements = get_value("requirements", prod_data)
        self.information = get_value("information", prod_data)
        self.active_substance = get_value("active_substance", prod_data)
        self.volume = get_value("volume", prod_data)
        self.roughness = get_value("roughness", prod_data)
        self.nutrition_data = self.Nutrition(prod_data)

    def get_data(self):
        nutrition_data = self.nutrition_data.get_data()
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
            "pant": self.pant,
            "storage": self.storage,
            "variable_weight": self.variable_weight,
            "extra_tender": self.extra_tender,
            "characteristics": self.characteristics,
            "requirements": self.requirements,
            "information": self.information,
            "volume": self.volume,
            "roughness": self.roughness
        } | nutrition_data
        return prod_data
