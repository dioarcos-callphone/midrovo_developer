from odoo import models, api
from odoo.exceptions import UserError

class ProductCatalogReport(models.AbstractModel):
    _name = 'report.amf_product_catalog.report_product_template_catalog'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['product.template'].browse(docids)
        # Validación de productos con cantidad cero
        for doc in docs:
            if doc.qty_available <= 0:
                raise UserError('Uno o más productos seleccionados no tienen stock disponible. Por favor, desmarca los productos con stock cero antes de generar el informe.')
        
        # Si pasa la validación, continuar con el flujo normal de generación del reporte
        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': docs,
        }
