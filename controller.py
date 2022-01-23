import automotive_models as m


class MainCtrl:
    db: m.db

    def __init__(self, db):
        self.db = db

    def get_all_brands(self):
        return m.CarBrand.select()

    def get_all_models(self):
        return m.CarModel.select()

    def get_all_companies(self):
        return m.Company.select()

    def get_cars(self):
        return m.Car.select()
    
    def get_car_by_id(self, id):
        return m.Car.get_by_id(id)

    def create_car(self, newCar):
        return m.Car.create(**newCar)

    def delete_car(self, car_id):
        return m.Car.delete_by_id(car_id)
    
    def update_car(self, car_id, body):
        return m.Car.update(**body).where(m.Car.id == car_id).execute()
