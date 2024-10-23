# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import pycompat, float_is_zero
from odoo.tools.float_utils import float_round
from datetime import datetime
import operator as py_operator


class KardexReportRegLines(models.Model):
    _name = "kardex.report.reg.lines"

    name = fields.Char(u'Doc. origen')
    partner = fields.Char(u'Usuario')
    ref = fields.Char(u'Referencia')
    description = fields.Char(u'Descripcion')
    costs = fields.Char(u'Costo und.',digits=(12, 4))
    total = fields.Char(u'Total',digits=(12, 4))
    type = fields.Char(u'Tipo')
    income = fields.Float(u'Entrada')
    outcome = fields.Float(u'Salida')
    value = fields.Float(u'Saldo')
    cost_balance = fields.Float(u'Costo x Saldo')
    reg_id = fields.Many2one('kardex.report.reg', 'Kardex Registration')


class KardexReportReg(models.Model):
    _name = "kardex.report.reg"
    _rec_name = "product_id"

    product_id = fields.Many2one('product.product', u'Producto', required=False, help=u"", )
    location_id = fields.Many2one('stock.location', u'Ubicación', required=False, help=u"",
                                  domain=[('usage', '=', 'internal')])
    date_from = fields.Date(u'Desde', help=u"", )
    date_to = fields.Date(u'Hasta', help=u"", )
    show_costs = fields.Boolean("Mostrar costos?", default=False)
    lines_ids = fields.One2many('kardex.report.reg.lines', 'reg_id', u'Lineas')


    def _get_context_for_report(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({'product_id': self.product_id.id,
                    'location_id': self.location_id.id,
                    'location_name': self.location_id.name,
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'show_costs': self.show_costs,
                    })
        return ctx

    def action_print_report(self):
        company = self.env.user.company_id
        ctx = self._get_context_for_report()
        ctx['active_model'] = 'res.company' 
        ctx['active_ids'] = [company.id]
        ctx['active_id'] = company.id
        report_name = self.env.ref("ec_kardex.kardex_individual_report")
        return report_name.with_context(ctx).report_action(self, data=ctx, config=False)

    def get_report_data_xls(self):
        report_model = self.env['report.stock.utils']
        ctx = self._get_context_for_report()
        return report_model.with_context(ctx).MakeReportxls()

    def action_get_report(self):
        res = {'type': 'ir.actions.act_url',
               'url': '/download/saveas?model=%(model)s&record_id=%(record_id)s&method=%(method)s&filename=%(filename)s' % {
                   'filename': u'Análisis.xlsx',
                   'model': self._name,
                   'record_id': self.id,
                   'method': 'get_report_data_xls',
               },
               'target': 'self',
               }

        return res