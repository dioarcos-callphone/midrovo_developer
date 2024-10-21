# -*- encoding: utf-8 -*-
from functools import partial
from odoo import models, api
from odoo.tools.misc import formatLang, format_date


class ReportEcKardexIndividual(models.AbstractModel):
    _name = 'report.ec_kardex.report_kardex_individual'

    @api.model
    def _get_report_values(self, docids, data=None):
        context = self.env.context.copy()
        if data:
            context.update(data)
        report_model = self.env['report.stock.utils']
        data = report_model.with_context(context).GetKardexIndividualData()
        return {
            'formatLang': partial(formatLang, self.env),
            'company': self.env.user.company_id,
            'format_date': partial(format_date, self.env),
            **data
        }
