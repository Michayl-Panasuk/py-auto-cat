import json
from typing import IO

from playhouse import shortcuts;
import automotive_models as m
import helpers;

class MainCtrl:
    db: m.db;
    entities = [(m.CarBrand, 'brands'), (m.CarModel, 'models'), (m.Company, 'companies'), (m.Car, 'cars')]

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


    def export_from_current_db(self, file: IO):

        toDump = {};
        for entry in self.entities:
            toDump[entry[1]] = list(map(lambda item: shortcuts.model_to_dict(item, recurse=False), entry[0].select()))

        file.write(json.dumps(toDump, default=str))
        file.close();
        return file;

    def import_to_current_db(self, file: IO):
        toDrop = self.entities[:];
        toDrop.reverse()
        with m.db.atomic():
            for entry in toDrop:
                entry[0].delete().execute();

            toInsert = json.load(file);
        
            for entry in self.entities:
                entry[0].insert_many(toInsert[entry[1]]).execute();
        file.close();

        return file;
            


        
        


# brandsCount = m.CarBrand.select().count()
#     modelsCount = m.CarModel.select().count()
#     carsCount = m.Car.select().count()

    # if brandsCount == 0 and modelsCount == 0 and carsCount == 0:
    #     brandsData = fetch_json('brands')
    #     modelsData = fetch_json('models')
    #     companiesData = fetch_json('companies')
    #     carsData = fetch_json('cars')
    #     with m.db.atomic():
    #         m.CarBrand.insert_many(brandsData).execute()
    #         m.CarModel.insert_many(modelsData).execute()
    #         m.Company.insert_many(companiesData).execute()
    #         m.Car.insert_many(carsData).execute()