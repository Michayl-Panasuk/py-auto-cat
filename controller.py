import json
from peewee import *
from typing import Dict, IO
from playhouse import shortcuts;
from operator import attrgetter;
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

    def get_cars(self, filterParams: Dict=None, sort=None):
        composedQ = m.Car.select();
        if filterParams and len(helpers.filterNoneInDict(filterParams).items()):
            cleanFilter = helpers.filterNoneInDict(filterParams);
            composedQ = composedQ.where(*[getattr(m.Car, k) == v for k, v in cleanFilter.items()])
        if sort:
            sortEntry = list(sort.items())[0];
            if sortEntry[1] == 'DESC':
               composedQ = composedQ.order_by(SQL(sortEntry[0]).desc())
            else:
               composedQ = composedQ.order_by(SQL(sortEntry[0]).asc())

        return composedQ;
    
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
        toDrop.reverse();
        with m.db.atomic():
            for entry in toDrop:
                entry[0].delete().execute();

            toInsert = json.load(file);
        
            for entry in self.entities:
                entry[0].insert_many(toInsert[entry[1]]).execute();
        file.close();
        return file;