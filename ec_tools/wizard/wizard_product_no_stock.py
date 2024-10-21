# -*- encoding: utf-8 -*-

from odoo import models, api, fields
import odoo.addons.decimal_precision as dp


class WizardProductNoStock(models.TransientModel):

    _name = 'wizard.product.no.stock'
    _description = u'Productos de producción sin stock'
    
    line_ids = fields.One2many('wizard.product.no.stock.detail', 'wizard_id', u'Productos sin stock', required=False, )


class WizardProductNoStockDetail(models.TransientModel):

    _name = 'wizard.product.no.stock.detail'
    _description = u'Detalle de productos de producción sin stock'
    
    wizard_id = fields.Many2one('wizard.product.no.stock', u'Asistente', 
        required=False, ondelete="cascade", )
    product_id = fields.Many2one('product.product', u'Producto', 
        required=False, )
    product_qty = fields.Float(u'Cantidad Requerida', digits=dp.get_precision('Product Unit of Measure'), )
    qty_available = fields.Float(u'Cantidad Disponible', digits=dp.get_precision('Product Unit of Measure'), )
    uom_id = fields.Many2one('product.uom', u'UdM', 
        required=False, )
    location_id = fields.Many2one('stock.location', u'Bodega', required=False, )
    lot_id = fields.Many2one('stock.production.lot', u'Lote de Producción', required=False, )
