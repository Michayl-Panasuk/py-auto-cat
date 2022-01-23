from ast import Str
import json
from os import name
from peewee import chunked
from pathlib import Path
from playhouse import shortcuts

import automotive_models as m


def fetch_json(fileName: Str):
    directoryPath = str(Path(__file__).parent.absolute())
    return json.load(open(f"{directoryPath}/{fileName}.json"))


def check_and_run_seeds():
    brandsCount = m.CarBrand.select().count()
    modelsCount = m.CarModel.select().count()
    carsCount = m.Car.select().count()

    if brandsCount == 0 and modelsCount == 0 and carsCount == 0:
        brandsData = fetch_json('brands')
        modelsData = fetch_json('models')
        companiesData = fetch_json('companies')
        carsData = fetch_json('cars')
        with m.db.atomic():
            m.CarBrand.insert_many(brandsData).execute()
            m.CarModel.insert_many(modelsData).execute()
            m.Company.insert_many(companiesData).execute()
            m.Car.insert_many(carsData).execute()
