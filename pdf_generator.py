from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.platypus import TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.rl_config import defaultPageSize


PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]


class PDFGenerator(object):

    def __init__(self, file_name):
        self.filename = file_name
        # define the pdf object
        self.doc = SimpleDocTemplate(
            self.filename, pagesize=A4, topMargin=50, bottomMargin=30,
            leftMargin=60, rightMargin=60)

        self.elements = []

        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='MainHeader',
                                       alignment=TA_CENTER, fontSize=12))
        self.styles.add(ParagraphStyle(name='EmptyStyle', alignment=TA_CENTER))

    def make_bold(self, text):
        return Paragraph('<b>' + str(text) + '</b>', self.styles['EmptyStyle'])

    def write_main_header(self):
        """
        main header section
        """
        self.elements.append(Spacer(1, 20))

        header1 = "<u><b>AMC WORK COMPLETION CERTIFICATE - FIC</b></u>"
        header2 = "<u><b>Contract No. NO.516/FIC/AMC/401- 404/14-15 dated 14 Aug 14</b></u>"
        first_header = Paragraph(header1, self.styles['MainHeader'])
        second_header = Paragraph(header2, self.styles['MainHeader'])
        main_header_table = Table(
            [[first_header], [second_header]], colWidths=(580,))
        main_header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        self.elements.append(main_header_table)

    def get_photo_table(self):
        photo_table = Table([['', '']],
                rowHeights=(120,),
                colWidths=(218, 217))
        photo_table.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
        ]))
        return photo_table

    def three_col_table(self, row):
        # 3 column table
        table = Table([row],
                colWidths=(145, 145, 145))
        table.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
            ('ALIGN',(0, 0), (-1, -1), 'CENTER'),
        ]))

        return table

    def write_body(self, data, names, designations):
        rowheights = [
            20, 20, 20,
            200, 120, 20,
            20, 20, 20,
            20, 100, 20,
            20, 20, 20,
        ]

        # data = [ [self.make_bold(val) for val in row] for row in row_data]
        # photo table
        photo_table = self.get_photo_table()
        data.insert(4, ['Photo attachment', photo_table])

        # 3 column section
        customer_sign = self.three_col_table(['', 'Customer Sign', ''])
        data.insert(11, ['Contractor Rep Sign', customer_sign])

        name = self.three_col_table([names[0], 'Name', names[1]])
        data.insert(12, ['Name', name])

        designation = self.three_col_table(
            [designations[0], 'Designation', designations[1]])
        data.insert(13, ['Designation', designation])

        date_seal = self.three_col_table(['', 'Date / Seal', ''])
        data.insert(14, ['Date / Seal', date_seal])

        body_table = Table(data,
                splitByRow=True,
                rowHeights=rowheights,
                colWidths=(145, 435))

        body_table.setStyle(TableStyle([
            ('ALIGN',(0, 0), (-1, -1), 'CENTER'),
            ('VALIGN',(0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING',(0, 0), (-1, -1), 5),
            ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
            ('BOX', (0,0), (-1, -1), 0.25, colors.black),
        ]))
        self.elements.append(Spacer(1, 12))
        self.elements.append(body_table)

    def write_pdf(self):
        self.doc.build(self.elements)
        return self.filename
