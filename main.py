import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow
from money_document import MoneyDocumentView
from models import AmountDocument
import models
from models import create_debug_engine, create_session, print_session
import os
import codecs
if os.name == 'nt':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def register(obj):
    models.SESSION.add(obj)


def commit():
    models.SESSION.commit()


def rollback():
    models.SESSION.rollback()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionQuit.triggered.connect(self.quit_application)
        self.ui.actionMoney.triggered.connect(self.add_money_document)

    def quit_application(self, event):
        app.quit()

    def add_money_document(self, event):
        doc = AmountDocument(1000, ["Ivanov", "Петров", "Lee"])
        register(doc)
        self.view_for_document(doc)

    def view_for_document(self, doc):
        doc_dial = MoneyDocumentView(doc)
        doc.amount += 1000
        doc_dial.update()
        rc = doc_dial.exec_()
        print("Now document amount is", doc.amount)
        # if rc:
        #    print("Create Document and save it somwhere")
        #    print("Создать документ")


if __name__ == '__main__':

    # import pudb
    #  pu.db

    de = create_debug_engine(True)
    create_session(de)

    print(models.SESSION)

    app = QApplication(sys.argv)

    w = ApplicationWindow()
    w.show()

    app.exec_()

    commit()
    # quit()
    del w
    del app
