# -*- coding: utf-8 -*-
from odoo import models, fields, registry, api
import logging
_logger = logging.getLogger(__name__)


class WizardProductDefaultTax(models.TransientModel):
    '''
    Asistente para asignar impuestos por Defecto
    '''
    _name = 'wizard.product.default.tax'
    _description = 'Asistente para asignar impuestos por Defecto'
    
    sale_tax_ids = fields.Many2many('account.tax', 'wizard_sale_tax_rel', 
                                    'wizard_id', 'tax_id', string=u'Impuestos en Ventas', domain=[('type_tax_use', '=', 'sale')])  
    purchase_tax_ids = fields.Many2many('account.tax', 'wizard_purchase_tax_rel', 
                                    'wizard_id', 'tax_id', string=u'Impuestos en Compras', domain=[('type_tax_use', '=', 'purchase')])
    
    def process_tax_change(self):
        ivalue_model = self.env['ir.values']
        company = self.env.user.company_id
        if self.sale_tax_ids:
            taxes_id = ivalue_model.search([
                ('name', '=', 'taxes_id'),
                ('model', '=', 'product.template'),
                                       ])
            if taxes_id:
                taxes_id.unlink()
            ivalue_model.sudo().set_default('product.template', "taxes_id", self.sale_tax_ids.ids, for_all_users=True, company_id=company.id)
        if self.purchase_tax_ids:
            supplier_taxes_id = ivalue_model.search([
                ('name', '=', 'supplier_taxes_id'),
                ('model', '=', 'product.template'),
                                       ])
            if supplier_taxes_id:
                supplier_taxes_id.unlink()
            ivalue_model.sudo().set_default('product.template', "supplier_taxes_id", self.purchase_tax_ids.ids, for_all_users=True, company_id=company.id)
        return {'type': 'ir.actions.act_window_close'}
