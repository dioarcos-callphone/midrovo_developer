from odoo import api, models
from odoo.exceptions import ValidationError
from datetime import datetime

class ReportProductCatalog(models.AbstractModel):
    _name = 'report.product_catalog_advanced.product_catalog_template'
    _description = 'Report Product Catalog'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        productos = data['productos']     
            
        if productos:
            return {
                'doc_ids': docids,
                'doc_model': 'report.product_catalog_advanced.product_catalog_template',
                'options': productos,
            }
            
        else:
            raise ValidationError("¡Revise que los productos tengan talla color y cantidad!")