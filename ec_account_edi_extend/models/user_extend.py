from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class UserExtend(models.Model):
    _inherit = 'res.users'
    
    printer_default_id = fields.Many2one(
        'sri.printer.point',
        u'Emisión por Defecto',
        required=False,
        index=True,
        auto_join=True,
    )
    
    filter_orders = fields.Boolean(
        u'Mostrar Solo pedidos de su Establecimiento?',
        readonly=False, 
    )
    
    
