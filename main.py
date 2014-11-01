#-*- coding: utf-8 -*-

import datetime
import sqlite3
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

from pdf_generator import PDFGenerator


qt_app = QApplication(sys.argv)
conn = sqlite3.connect('amc.db')

# Create table - only once
table_creation_query = """
    create table certificate
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     wcc VARCHAR(30) NOT NULL,
     document_date DATE NOT NULL,
     nature_of_work VARCHAR(30),
     routines TEXT,
     parts_replaced VARCHAR(200),
     spares_supplied_by VARCHAR(30),
     invoice_details VARCHAR(30),
     requirment_oem VARCHAR(5),
     oem_service_report VARCHAR(30),
     customer_remark TEXT,
     customer_name VARCHAR(30),
     customer_designation VARCHAR(50),
     contractor_name VARCHAR(30),
     contractor_designation VARCHAR(50)
    );
"""
#conn.execute(table_creation_query)
#conn.close()
#sys.exit(0)


class CertificateGenerator(QWidget):
    ''' This class will generate a AMC completion pdf certificate.'''

    def __init__(self):
        # Initialize the object as a QWidget and
        # set its title and minimum width
        QWidget.__init__(self)
        self.setWindowTitle('AMC Certificate Generator')
        self.setMinimumWidth(500)

        # Create the QVBoxLayout that lays out the whole form
        self.layout = QVBoxLayout()

        # Create the form layout that manages the labeled controls
        self.form_layout = QFormLayout()

        # wcc - auto fill; create a textbox and add it to form layout
        self.wcc = QLineEdit(self)
        result = conn.execute('select count(id) from certificate')
        conn_id = result.fetchone()[0]
        self.wcc.setText("FIC/{0}/2014-15".format(conn_id + 1))
        self.form_layout.addRow('WCC:', self.wcc)

        # DATE: system date / user chosen date;
        # create a textbox and add it to form layout
        self.input_date = QCalendarWidget(self)
        self.form_layout.addRow('DATE:', self.input_date)

        # The salutations that we want to make available
        self.work_type = ['Daily',
                          'Weekly',
                          'Monthly',
                          'Other Routines',
                          'Defect Rectification']

        # Create and fill the combo box to choose the salutation
        # And Add it to the form layout with a label
        self.nature_of_work = QComboBox(self)
        self.nature_of_work.addItems(self.work_type)
        self.form_layout.addRow('Nature of work:', self.nature_of_work)

        # Routines carried out
        # service report - contractor's engineer 10 lines
        self.routines = QTextEdit(self)
        self.form_layout.addRow('Routines Carried Out:', self.routines)

        # Parts Replaced
        self.parts_replaced = QLineEdit(self)
        self.form_layout.addRow('Parts Replaced:', self.parts_replaced)

        # Spares Supplied By
        self.suppliers = ['Navy' , 'Contractor']
        self.spares = QComboBox(self)
        self.spares.addItems(self.suppliers)
        self.form_layout.addRow('Spares Supplied By:', self.spares)

        # Invoice Details
        self.invoice = QLineEdit(self)
        self.form_layout.addRow('Invoice Details:', self.invoice)

        # Requirement of OEM
        self.boolean = ['Yes' , 'No']
        self.oem = QComboBox(self)
        self.oem.addItems(self.boolean)
        self.form_layout.addRow('Requirement of OEM:', self.oem)

        # OEM service report
        self.service = QLineEdit(self)
        self.form_layout.addRow('OEM Service Report:', self.service)

        # Customer Remark
        self.remark = QTextEdit(self)
        self.form_layout.addRow('Customer Remark:', self.remark)

        # contractor name
        self.contractor_name = QLineEdit(self)
        self.form_layout.addRow('Contractor Name:', self.contractor_name)
        # contractor designation
        self.contractor_desig = QLineEdit(self)
        self.form_layout.addRow('Contractor Designation:',
                self.contractor_desig)

        # customer name
        self.customer_name = QLineEdit(self)
        self.form_layout.addRow('Customer Name:', self.customer_name)
        # customer designation
        self.customer_desig = QLineEdit(self)
        self.form_layout.addRow('Customer Designation:',
                self.customer_desig)

        # Add the form layout to the main VBox layout
        self.layout.addLayout(self.form_layout)

        # Add stretch to separate the form layout from the button
        self.layout.addStretch(1)

        # Create a horizontal box layout to hold the button
        self.button_box = QHBoxLayout()

        # Add stretch to push the button to the far right
        self.button_box.addStretch(1)

        # Create the build button with its caption
        self.build_button = QPushButton('Generate Certificate', self)

        # Add it to the button box
        self.button_box.addWidget(self.build_button)

        # Add the button box to the bottom of the main VBox layout
        self.layout.addLayout(self.button_box)

        # Set the VBox layout as the window's main layout
        self.setLayout(self.layout)

        # listen to button click
        self.build_button.clicked.connect(self.clicked_slot)

    def generate_report(self, wcc):
        cur = conn.execute(
            "select * from certificate where wcc='{0}'".format(wcc))
        result = cur.fetchone()
        pdf = PDFGenerator('amc_certificate_{0}.pdf'.format(result[0]))
        pdf.write_main_header()
        row_headers = [
            'WCC', 'DATE', 'Nature of work', 'Routines carried out',
            'Parts Replaced', 'Spares supplied by',
            'Invoice details', 'Requirement of OEM', 'OEM service report',
            'Customer remark'
        ]
        data_column = [result[1], result[2], result[3], result[4], result[5],
            result[6], result[7], result[8], result[9], result[10]]

        names = [result[13], result[11]]
        designations = [result[14], result[12]]

        data = zip(row_headers, data_column)
        pdf.write_body(data, names, designations)
        file_name = pdf.write_pdf()
        print file_name
        return file_name

    @Slot()
    def clicked_slot(self):
        ''' This is called when the button is clicked. '''
        wcc = self.wcc.text()
        document_date = self.input_date.selectedDate()
        nature_of_work = self.work_type[self.nature_of_work.currentIndex()]
        routines = self.routines.toPlainText()
        parts_replaced = self.parts_replaced.text()
        spares_supplied_by = self.suppliers[self.spares.currentIndex()]
        invoice_details = self.invoice.text()
        requirment_oem = self.boolean[self.oem.currentIndex()]
        oem_service_report = self.service.text()
        customer_remark = self.remark.toPlainText()
        customer_name = self.customer_name.text()
        customer_designation = self.customer_desig.text()
        contractor_name = self.contractor_name.text()
        contractor_designation = self.contractor_desig.text()

        values_list = [wcc, document_date.toPython(), nature_of_work, routines,
            parts_replaced, spares_supplied_by, invoice_details,
            requirment_oem, oem_service_report, customer_remark,
            customer_name, customer_designation, contractor_name,
            contractor_designation]

        cleaned_values_list = ["'" + str(v) + "'"  if v else "' '" for v in values_list]

        insert_command = """insert into certificate
            (wcc, document_date, nature_of_work, routines, parts_replaced,
            spares_supplied_by, invoice_details, requirment_oem,
            oem_service_report, customer_remark, customer_name,
            customer_designation, contractor_name, contractor_designation)
            VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10},
            {11}, {12}, {13})""".format(*cleaned_values_list)
        cur = conn.execute(insert_command)
        conn.commit()
        file_name = self.generate_report(wcc)
        return file_name

    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        qt_app.exec_()

# Create an instance of the application window and run it
app = CertificateGenerator()
app.run()
