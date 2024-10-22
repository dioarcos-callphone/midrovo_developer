# -*- encoding: utf-8 -*-

from odoo import models, api, fields
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class WizardEcKardexAllStockReport(models.TransientModel):
    _name = 'wizard.ec_kardex.all.stock.report'
    _description = u'Asistente para Stock por Almacen'

    type = fields.Selection([('range','Rango de Fechas'),('today','Actualidad')], default='range', string="Tipo de Reporte")
    location_id = fields.Many2one('stock.location', u'Ubicación', required=False, help=u"", domain=[('usage','=', 'internal')] )
    start_date = fields.Date(u'Desde', help=u"", )
    end_date = fields.Date(u'Hasta', help=u"", )
    categ_id = fields.Many2one('product.category')
    mostrar_costos = fields.Boolean(default=False)
    
    is_inventory_user = fields.Boolean(compute='_compute_is_inventory_user')

    def _compute_is_inventory_user(self):
        for record in self:
            is_group = self.env.user.has_group('inventory_report_location.group_inventory_report_location_user')
            _logger.info(f'PERTENECE AL GRUPO INVENTORY REPORT LOCATION? >>> { is_group }')
            record.is_inventory_user = is_group

    def _get_context_for_report(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        categoria=False
        if self.categ_id:
            categoria=self.categ_id.id

        if not self.start_date:
            start_date = datetime.strptime('1970-01-01', "%Y-%m-%d").date()
        else:
            start_date = self.start_date
        if self.type=='range':
            end_date = self.end_date
        else:
            end_date = self.env['ec.tools'].get_date_now()
        ctx.update({
            'location_id': self.location_id.id,
            'location_name': self.location_id.name,
            'categ_id': categoria,
            'start_date': start_date,
            'end_date': end_date,
            'type': self.type,
            'mostrar_costos':True if self.mostrar_costos else False
        })
        return ctx

    def action_print_report(self):
        company = self.env.user.company_id
        ctx = self._get_context_for_report()
        ctx['active_model'] = 'reºs.company'
        ctx['active_ids'] = [company.id]
        ctx['active_id'] = company.id
        report_name = self.env.ref("ec_kardex.kardex_all_stock_report")
        return report_name.with_context(ctx).report_action(self, data=ctx, config=False)

    def get_report_data_xls(self):
        report_model = self.env['report.ec_kardex.report_kardex_all_stock_xls']
        ctx = self._get_context_for_report()
        return report_model.with_context(ctx).get_report_xls()

    def action_get_report(self):
        res = {
            'type': 'ir.actions.act_url',
            'url': '/download/saveas?model=%(model)s&record_id=%(record_id)s&method=%(method)s&filename=%(filename)s' % {
                'filename': u'Stock por Almacen.xlsx',
                'model': self._name,
                'record_id': self.id,
                'method': 'get_report_data_xls'
            },
            'target': 'self'
        }
        return res