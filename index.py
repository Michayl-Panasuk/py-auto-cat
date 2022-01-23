
from tkinter import *
import ui as AppUi
import automotive_models as m
import seeds.index as seed
import controller as ctrl

def check_initials():
    m.db.connect()
    m.db.create_tables(
        [m.CarBrand, m.CarModel, m.Company, m.Car], safe=True)
    seed.check_and_run_seeds()
    m.db.close()


check_initials()

if __name__ == '__main__':
    window = Tk()
    application = AppUi.App(window, ctrl.MainCtrl(m.db))
    window.mainloop()
