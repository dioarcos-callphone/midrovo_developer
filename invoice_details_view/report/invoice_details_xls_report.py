from odoo import models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class InvoiceDetailsXlsxReport(ReportXlsx):
    
    def generate_xlsx_report(self, workbook, data, invoices):
        sheet = workbook.add_worksheet('Detalles de Factura')
        bold = workbook.add_format({'bold': True})

        # Cabeceras de las columnas
        sheet.write(0, 0, 'Factura', bold)
        sheet.write(0, 1, 'Comercial', bold)
        sheet.write(0, 2, 'Producto', bold)
        sheet.write(0, 3, 'Cantidad', bold)
        sheet.write(0, 4, 'Precio', bold)
        sheet.write(0, 5, 'Total', bold)

        # Añadir datos
        row = 1
        for detail in data['options']:  # Usar 'options' que viene del _get_report_values
            sheet.write(row, 0, detail['numero'])
            sheet.write(row, 1, detail['comercial'])
            sheet.write(row, 2, detail['producto'])
            sheet.write(row, 3, detail['cantidad'])
            sheet.write(row, 4, detail['precio'])
            sheet.write(row, 5, detail['costo'])
            row += 1

InvoiceDetailsXlsxReport('report.invoice_details_view.report_invoice_details_xlsx', 'account.move')
