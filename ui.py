from tkinter import ttk  # підключаємо модуль інтерфейсів
from tkinter import *
from typing import Any, List

from peewee import ModelSelect

import controller
import validators

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def items_to_names(items):
    newArr = []
    for item in items:
        newArr.append(item.name)
    return newArr


def filterArr(items, predicate):
    newArr = []
    i = 0
    for item in items:
        if predicate(item):
            newArr.append(item.name)
        i += 1
    return newArr


def findInArray(items, predicate):
    i = 0
    for item in items:
        if predicate(item):
            return item
        i += 1
    return

class CarForm:
    brandModel: StringVar
    carModelModel: StringVar
    companyModel: StringVar
    # Controls
    brandCtrl: OptionMenu
    modelCtrl: OptionMenu
    companyCtrl: OptionMenu
    priceCtrl: Entry


class App:
    ctrl: controller.MainCtrl
    frame: Frame
    tree: ttk.Treeview
    brandModel: StringVar
    carModelModel: StringVar
    companyModel: StringVar
    brandCtrl: OptionMenu
    modelCtrl: OptionMenu
    companyCtrl: OptionMenu
    priceCtrl: Entry
    cars: Any
    brands: Any
    models: Any
    companies: Any

    def __init__(self, window, ctrl: controller.MainCtrl):
        # s = ttk.Style()
        # s.configure('TMenubutton', background='green')
        # Запуск вікна
        self.wind = window
        self.ctrl = ctrl
        self.wind.title('List')

        self.get_initial_data()
        self.create_form_widgets()
        self.create_table_widget()
        self.create_misc_widgets()
        self.fill_cars_table()
       

    def create_form_widgets(self):
        # Створюємо фрейм
        self.frame = LabelFrame(self.wind, text='Add new car')
        self.frame.grid(row=0, column=0, columnspan=3, pady=20)

        # # Brand Input
        Label(self.frame, text='Brand: ').grid(row=1, column=0)
        self.brandModel = StringVar(self.frame)
        self.brandCtrl = OptionMenu(self.frame, self.brandModel, *items_to_names(
            self.brands), command=lambda *args: self.update_options_list(self.modelCtrl, self.carModelModel, self.pick_car_models(self.brandModel)))
        self.brandCtrl.grid(row=1, column=1)
        

        # Model Input
        Label(self.frame, text='Model: ').grid(row=2, column=0)
        self.carModelModel = StringVar(self.frame)
        self.modelCtrl = OptionMenu(
            self.frame, self.carModelModel, *['Select Brand'])
        self.modelCtrl.grid(row=2, column=1)

        # Company Input
        Label(self.frame, text='Company: ').grid(row=3, column=0)
        self.companyModel = StringVar(self.frame)
        self.companyCtrl = OptionMenu(
            self.frame, self.companyModel, *items_to_names(self.companies))
        self.companyCtrl.grid(row=3, column=1)

        # Pirce Input
        Label(self.frame, text='Price: ').grid(row=4, column=0)
        self.priceCtrl = Entry(self.frame)
        self.priceCtrl.grid(row=4, column=1)

    def create_table_widget(self):
        # Table
        columns = ('id', 'brand_name', 'model_name', 'company_name', 'price')
        self.tree = ttk.Treeview(height=10, columns=columns)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('id', text='Id', anchor=CENTER)
        self.tree.heading('brand_name', text='Brand', anchor=CENTER)
        self.tree.heading('model_name', text='Model', anchor=CENTER)
        self.tree.heading('company_name', text='Company', anchor=CENTER)
        self.tree.heading('price', text='Price', anchor=CENTER)

        # Buttons
        ttk.Button(text='Delete', command=self.delete_product).grid(
            row=5, column=0, sticky=W + E)
        ttk.Button(text='Edit', command=self.edit_product).grid(
            row=5, column=1, sticky=W + E)

    def create_misc_widgets(self):
        # Button Add Product
        ttk.Button(self.frame, text='Save', command=self.add_car).grid(
            row=5, columnspan=2, sticky=W + E)

        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

    def get_initial_data(self):
        self.cars = self.ctrl.get_cars()
        self.brands = self.ctrl.get_all_brands()
        self.models = self.ctrl.get_all_models()
        self.companies = self.ctrl.get_all_companies()

    # Get Products from Database
    def fill_cars_table(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        mapped = []
        for row in self.ctrl.get_cars():
            mapped.append((row.id, row.brand.name, row.model.name,
                          row.company.name, row.price))

        # filling data
        for row in mapped:
            self.tree.insert('', 0, values=row)

    # User Input Validation
    def check_form(self, form):
        fValue = self.pick_form_value(form);
        for k in ('model', 'brand', 'company'):
            if len(fValue[k]) == 0:
                return False
        if fValue['price'] <= 0:
             return False
        return True

   

    def add_car(self):
        if self.check_form(self):
            
            fValue = self.normalize_form_value(self.pick_form_value(self));

            self.ctrl.create_car(fValue)

            self.message['text'] = 'Авто успешно добавлено'
            # self.name.delete(0, END)
            self.priceCtrl.delete(0, END)
        else:
            self.message['text'] = 'Заполните поля Brand, Model, Company, Price'
        self.fill_cars_table()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Select car in list'
            return
        self.message['text'] = ''
        car_id = self.tree.item(self.tree.selection())['values'][0];
        self.ctrl.delete_car(car_id)
        self.message['text'] = 'Record {} deleted Successfully'.format(car_id)
        self.fill_cars_table()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Выберите запись в таблице'
            return

        # name = self.tree.item(self.tree.selection())['text']
        # old_price = self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit car'

        car = self.tree.item(self.tree.selection())['values'];


        carForm = self.create_edit_car_form(self.edit_wind, {
            'brand': car[1],
            'model': car[2],
            'company': car[3],
            'price': car[4],
        })

        Button(self.edit_wind, text='Update', command= lambda *args: self.submit_edit_car(car[0], carForm, self.edit_wind)).grid(row=5, column=0, sticky=W)
        Button(self.edit_wind, text='Canell', command= lambda *args:  self.edit_wind.destroy()).grid(row=5, column=1, sticky=W)

        self.edit_wind.mainloop()

    def submit_edit_car(self, carId, carForm, modal):
        carValue = self.normalize_form_value(self.pick_form_value(carForm))
        self.ctrl.update_car(carId, carValue)
        modal.destroy()
        # self.run_query(query, parameters)
        # self.edit_wind.destroy()
        # self.message['text'] = 'Запись {} успшено обновлена'.format(name)
        # self.fill_cars_table()

    def pick_car_models(self, brandModel):
        newBrand = brandModel.get()
        selectedBrand = findInArray(
            self.brands, lambda item: item.name == newBrand)
        newModelsList = filterArr(self.models, lambda item: item.brand.id == selectedBrand.id)

        return newModelsList



    def update_options_list(self, control: OptionMenu, model: StringVar, newOptions: List):
        menu = control['menu']
        menu.delete(0, 'end')
        for string in newOptions:
            menu.add_command(label=string,
                             command=lambda value=string: model.set(value))

    def create_edit_car_form(self, host, car=None, form: CarForm=CarForm()):

         # # Brand Input
        Label(host, text='Brand: ').grid(row=1, column=0)
        form.brandModel = StringVar(host)
        form.brandCtrl = OptionMenu(host, form.brandModel, *items_to_names(
            self.brands), command=lambda *args: self.update_options_list(form.modelCtrl, form.carModelModel, self.pick_car_models(form.brandModel)))
        form.brandCtrl.grid(row=1, column=1)

        # Model Input
        Label(host, text='Model: ').grid(row=2, column=0)
        form.carModelModel = StringVar(host)
        form.modelCtrl = OptionMenu(
            host, form.carModelModel, *['Select Brand'])
        form.modelCtrl.grid(row=2, column=1)

        # Company Input
        Label(host, text='Company: ').grid(row=3, column=0)
        form.companyModel = StringVar(host)
        form.companyCtrl = OptionMenu(
            host, form.companyModel, *items_to_names(self.companies))
        form.companyCtrl.grid(row=3, column=1)

        # Pirce Input
        Label(host, text='Price: ').grid(row=4, column=0)
        form.priceCtrl = Entry(host)
        form.priceCtrl.grid(row=4, column=1)

        if car:
          form.brandModel.set(car['brand'])
          form.companyModel.set(car['company'])
          self.update_options_list(form.modelCtrl, form.carModelModel, self.pick_car_models(form.brandModel))
          form.carModelModel.set(car['model'])
          form.priceCtrl.delete(0,END)
          form.priceCtrl.insert(0, car['price'])

        return form;

    def pick_form_value(self, carForm):
        rawValue = {
            'brand': carForm.brandModel.get(),
            'model': carForm.carModelModel.get(),
            'company': carForm.companyModel.get(),
            'price': safe_cast(carForm.priceCtrl.get(), int, 0)
        }
        return rawValue;

    def normalize_form_value(self, rawValue):
        fValue = {
            'brand': findInArray(self.brands, lambda item: item.name == rawValue['brand']).id,
            'model': findInArray(self.models, lambda item: item.name == rawValue['model']).id,
            'company': findInArray(self.companies, lambda item: item.name == rawValue['company']).id,
            'price': rawValue['price']
        }
        return fValue;

          
          


