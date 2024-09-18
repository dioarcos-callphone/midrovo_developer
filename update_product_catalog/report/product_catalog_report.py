from odoo import models, api
from odoo.exceptions import ValidationError

class ProductCatalogReport(models.AbstractModel):
    _name = 'report.amf_product_catalog.report_product_template_catalog'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['product.template'].browse(docids)
        
        if len(docs) > 10:
            raise ValidationError('Solo se permite generar 140 productos en el catálogo.')

        for doc in docs:
            if doc.qty_available <= 0:
                raise ValidationError('Uno o más productos seleccionados no tienen stock disponible. Por favor, desmarca los productos con stock cero antes de generar el informe.')
        

        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': docs,
        }
