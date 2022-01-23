from peewee import *
import json
import datetime

config = json.load(open("config.json"));
db = None;
if config['masterDB'] == "SQLite":
    db = SqliteDatabase(config['SQLite']['path'], pragmas={'foreign_keys': 1})
else:
    db = PostgresqlDatabase(config['PostgreSQL'])
     



class BaseModel(Model):
    class Meta:
        database = db


class CarBrand(BaseModel):
    name = CharField(unique=True, null=False)


class CarModel(BaseModel):
    name = CharField(null=False)
    brand = ForeignKeyField(CarBrand, backref='carbrand')


class Company(BaseModel):
    name = CharField(null=False)
    contact_person = CharField(null=False)
    phone = CharField(null=False)
    address = CharField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now, index=True)


class Car(BaseModel):
    brand = ForeignKeyField(CarBrand, backref='car')
    model = ForeignKeyField(CarModel, backref='car')
    price = DecimalField(decimal_places=2, constraints=[
                         Check('price > 0')], auto_round=True)
    created_at = DateTimeField(default=datetime.datetime.now, index=True)

    company = ForeignKeyField(Company)

    class Meta:
        order_by = ('created_at')
