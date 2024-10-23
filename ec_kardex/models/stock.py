# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import pycompat,float_is_zero
from odoo.tools.float_utils import float_round
from datetime import datetime
import operator as py_operator 



class Product(models.Model):
    _inherit = "product.template"


    sale_ok = fields.Boolean('Can be Sold', default=False)


    def cost_method_name(self):
        if self.cost_method == 'standard':
            return 'Costo Estándar'
        elif self.cost_method == 'average':
            return 'Costo Promedio'
        elif self.cost_method == 'fifo':
            return 'Primera entrada,primera salida'


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        # import pdb 
        # pdb.set_trace()
        if self._context.get('purchase_product_template',False) == True:
            if view_type == 'form':
                view_id = self.env.ref('ec_kardex.product_template_form_purchase_cen_view').id
            # else:
            #     view_id = self.env.ref('membership.membership_products_tree').id
        return super(Product, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)




class ProductProduct(models.Model):
    _inherit='product.product'

    def cost_method_name(self):
        if self.cost_method == 'standard':
            return 'Costo Estándar'
        elif self.cost_method == 'average':
            return 'Costo Promedio'
        elif self.cost_method == 'fifo':
            return 'Primera entrada,primera salida'


