# -*- encoding: utf-8 -*-

import time
from datetime import datetime
from odoo import models, api, fields


class WizardEcKardexIndividualReport(models.TransientModel):

    _name = 'wizard.ec_kardex.all.report'
    _description = u'Asistente para kardex General'

    start_date = fields.Date(u'Fecha de Inicio', default=lambda *a: time.strftime('%Y-%m-01'), help=u"",)
    end_date = fields.Date(u'Fecha de Fin', default=datetime.now(), help=u"",)
    filter = fields.Selection([
        ('by_product', u'Por Producto'),
        ('by_category', u'Por Categoria'),
        ('by_lot', u'Por Lote'),
    ], string=u'Filtro', default=u'by_category',  help=u"",)
    location_ids = fields.Many2many('stock.location', 'wizard_kardex_all_location_rel', 'wizard_id', 'location_id',
                                    u'Localidades', help=u"")
    category_ids = fields.Many2many('product.category', 'wizard_kardex_all_category_rel', 'wizard_id', 'category_id',
                                    u'Categorias', help=u"")
    product_ids = fields.Many2many('product.product', 'wizard_kardex_all_product_rel', 'wizard_id', 'product_id',
                                   u'Productos', help=u"")
    lot_ids = fields.Many2many('stock.lot', 'wizard_kardex_all_lot_rel', 'wizard_id', 'lot_id', u'Lots',
                               help=u"")

    def _get_context_for_report(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({
            'product_ids': self.product_ids.ids,
            'category_ids': self.category_ids.ids,
            'lot_ids': self.lot_ids.ids,
            'location_ids': self.location_ids.ids,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'filter_type': self.filter
        })
        return ctx

    def action_print_report(self):
        company = self.env.user.company_id
        ctx = self._get_context_for_report()
        ctx['active_model'] = 'res.company'
        ctx['active_ids'] = [company.id]
        ctx['active_id'] = company.id
        report_name = self.env.ref("ec_kardex.kardex_all_report")
        return report_name.with_context(ctx).report_action(self, data=ctx, config=False)

    def get_report_data_xls(self):
        report_model = self.env['report.stock.utils']
        ctx = self._get_context_for_report()
        return report_model.with_context(ctx).MakeReportAllxls()

    def action_get_report(self):
        res = {
            'type': 'ir.actions.act_url',
            'url': '/download/saveas?model=%(model)s&record_id=%(record_id)s&method=%(method)s&filename=%(filename)s' % {
                'filename': u'Análisis Total.xlsx',
                'model': self._name,
                'record_id': self.id,
                'method': 'get_report_data_xls'
            },
            'target': 'self'
        }

        return res
    
