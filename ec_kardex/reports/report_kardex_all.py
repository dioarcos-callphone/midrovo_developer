# -*- encoding: utf-8 -*-
from odoo.tools.misc import formatLang, format_date
from functools import partial
from odoo import api, models


class ReportEcKardexAll(models.AbstractModel):
    
    _name = 'report.ec_kardex.report_kardex_all'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        context = self.env.context.copy()
        if data:
            context.update(data)
        report_model = self.env['report.stock.utils']
        data = report_model.with_context(context).GetKardexAllData()
        return {
            'formatLang': partial(formatLang, self.env),
            'format_date': partial(format_date, self.env),
            "products": data
        }
