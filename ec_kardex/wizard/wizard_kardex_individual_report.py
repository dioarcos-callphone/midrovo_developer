# -*- encoding: utf-8 -*-
from odoo import models, api, fields
from datetime import timedelta, datetime, time

import pytz
from dateutil.relativedelta import relativedelta

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    # TODO saas-17: remove the try/except to directly import from misc
    import xlsxwriter
import io
from odoo.tools.translate import _
from odoo.exceptions import except_orm, Warning, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF, DEFAULT_SERVER_DATETIME_FORMAT as DTF

class WizardKardexIndividualReport(models.TransientModel):
    _name = 'wizard.ec_kardex.individual.report'
    _description = u'Asistente para kardex individual'

    product_id = fields.Many2one('product.product', u'Producto', required=False, help=u"", )
    location_id = fields.Many2one('stock.location', u'Ubicación', required=False, help=u"",
                                  domain=[('usage', '=', 'internal')])
    date_from = fields.Date(u'Desde', help=u"", )
    date_to = fields.Date(u'Hasta', help=u"", )
    report_format = fields.Selection([
        ('xls', u'Archivo Excel(.xls)'),
        ('pdf', u'Archivo PDF(.pdf)'),
    ], string=u'Tipo de reporte', default=u'pdf', help=u"", )
    show_costs = fields.Boolean("Mostrar costos?", default=False)

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

    def action_view_report(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ec_kardex.action_kardex_report_reg")
        kard = self.env['kardex.report.reg'].search([])
        for lin in kard:
            for line in lin.lines_ids:
                line.unlink()
            lin.unlink()
        # primero creo la vista
        kardex = self.env['kardex.report.reg'].create({'product_id': self.product_id.id,
                                                       'location_id': self.location_id.id,
                                                       'date_from': self.date_from,
                                                       'date_to': self.date_to,
                                                       'show_costs': self.show_costs,
                                                       })
        # ahora creo las lineas en base a la funcion del reporte excel

        product = self.product_id
        location = self.location_id
        move_type = {
            'incoming': u'Entrada',
            'outgoing': u'Salida',
            'internal': u'Interno'
        }
        move_model = self.env["stock.move"]
        fields_model = self.env['ir.fields.converter']
        tz_name = fields_model._input_tz()
        date_from = self.date_from
        if not date_from:
            date_from = "1970-01-01"
        date_to = self.date_to
        if not date_to:
            date_to = datetime.now().date()
        date_from_aux = ''
        if isinstance(date_from, str):
            date_from = datetime.strptime(date_from + " 00:00:00", DTF)
        if isinstance(date_to, str):
            date_to = datetime.strptime(date_to + " 23:59:59", DTF)
        # date_from = date_from - timedelta(hours=5)
        # date_to = date_to - timedelta(hours=5)
        # pasar la fecha a UTC, para que al tomar por SQL considere los datos correctamente
        start_time = date_from
        start_time = start_time.strftime(DTF)
        # cuando me pasen solo fecha, debo considerar todu el dia
        # end_time = date_to
        # end_time=date_to + timedelta(days=1)
        end_time = date_to
        end_time = end_time.strftime(DTF)
        common_domain = [
            ("product_id", "=", product.id),
            ("date", ">", start_time),
            ("date", "<=", end_time),
            ("state", "=", "done"),
        ]
        move_in_recs = move_model.search(common_domain + [("location_dest_id", "=", [location.id])], order="date")
        # find all moves leaving from location
        move_out_recs = move_model.search(common_domain + [("location_id", "=", [location.id])], order="date")
        # order moves by date
        order_moves = move_in_recs + move_out_recs
        order_moves = order_moves.sorted(key=lambda x: x.date)
        lines = []
        # add opening line of report
        params = {
            'location_id': location.id,
            'product_id': product.id,
            'start_date': start_time
        }
        self.env.cr.execute('''
        						SELECT sm.product_id AS product_id,
        							SUM(sm.product_qty) AS qty_in
        						FROM stock_move sm
        							INNER JOIN product_product pp ON pp.id = sm.product_id
        							INNER JOIN product_template pt ON pt.id = pp.product_tmpl_id
        						WHERE sm.location_dest_id = %(location_id)s
        							AND sm.location_id != %(location_id)s
        							AND sm.state = 'done'
        							AND product_id = %(product_id)s
        							AND sm.date < %(start_date)s
        						GROUP BY product_id
        					''', params)
        data = self.env.cr.dictfetchone()
        start_qty_in = data and data.get('qty_in', 0.0) or 0.0
        self.env.cr.execute('''
        						SELECT sm.product_id AS product_id,
        							SUM(sm.product_qty) AS qty_out
        						FROM stock_move sm
        							INNER JOIN product_product pp ON pp.id = sm.product_id
        							INNER JOIN product_template pt ON pt.id = pp.product_tmpl_id
        						WHERE sm.location_dest_id != %(location_id)s
        							AND sm.location_id = %(location_id)s
        							AND sm.state = 'done'
        							AND product_id = %(product_id)s
        							AND sm.date < %(start_date)s
        						GROUP BY product_id
        					''', params)
        data = self.env.cr.dictfetchone()
        start_qty_out = data and data.get('qty_out', 0.0) or 0.0
        lines.append({
            "date": date_from_aux,
            "src": " ",
            "origin": " ",
            "dest": " ",
            "ref": u"Balance Inicial",
            "price_unit": " ",
            "amount": " ",
            "type": " ",
            "partner": " ",
            "qty_in": start_qty_in,
            "qty_out": start_qty_out,
            "balance": start_qty_in - start_qty_out,
        })
        # add move lines of report
        total_qty_in = start_qty_in
        total_qty_out = start_qty_out
        for move in order_moves:
            fecha_entrega_req = ""
            # if move.picking_id:
            # 	if move.picking_id.purchase_request_id:
            # 		fecha_entrega_req=move.picking_id.purchase_request_id.date_end
            account_ids = self.env['account.move'].search(
                [('stock_move_id', '=', move.id), ('state', '=', 'posted')])
            asiento = ''
            for acc_id in account_ids:
                asiento += acc_id.name + " "
            qty_in = move in move_in_recs and move.product_qty or 0.0
            qty_out = move in move_out_recs and move.product_qty or 0.0
            price_unit = move.price_unit
            total_qty_in += qty_in
            total_qty_out += qty_out
            # pasar la fecha en la zona horaria del usuario
            move_date = move.date
            picking_type = move.picking_type_id
            if not picking_type:
                picking_type = move.picking_id.picking_type_id
            src_name = move.location_id.name
            if move.location_id.location_id:
                src_name = move.location_id.location_id.name + ' / ' + move.location_id.name
            dest_name = move.location_dest_id.name
            if move.location_dest_id.location_id:
                dest_name = move.location_dest_id.location_id.name + ' / ' + move.location_dest_id.name

            origin_out = ''
            # SACAR NUMERO DE FACTURA
            if move.picking_id:
                origin_out = move.picking_id.origin
                # invoice = self.env['account.move'].search([('picking_id','=',move.picking_id.id),('move_type', 'in', ['out_invoice','out_refund']),('state', '!=', 'cancel')])
                invoice = self.env['account.move'].search(
                    [('move_type', 'in', ['out_invoice', 'out_refund']), ('state', '!=', 'cancel')])
                if invoice:
                    origin_out = invoice[0].l10n_latam_document_number

                else:
                    invoice = self.env['account.move'].search(
                        [('ref', '=', move.picking_id.origin), ('move_type', '=', ['out_invoice', 'out_refund']),
                         ('state', '!=', 'cancel')])
                    if invoice:
                        origin_out = invoice[0].l10n_latam_document_number
                    else:
                        invoice = self.env['account.move'].search([('name', '=', move.picking_id.origin),
                                                                   ('move_type', '=', ['out_invoice', 'out_refund']),
                                                                   ('state', '!=', 'cancel')])

            else:
                invoice = self.env['account.move'].search(
                    [('ref', '=', move.picking_id.origin), ('move_type', '=', ['out_invoice', 'out_refund']),
                     ('state', '!=', 'cancel')])
                if invoice:
                    origin_out = invoice[0].l10n_latam_document_number
            if not origin_out:
                invoice = self.env['account.move'].search(
                    [('invoice_origin', '=', move.picking_id.origin), ('move_type', '=', ['out_invoice', 'out_refund']),
                     ('state', '!=', 'cancel')])
            if invoice:
                origin_out = invoice[0].l10n_latam_document_number
                partner_id = ""
                if move.picking_id:
                    if move.picking_id.partner_id:
                        partner_id = move.picking_id.partner_id.name
                lines.append({
                    "date": (move_date - timedelta(hours=5)).strftime(DTF),
                    "fecha_req": fecha_entrega_req.strftime(DTF) if fecha_entrega_req != "" else "",
                    "src": src_name,
                    "asiento": asiento,
                    "origin": origin_out,
                    "dest": dest_name,
                    "ref": move.name,
                    "price_unit": price_unit,
                    "amount": price_unit * (qty_in if qty_in > 0 else qty_out),
                    "type": picking_type and move_type.get(picking_type.code, u'Interno') or u'Interno',
                    "partner": partner_id,
                    "qty_in": qty_in,
                    "qty_out": qty_out,
                    "balance": total_qty_in - total_qty_out,
                })
            else:
                partner_id = ""
                if move.picking_id:
                    if move.picking_id.partner_id:
                        partner_id = move.picking_id.partner_id.name
                lines.append({
                    "date": (move_date - timedelta(hours=5)).strftime(DTF),
                    "src": src_name,
                    "asiento": asiento,
                    "origin": origin_out,
                    "dest": dest_name,
                    "ref": move.name,
                    "price_unit": price_unit,
                    "amount": price_unit * (qty_in if qty_in > 0 else qty_out),
                    "type": picking_type and move_type.get(picking_type.code, u'Interno') or u'Interno',
                    "partner": partner_id,
                    "qty_in": qty_in,
                    "qty_out": qty_out,
                    "balance": total_qty_in - total_qty_out,
                })
        else:
            saldo = total_qty_in - total_qty_out
            lines.append({
                "date": date_to,
                "src": " ",
                "asiento": " ",
                "origin": " ",
                "dest": " ",
                "ref": "Cierre del Balance",
                "price_unit": " ",
                "amount": " ",
                "type": " ",
                "partner": " ",
                "qty_in": total_qty_in,
                "qty_out": total_qty_out,
                "balance": saldo,
                "costo_balance": saldo * product.standard_price,
            })

        for aux in lines:
            costs = 0.00
            total = 0.00
            if aux['price_unit'] != ' ':
                costs = float(aux['price_unit'])
            if aux['amount'] != ' ':
                total = float(aux['amount'])
            self.env['kardex.report.reg.lines'].create({'name': aux['origin'],
                                                        'ref': aux['partner'],
                                                        'description': aux['ref'],
                                                        'costs': "%0.4f" % costs,
                                                        'total': "%0.4f" % total,
                                                        'type': aux['type'],
                                                        'income': aux['qty_in'],
                                                        'partner': aux['partner'],
                                                        'outcome': aux['qty_out'],
                                                        'value': aux['balance'],
                                                        'cost_balance': aux['costo_balance'],
                                                        'reg_id': kardex.id,
                                                        })
        # ahora redirijo a la vista form donde mostrara el proceso
        if kardex:
            form_view = [(self.env.ref('ec_kardex.kardex_report_reg_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = kardex.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
