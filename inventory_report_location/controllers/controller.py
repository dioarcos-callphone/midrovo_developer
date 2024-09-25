from odoo import http
from odoo.http import request

class ProductReportController(http.Controller):

    @http.route('/product/pdf_report', type='http', auth='public' csrf=False)
    def pdf_report(self, **kwargs):
        products = request.env['product.product'].search([])  # O puedes aplicar un dominio
        return products.action_pdf()
