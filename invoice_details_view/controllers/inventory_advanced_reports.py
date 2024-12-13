from odoo import http
from odoo.http import request

class InvoiceDetailsController(http.Controller):

    @http.route('/report/invoice_details', type='http', auth='user', methods=['GET'])
    def download_excel(self, wizard_id, **kwargs):
        wizard = request.env['invoice.details.wizard'].browse(int(wizard_id))
        xlsx_data = wizard.get_xlsx_report()

        # Establecer los encabezados para la descarga del archivo
        file_name = 'informe_detalles_facturas.xlsx'
        headers = [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', 'attachment; filename=%s' % file_name)
        ]

        return request.make_response(xlsx_data, headers=headers)