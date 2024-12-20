from odoo import models, fields, api

class UserExtend(models.Model):
    _inherit = 'res.users'
    
    printer_default_id = fields.Many2one(
        'sri.printer.point',
        u'Punto de Emisión',
        required=False,
        index=True, auto_join=True,
        domain= lambda self: self._domain_printer_point_ids()
    )
    
    
    @api.depends('shop_ids')
    def _domain_printer_point_ids(self):
        printer_point_ids = []
        for record in self:
            for shop_id in record.shop_ids:
                if shop_id.printer_point_ids:
                    for printer_point_id in shop_id.printer_point_ids:
                        printer_point_ids.append(printer_point_id.id)
                        
        return [('id', 'in', printer_point_ids)]
    
