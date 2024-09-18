from odoo import models, api

import logging
_logger = logging.getLogger(__name__)

class CustomReplenishmentTemplateReport(models.AbstractModel):
    _inherit = 'report.stock.report_product_template_replenishment'

    @api.model
    def get_report_values(self, docids, data=None, serialize=False):
        res = super(CustomReplenishmentTemplateReport, self).get_report_values(docids, data, serialize)
        
        _logger.info(f'>>>>> FUNCIONA <<<<<')
        
        return res