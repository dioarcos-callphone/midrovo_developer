# -*- encoding: utf-8 -*-


import time
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta

try:
	from odoo.tools.misc import xlsxwriter
except ImportError:
	# TODO saas-17: remove the try/except to directly import from misc
	import xlsxwriter
import io

from odoo import models, api, fields
from odoo.tools.translate import _
from odoo.exceptions import except_orm, Warning, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF, DEFAULT_SERVER_DATETIME_FORMAT as DTF

import logging
_logger = logging.getLogger(__name__)


class ReportStockUtils(models.AbstractModel):
	_name = 'report.stock.utils'
	_description = u'Utilidad para generar reporte de stock'

	LETTERS = list(map(chr, range(65, 90)))

	@api.model
	def GetLetterForPosition(self, position):
		return self.LETTERS[position]

	@api.model
	def _sum_inputs(self, lines):
		qty = 0.0
		for line in lines:
			qty += line.get('qty_in', 0.0)
		return qty

	@api.model
	def _sum_outputs(self, lines):
		qty = 0.0
		for line in lines:
			qty += line.get('qty_out', 0.0)
		return qty

	@api.model
	def get_lines_totals_stock(self, product, location, date_from=None, date_to=None):
		from datetime import timedelta
		move_type = {
			'incoming': u'Entrada',
			'outgoing': u'Salida',
			'internal': u'Interno'
		}
		move_model = self.env["stock.move"]
		fields_model = self.env['ir.fields.converter']
		tz_name = fields_model._input_tz()
		if not date_from:
			date_from = "1970-01-01"
		if not date_to:
			date_to = datetime.now().date()
		date_from_aux = ''
		# date_from = date_from - timedelta(hours=5)
		# date_to = date_to - timedelta(hours=5)
		# pasar la fecha a UTC, para que al tomar por SQL considere los datos correctamente
		start_time = date_from
		start_time = start_time.strftime('%Y-%m-%d')
		if isinstance(start_time, str):
			start_time = datetime.strptime(start_time + " 00:00:00", DTF)

		end_time = date_to
		end_time = end_time.strftime('%Y-%m-%d')

		if isinstance(end_time, str):
			end_time = datetime.strptime(end_time + " 23:59:59", DTF) + timedelta(hours=5)
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
		# add move lines of report
		total_qty_in = start_qty_in
		total_qty_out = start_qty_out
		for move in order_moves:
			qty_in = move in move_in_recs and move.product_qty or 0.0
			qty_out = move in move_out_recs and move.product_qty or 0.0
			price_unit = move.price_unit
			total_qty_in += qty_in
			total_qty_out += qty_out
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
			lines.append({
				"date": (move_date - timedelta(hours=5)).strftime(DTF),
				"src": src_name,
				"dest": dest_name,
				"ref": move.name,
				"price_unit": price_unit,
				"amount": price_unit * (qty_in if qty_in > 0 else qty_out),
				"type": picking_type and move_type.get(picking_type.code, u'Interno') or u'Interno',
				"qty_in": qty_in,
				"qty_out": qty_out,
				"balance": total_qty_in - total_qty_out,
			})
		return lines

	@api.model
	def get_lines_totals(self, product, location, date_from=None, date_to=None):
		from datetime import timedelta
		move_type = {
			'incoming': u'Entrada',
			'outgoing': u'Salida',
			'internal': u'Interno'
		}
		move_model = self.env["stock.move"]
		fields_model = self.env['ir.fields.converter']
		tz_name = fields_model._input_tz()
		if not date_from:
			date_from = "1970-01-01"
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
		# cuando me pasen solo fecha, debo considerar todo el dia
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
			"src": "",
			"dest": "",
			"ref": u"Balance Inicial",
			"price_unit": "",
			"amount": "",
			"type": "",
			"qty_in": start_qty_in,
			"qty_out": start_qty_out,
			"balance": start_qty_in - start_qty_out,
		})
		# add move lines of report
		total_qty_in = start_qty_in
		total_qty_out = start_qty_out
		for move in order_moves:
			qty_in = move in move_in_recs and move.product_qty or 0.0
			qty_out = move in move_out_recs and move.product_qty or 0.0
			price_unit = move.price_unit
			total_qty_in += qty_in
			total_qty_out += qty_out
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
			lines.append({
				"date": (move_date - timedelta(hours=5)).strftime(DTF),
				"src": src_name,
				"dest": dest_name,
				"ref": move.name,
				"price_unit": price_unit,
				"amount": price_unit * (qty_in if qty_in > 0 else qty_out),
				"type": picking_type and move_type.get(picking_type.code, u'Interno') or u'Interno',
				"qty_in": qty_in,
				"qty_out": qty_out,
				"balance": total_qty_in - total_qty_out,
			})
		lines.append({
			"date": date_to,
			"src": "",
			"dest": "",
			"ref": "Cierre del Balance",
			"price_unit": "",
			"amount": "",
			"type": "",
			"qty_in": total_qty_in,
			"qty_out": total_qty_out,
			"balance": total_qty_in - total_qty_out,
		})
  
		return lines

	@api.model
	def get_lines(self, product, location, date_from=None, date_to=None):
		from datetime import timedelta
		move_type = {
			'incoming': u'Entrada',
			'outgoing': u'Salida',
			'internal': u'Interno'
		}
		move_model = self.env["stock.move"]
		fields_model = self.env['ir.fields.converter']
		tz_name = fields_model._input_tz()
		if not date_from:
			date_from = "1970-01-01"
		if not date_to:
			date_to = datetime.now().date()
		date_from_aux = ''
		# date_from = date_from - timedelta(hours=5)
		# date_to = date_to - timedelta(hours=5)
		# pasar la fecha a UTC, para que al tomar por SQL considere los datos correctamente
		start_time = date_from
		if isinstance(start_time, str):
			start_time = datetime.strptime(start_time,'%Y-%m-%d')
   
		start_time = start_time.strftime('%Y-%m-%d')
		start_time = datetime.strptime(start_time+" 00:00:00", DTF)

		end_time = date_to
		if isinstance(end_time, str):
			end_time = datetime.strptime(end_time,'%Y-%m-%d')
   
		end_time = end_time.strftime('%Y-%m-%d')
		end_time = datetime.strptime(end_time + " 23:59:59", DTF) + timedelta(hours=5)
  
		common_domain = [
			("product_id", "=", product.id),
			("date", ">=", start_time),
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
							AND sm.date <= %(start_date)s
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
							AND sm.date <= %(start_date)s
						GROUP BY product_id
					''', params)
		data = self.env.cr.dictfetchone()
		start_qty_out = data and data.get('qty_out', 0.0) or 0.0
		lines.append({
			"date": date_from_aux,
			"src": "",
			"origin": "",
			"dest": "",
			"ref": u"Balance Inicial",
			"price_unit": "",
			"amount": "",
			"type": "",
			"partner": "",
			"qty_in": start_qty_in,
			"qty_out": start_qty_out,
			"balance": start_qty_in - start_qty_out,
		})
		# add move lines of report
		total_qty_in = start_qty_in
		total_qty_out = start_qty_out
		for move in order_moves:
			fecha_entrega_req=""
			account_ids = self.env['account.move'].search([('stock_move_id', '=', move.id), ('state', '=', 'posted')])
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

			origin_out=''
			# SACAR NUMERO DE FACTURA
			if move.picking_id:
				origin_out = move.picking_id.origin
				# invoice = self.env['account.move'].search([('picking_id','=',move.picking_id.id),('move_type', 'in', ['out_invoice','out_refund']),('state', '!=', 'cancel')])
				invoice = self.env['account.move'].search([('move_type', 'in', ['out_invoice','out_refund']),('state', '!=', 'cancel')])
				if invoice:
					origin_out = invoice[0].l10n_latam_document_number

				else:
					invoice = self.env['account.move'].search([('ref', '=', move.picking_id.origin),('move_type', '=', ['out_invoice','out_refund']),('state', '!=', 'cancel')])
					if invoice:
						origin_out = invoice[0].l10n_latam_document_number
					else:
						invoice = self.env['account.move'].search([('name', '=', move.picking_id.origin),
																   ('move_type', '=', ['out_invoice', 'out_refund']),
																   ('state', '!=', 'cancel')])

			else:
				invoice = self.env['account.move'].search([('ref', '=', move.picking_id.origin),('move_type', '=', ['out_invoice','out_refund']),('state', '!=', 'cancel')])
				if invoice:
					origin_out = invoice[0].l10n_latam_document_number
			if not origin_out:
				invoice = self.env['account.move'].search([('invoice_origin', '=', move.picking_id.origin),('move_type', '=', ['out_invoice','out_refund']),('state', '!=', 'cancel')])
			if invoice:
				origin_out = invoice[0].l10n_latam_document_number
				partner = ""
				if move.picking_id:
					if move.picking_id.partner_id:
						partner = move.picking_id.partner_id.name
				lines.append({
					"date": (move_date - timedelta(hours=5)).strftime(DTF),
					"fecha_req":fecha_entrega_req.strftime(DTF) if fecha_entrega_req!="" else "" ,
					"src": src_name,
					"asiento": asiento,
					"origin": origin_out,
					"partner_name": partner,
					"dest": dest_name,
					"ref": move.name,
					"price_unit": price_unit,
					"amount": price_unit * (qty_in if qty_in > 0 else qty_out),
					"type": picking_type and move_type.get(picking_type.code, u'Interno') or u'Interno',
					"partner": move.picking_id and move.picking_id.name or '',
					"qty_in": qty_in,
					"qty_out": qty_out,
					"balance": total_qty_in - total_qty_out,
				})
			else:
				partner = ""
				if move.picking_id:
					if move.picking_id.partner_id:
						partner = move.picking_id.partner_id.name
				lines.append({
					"date": (move_date - timedelta(hours=5)).strftime(DTF),
					"src": src_name,
					"asiento": asiento,
					"origin": origin_out,
					"partner_name": partner,
					"dest": dest_name,
					"ref": move.name,
					"price_unit": price_unit,
					"amount": price_unit * (qty_in if qty_in > 0 else qty_out),
					"type": picking_type and move_type.get(picking_type.code, u'Interno') or u'Interno',
					"partner": move.picking_id and move.picking_id.name or '',
					"qty_in": qty_in,
					"qty_out": qty_out,
					"balance": total_qty_in-total_qty_out,
				})
		else:
			saldo = total_qty_in - total_qty_out
			lines.append({
				"date": date_to,
				"src": "",
				"asiento": "",
				"origin": "",
				"partner_name": "",
				"dest": "",
				"ref": "Cierre del Balance",
				"price_unit": "",
				"amount": "",
				"type": "",
				"partner": "",
				"qty_in": total_qty_in,
				"qty_out": total_qty_out,
				"balance": saldo,
				"costo_balance": saldo * product.standard_price # SE MULTIPLICA EL SALDO TOTAL POR EL STANDARD PRICE (COSTO)
			})
   
		return lines

	@api.model
	def GetKardexIndividualData(self):
		product_model = self.env['product.product']
		location_model = self.env['stock.location']
		context = self.env.context.copy()
		product =product_model.browse(context.get('product_id'))
		location = location_model.browse(context.get('location_id'))
		date_from = context.get('date_from', False)
		date_to = context.get('date_to', False)
		lines = self.get_lines(product, location, date_from, date_to)
		sum_inputs = self._sum_inputs(lines)
		sum_outputs = self._sum_inputs(lines)
		return {
			'product': product ,
			'location': location,
			'lines': lines,
			'sum_inputs': sum_inputs,
			'sum_outputs': sum_outputs,
			'date_from': date_from,
			'date_to': date_to,
		}

	@api.model
	def MakeReportxls(self):
		context = self.env.context.copy()
		location_name = context.get('location_name')
		date_from = context.get('date_from', False)
		date_to = context.get('date_to', False)
		show_costs = context.get('show_costs', False)

		filter_data = [
			('Fechas de Corte', 'Desde: %s - Hasta: %s' % (date_from, date_to)),

		]

		fp = io.BytesIO()

		workbook = xlsxwriter.Workbook(fp, {'in_memory': True, 'constant_memory': False})
		worksheet = workbook.add_worksheet('Kardex Individual x Producto')

		FORMATS = {
			'bold': workbook.add_format({'bold': True, 'text_wrap': True}),
			'number': workbook.add_format({'num_format': '#,##0.00'}),
			'money': workbook.add_format({'num_format': '$#,##0.00'}),
			'number_bold': workbook.add_format({'num_format': '#,##0.00', 'bold': True}),
			'money_bold': workbook.add_format({'num_format': '$#,##0.00', 'bold': True}),
			'date': workbook.add_format({'num_format': 'dd/mm/yyyy'}),
			'datetime': workbook.add_format({'num_format': 'dd/mm/yyyy h:m:s'}),
			'date_bold': workbook.add_format({'num_format': 'dd/mm/yyyy', 'bold': True}),
			'datetime_bold': workbook.add_format({'num_format': 'dd/mm/yyyy h:m:s', 'bold': True}),
			'merge_center': workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True}),
		}

		COLUM_POS = {
			'date': 0,
			'src': 1,
			'dest': 2,
			'asiento': 3,
			'origin': 4,
			'partner_name': 5,
			'partner': 6,
			'ref': 7,
			'price_unit': 8,
			'amount': 9,
			'type': 10,
			'qty_in': 11,
			'qty_out': 12,
			'balance': 13,
			'costo_balance': 14,
		}
		sin_COLUM_POS = {
			'date': 0,
			'src': 1,
			'dest': 2,
			'asiento': 3,
			'origin': 4,
			'partner_name': 6,
			'partner': 6,
			'ref': 7,
			'type': 8,
			'qty_in': 9,
			'qty_out': 10,
			'balance': 11,
		}

		COLUM_SIZE = {
			'date': 30,
			'src': 40,
			'dest': 30,
			'asiento': 30,
			'origin': 15,
			'partner_name': 15,
			'partner': 15,
			'ref': 40,
			'price_unit': 25,
			'amount': 10,
			'type': 10,
			'qty_in': 15,
			'qty_out': 15,
			'balance': 15,
			'costo_balance': 15,

		}
		sin_COLUM_HEADER = {
			'date': 'Fecha',
			'src': 'Bodega de Origen',
			'dest': 'Bodega de Destino',
			'asiento':'Asiento Contable',
			'origin': 'Documento de Origen',
			'partner_name': 'Usuario',
			'partner': 'Referencia',
			'ref': u'Descripción',
			'type': 'Tipo',
			'qty_in': 'Entrada',
			'qty_out': 'Salida',
			'balance': 'Saldo',
		}
		COLUM_HEADER = {
			'date': 'Fecha',
			'src': 'Bodega de Origen',
			'dest': 'Bodega de Destino',
			'asiento':'Asiento Contable',
			'origin': 'Documento de Origen',
			'partner_name': 'Usuario',
			'partner': 'Referencia',
			'ref': u'Descripción',
			'price_unit': 'Costo Unitario $',
			'amount': 'Total $',
			'type': 'Tipo',
			'qty_in': 'Entrada',
			'qty_out': 'Salida',
			'balance': 'Saldo',
			'costo_balance': 'Costo x Saldo'
		}
		COLUM_FORMAT = {
			'date': 'date',
			'src': False,
			'dest': False,
			'asiento':False,
			'origin': False,
			'partner': False,
			'partner_name': False,
			'price_unit': 'money',
			'ref': False,
			'origin': False,
			'amount': 'money',
			'type': False,
			'qty_in': 'number',
			'qty_out': 'number',
			'balance': 'number',
			'costo_balance': 'number',
		}
		if location_name in ["MATRIZ SUMINISTROS DE LIMPIEZA", "URDESA SUMINISTROS DE LIMPIEZA",
							 "QUITO SUMINISTROS DE LIMPIEZA",
							 "MATRIZ SUMINISTROS DE OFICINA", "URDESA SUMINISTROS DE OFICINA",
							 "QUITO SUMINISTROS DE OFICINA",
							 "MATRIZ SUMINISTROS ELECTRICOS", "URDESA SUMINISTROS ELECTRICOS",
							 "QUITO SUMINISTROS ELECTRICOS"]:
			COLUM_POS = {
				'date': 0,
				'fecha_req':1,
				'src': 2,
				'dest': 3,
				'asiento': 4,
				'origin': 5,
				'partner_name': 6,
				'partner': 7,
				'ref': 8,
				'price_unit': 9,
				'amount': 10,
				'type': 11,
				'qty_in': 12,
				'qty_out': 13,
				'balance': 14,
				'costo_balance': 15,
			}
			sin_COLUM_POS = {
				'date': 0,
				'fecha_req':1,
				'src': 2,
				'dest': 3,
				'asiento': 4,
				'origin': 5,
				'partner_name': 6,
				'partner': 7,
				'ref': 8,
				'type': 9,
				'qty_in': 10,
				'qty_out': 11,
				'balance': 12,
				'costo_balance': 13,
			}
			COLUM_SIZE["fecha_req"]=30
			COLUM_HEADER["fecha_req"]="Fecha Requisión"
			COLUM_FORMAT["fecha_req"]='date'

		current_row = 0
		#escribir la cabecera
		if show_costs:
			for key in COLUM_HEADER.keys():
				value = COLUM_HEADER[key]
				worksheet.write(current_row, COLUM_POS[key], value, FORMATS['bold'])
		else:
			for key in sin_COLUM_HEADER.keys():
				value = sin_COLUM_HEADER[key]
				worksheet.write(current_row, sin_COLUM_POS[key], value, FORMATS['bold'])
		report_data = self.GetKardexIndividualData()
		if show_costs:
			cols_position = COLUM_POS.values()
		else:
			cols_position = sin_COLUM_POS.values()
		current_row = 0
		current_row_2 = 0
		worksheet.merge_range(current_row, min(cols_position), current_row, max(cols_position),
							  u"Kardex Individual x Producto", FORMATS['merge_center'])
		current_row += 1

		for product in report_data.get('product', []):
			current_row += 1
			current_row_2 += 1
			worksheet.write(current_row, 0, 'Empresa: ', FORMATS['bold'])
			worksheet.write(current_row, current_row_2, self.env.company.name, FORMATS.get(COLUM_FORMAT['dest']))
			current_row += 1
			worksheet.write(current_row, 0, 'Ruc: ', FORMATS['bold'])
			worksheet.write(current_row, current_row_2, self.env.company.vat, FORMATS.get(COLUM_FORMAT['dest']))
			current_row += 1
			worksheet.write(current_row, 0, 'Producto: ', FORMATS['bold'])
			worksheet.write(current_row, current_row_2, product.display_name, FORMATS.get(COLUM_FORMAT['dest']))
			current_row += 1
			worksheet.write(current_row, 0, 'Referencia Interna: ', FORMATS['bold'])
			worksheet.write(current_row, current_row_2, product.default_code, FORMATS.get(COLUM_FORMAT['dest']))
			current_row += 1
			worksheet.write(current_row, 0, 'Codigo de Barras: ', FORMATS['bold'])
			worksheet.write(current_row, current_row_2, product.barcode, FORMATS.get(COLUM_FORMAT['dest']))
			current_row += 1
			worksheet.write(current_row, 0, 'Método de Valorización: ', FORMATS['bold'])
			worksheet.write(current_row, current_row_2, product.cost_method_name(), FORMATS.get(COLUM_FORMAT['dest']))
			current_row += 1
			worksheet.write(current_row,0, 'Bodega: ', FORMATS['bold'])
			for location in report_data.get('location', []):
				worksheet.write(current_row,current_row_2, location.display_name, FORMATS.get(COLUM_FORMAT['dest']))
			current_row += 1
			worksheet.write(current_row,0, 'Unidad de Medida: ', FORMATS['bold'])
			worksheet.write(current_row,current_row_2, product.uom_id.name, FORMATS.get(COLUM_FORMAT['dest']))
			current_row += 1

		if filter_data and date_from and date_to:
			for key, value in filter_data:
				worksheet.write(current_row, 0, key, FORMATS['bold'])
				worksheet.merge_range(current_row, min(cols_position)+1 , current_row, max(cols_position), value)
				current_row += 1

		current_row += 1

		if show_costs:
			for key in COLUM_HEADER.keys():
				value = COLUM_HEADER[key]
				worksheet.write(current_row, COLUM_POS[key], value, FORMATS['bold'])
		else:
			for key in sin_COLUM_HEADER.keys():
				value = sin_COLUM_HEADER[key]
				worksheet.write(current_row, sin_COLUM_POS[key], value, FORMATS['bold'])

		if show_costs:
			for lines in report_data.get('lines', []):
				current_row += 1
				for key in COLUM_POS.keys():
					value = lines.get(key, '')
					worksheet.write(current_row, COLUM_POS[key], value, FORMATS.get(COLUM_FORMAT[key]))
		else:
			for lines in report_data.get('lines', []):
				current_row += 1
				for key in sin_COLUM_POS.keys():
					value = lines.get(key, '')
					worksheet.write(current_row, sin_COLUM_POS[key], value, FORMATS.get(COLUM_FORMAT[key]))

		if show_costs:
			for column_name in COLUM_POS.keys():
				position = COLUM_POS[column_name]
				worksheet.set_column(position, position, COLUM_SIZE[column_name])
		else:
			for column_name in sin_COLUM_POS.keys():
				position = sin_COLUM_POS[column_name]
				worksheet.set_column(position, position, COLUM_SIZE[column_name])

		workbook.close()
		fp.seek(0)
		data = fp.read()
		fp.close()
		return data

	def _get_initial_stock(self, location_id, start_time, product_id):
		query_out = """
					SELECT 
						sum(sm.product_qty)
					FROM stock_move sm
						LEFT JOIN product_product pp ON pp.id = sm.product_id
						LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
					WHERE date < %(start_time)s 
						AND product_id = %(product_id)s
						AND sm.location_id = %(location_id)s 
						AND sm.location_id != sm.location_dest_id
						AND sm.state = 'done' AND sm.product_qty != 0 AND sm.product_qty IS NOT NULL
					"""
		query_in = """					
					SELECT 
						sum(sm.product_qty) as total
					FROM stock_move sm
						LEFT JOIN product_product pp ON pp.id = sm.product_id
						LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
					WHERE date < %(start_time)s 
						AND product_id = %(product_id)s
						AND sm.location_dest_id = %(location_id)s 
						AND sm.location_id != sm.location_dest_id
						AND sm.state = 'done' AND sm.product_qty != 0 AND sm.product_qty IS NOT NULL					
				"""
		params = {
			'start_time': start_time,
			'product_id': product_id.id,
			'location_id': location_id.id
		}
		self.env.cr.execute(query_in, params)
		result_in = self.env.cr.dictfetchall()
		qty_in = result_in[0]['total'] or 0
		self.env.cr.execute(query_out, params)
		qty_out = self.env.cr.dictfetchall()
		qty_out = qty_out[0]['sum'] or 0
		return qty_in - qty_out

	def _compute_initial_average_cost(self, product_id):
		query_out = """
							SELECT 
								sum(sm.product_qty)
							FROM stock_move sm
								LEFT JOIN product_product pp ON pp.id = sm.product_id
								LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
							WHERE date < %(start_time)s 
								AND product_id = %(product_id)s
								AND sm.location_id = %(location_id)s 
								AND sm.location_id != sm.location_dest_id
								AND sm.state = 'done' AND sm.product_qty != 0 AND sm.product_qty IS NOT NULL
							"""
		query_in = """					
							SELECT 
								sum(sm.product_qty) as total
							FROM stock_move sm
								LEFT JOIN product_product pp ON pp.id = sm.product_id
								LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
							WHERE date < %(start_time)s 
								AND product_id = %(product_id)s
								AND sm.location_dest_id = %(location_id)s 
								AND sm.location_id != sm.location_dest_id
								AND sm.state = 'done' AND sm.product_qty != 0 AND sm.product_qty IS NOT NULL					
						"""
		params = {
			'start_time': start_time,
			'product_id': product_id.id,
			'location_id': location_id.id
		}
		self.env.cr.execute(query_in, params)
		result_in = self.env.cr.dictfetchall()
		qty_in = result_in[0]['total'] or 0
		self.env.cr.execute(query_out, params)
		qty_out = self.env.cr.dictfetchall()
		qty_out = qty_out[0]['sum'] or 0
		return qty_in - qty_out

	def _get_initial_average_cost(self, location_id, start_time, product_id):
		historic_ids = self.env['product.historic.cost'].search([
			('product_id', '=', product_id.id),
			('create_date', '<=', start_time)
		], order='create_date desc', limit=1)
		if not historic_ids:
			return self._compute_initial_average_cost(product_id)
		return historic_ids.cost

	def _get_kardex_stock_from_product(self, moves, location_id):
		total_qty = 0
		for move in moves:
			# Means OUT
			if move['location_id'] == location_id.id:
				total_qty -= move['product_qty']
			# Means IN
			elif move['location_dest_id'] == location_id.id:
				total_qty += move['product_qty']
		return total_qty

	def _get_kardex_from_product(self, moves, location_id, initial_stock):
		result = []
		average = 1
		location_obj = self.env['stock.location']
		total_qty = 0
		for move in moves:
			# Means OUT

			if move['location_id'] == location_id.id:
				total_qty -= move['product_qty']
				fecha = move['date']
				_logger.info(f'TIPO DE FECHA >>> { type(fecha) }')
				result.append({
					'date': move['date'],
					'name': move['reference'] or move['name'],
					'location': location_obj.browse(move['location_id']).name,
					'type': 'out',
					'origen': location_obj.browse(move['location_dest_id']).name,
					'doc_origen':move['origin'] or '',
					'qty': move['product_qty'],
					'total_qty': total_qty,
					'price_unit': average,
					'average_price': average,
					'inventory_value': average * total_qty
				})

			# Means IN
			elif move['location_dest_id'] == location_id.id:
				if move['price_unit']:
					price_unit = move['price_unit']
					if (move['product_qty'] + total_qty) != 0:
						average = round((move['product_qty'] * move['price_unit'] + (total_qty * average)) / (move['product_qty'] + total_qty), 2)
					else:
						average = 0.00
				else:
					price_unit = 0.00
					average = 1

				total_qty += move['product_qty']
				result.append({
					'date': move['date'],
					'name': move['reference'] or move['name'],
					'location': location_obj.browse(move['location_id']).name,
					'type': 'in',
					'origen': location_obj.browse(move['location_id']).name,
					'doc_origen':move['origin'] or '',
					'qty': move['product_qty'],
					'total_qty': total_qty,
					'price_unit': round(price_unit, 2),
					'average_price': average,
					'inventory_value': average * total_qty
				})
		return result

	def GetKardexAllStockData(self):
		from datetime import timedelta
		product_model = self.env['product.product']
		location_model = self.env['stock.location']
		category_model = self.env['product.category']
		context = self.env.context.copy()
		start_date = context.get('start_date', False)
		end_date = context.get('end_date', False)
		if not start_date:
			start_date= datetime.strptime('1970-01-01', "%Y-%m-%d")
		if not end_date:
			timestamp = datetime.strptime(time.strftime(DTF), DTF)
			end_date = (fields.Datetime.context_timestamp(self, timestamp) + relativedelta(months=+1, day=1, days=-1)).strftime(DF)
		if isinstance(start_date, str):
			start_date = datetime.strptime(start_date, "%Y-%m-%d")
		#"1970-01-01 00:00:00"
		if isinstance(end_date, str):
			end_date = datetime.strptime(end_date, "%Y-%m-%d")
		# pasar la fecha a UTC, para que al tomar por SQL considere los datos correctamente
		start_time = start_date
		start_time = start_time.strftime(DTF)
		end_date = end_date + timedelta(days=1)
		end_time = end_date.strftime(DTF)
		location_id = location_model.browse(context['location_id'])
		categoria_id=False
		if context['categ_id']:
			categoria_id = category_model.browse(context['categ_id'])
		product_ids = product_model.search([('type', '!=', 'service')]).ids
		query = """
					SELECT sm.product_id,
						sm.location_id,
						sm.name,
						sm.reference,
						sm.date,
						sm.picking_id,
						sm.location_dest_id,
						sm.price_unit,
						sm.product_uom,
						sm.product_qty,
						pi.origin
					FROM stock_move sm
						LEFT JOIN product_product pp ON pp.id = sm.product_id
						LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
						LEFT JOIN stock_picking pi ON pi.id = sm.picking_id
					WHERE sm.date <= %(end_time)s and sm.date >= %(start_time)s
						AND product_id = %(product_id)s
						AND (sm.location_id = %(location_id)s OR sm.location_dest_id = %(location_id)s)
						AND sm.location_id != sm.location_dest_id
						AND sm.state = 'done' AND sm.product_qty != 0 AND sm.product_qty IS NOT NULL
				"""
		if categoria_id:
			product_ids = product_model.search([('type', '!=', 'service'),('categ_id', '=', categoria_id.id)]).ids
			query += """ 
					AND pt.categ_id= %(categoria_id)s """

		query += """ 
				ORDER BY date ASC
			"""
		results = []

		for product_id in product_model.browse(product_ids):
			params = {
				'start_time': start_time,
				'end_time': end_time,
				'product_id': product_id.id,
				'location_id': location_id.id,
			}
			if categoria_id:
				params['categoria_id'] = categoria_id.id

			self.env.cr.execute(query, params)
			data_aux = self.env.cr.dictfetchall()
			if not any(c['product_code'] == product_id.default_code and c['location_id'] == location_id.id for c in results):
				detailed_type = ""
				if product_id.detailed_type == 'product':
					detailed_type = "Almacenable"
				if product_id.detailed_type == 'consu':
					detailed_type = "Consumible"
				if product_id.detailed_type == 'service':
					detailed_type = "Servicio"
				results.append({'product_code': product_id.default_code,
								'product_name': product_id.name,
								'detailed_type': detailed_type,
								'location_name': location_id.name,
								'location_id': location_id.id,
								'product_id': product_id.id,
								'product_uom_id': product_id.uom_id.id,
								'product_uom_name': product_id.uom_id.name,
								'quantity': self._get_kardex_stock_from_product(data_aux, location_id),
								'costo_unit': product_id.standard_price,
								'tot_costo_unit':product_id.standard_price*self._get_kardex_stock_from_product(data_aux, location_id) if self._get_kardex_stock_from_product(data_aux, location_id)> 0 else 0})
		return results

	def GetKardexAllData(self):
		from datetime import timedelta
		product_model = self.env['product.product']
		location_model = self.env['stock.location']
		context = self.env.context.copy()
		start_date = context.get('start_date', False)
		end_date = context.get('end_date', False)
		if not start_date:
			start_date = datetime.strptime('1970-01-01', "%Y-%m-%d")  # "1970-01-01 00:00:00"
		if not end_date:
			timestamp = datetime.strptime(time.strftime(DTF), DTF)
			end_date = (fields.Datetime.context_timestamp(self, timestamp) + relativedelta(months=+1, day=1, days=-1)).strftime(DF)
		if isinstance(start_date, str):
			start_date = datetime.strptime(start_date, "%Y-%m-%d")
		if isinstance(end_date, str):
			end_date = datetime.strptime(end_date, "%Y-%m-%d")
		# pasar la fecha a UTC, para que al tomar por SQL considere los datos correctamente
		start_time = start_date
		start_time = start_time.strftime(DTF)
		end_date = end_date + timedelta(days=1)
		end_time = end_date.strftime(DTF)
		filter_type = context.get('filter_type', 'by_category')
		product_ids = context.get('product_ids', [])
		category_ids = context.get('category_ids', [])
		lot_ids = context.get('lot_ids', [])
		location_ids = context.get('location_ids', [])
		if not location_ids:
			location_ids = location_model.search([('usage', '=', 'internal')]).ids
		if filter_type == 'by_category' and category_ids:
			product_ids = product_model.search([('categ_id', 'in', category_ids)]).ids
		elif filter_type == 'by_lot' and lot_ids:
			SQL = """SELECT product_id FROM stock_production_lot WHERE id IN %(lot_ids)s"""
			self.env.cr.execute(SQL, {'lot_ids': tuple(lot_ids)})
			product_ids = map(lambda x: x[0], self.env.cr.fetchall())
		if not product_ids:
			product_ids = product_model.search([('type', '!=', 'service')]).ids
		if not product_ids:
			raise Warning(_(u"There's not any product or category selected"))
		query = """
					SELECT 
					    sm.id,
					    sm.product_id,
						sm.location_id,
						sm.name,
						sm.reference,
						sm.date,
						sm.picking_id,
						sm.location_dest_id,
						sm.price_unit,
						sm.product_uom,
						sm.product_qty,
						pi.origin
					FROM stock_move sm
						LEFT JOIN product_product pp ON pp.id = sm.product_id
						LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
						LEFT JOIN stock_picking pi ON pi.id = sm.picking_id
					WHERE sm.date >= %(start_time)s AND sm.date <= %(end_time)s 
						AND product_id = %(product_id)s
						AND (sm.location_id = %(location_id)s OR sm.location_dest_id = %(location_id)s)
						AND sm.location_id != sm.location_dest_id
						AND sm.state = 'done' AND sm.product_qty != 0 AND sm.product_qty IS NOT NULL
				""" \
				"""
					ORDER BY date ASC
				"""
		results = {}
		for product_id in product_model.browse(product_ids):
			default_code = ''
			if product_id.default_code:
				default_code = ' ['+ product_id.default_code + ']'

			results[product_id.name + default_code] = {}
			for location_id in location_model.browse(location_ids):
				params = {
					'start_time': start_time,
					'end_time': end_time,
					'product_id': product_id.id,
					'location_id': location_id.id
				}
				self.env.cr.execute(query, params)
				data_aux = self.env.cr.dictfetchall()
				initial_stock = self._get_initial_stock(location_id, start_time, product_id)
				results[product_id.name + default_code][location_id.display_name] = self._get_kardex_from_product(data_aux, location_id, initial_stock)
    
		# _logger.info(f'MOSTRANDO RESULT >>> { results }')
		return results

	@api.model
	def MakeReportAllxls(self):
		fp = io.BytesIO()
		workbook = xlsxwriter.Workbook(fp, {'in_memory': True, 'constant_memory': False})
		sheet = workbook.add_worksheet('Kardex General')
		bold_color_ubi = workbook.add_format({'align': 'center', 'bold': True, 'text_wrap': True, 'font_size': 12})
		bold_color_ubi.set_bg_color('#00FF99')

		bold_color = workbook.add_format({'align': 'center', 'bold': True, 'text_wrap': True})
		bold_color.set_bg_color('#00FF99')

		bold_color_product = workbook.add_format({'align': 'center', 'bold': True, 'text_wrap': True, 'font_size': 14})
		bold_color_product.set_bg_color('#12CA95')
		cell_color = workbook.add_format({'align': 'center', 'text_wrap': True})
		cell_color.set_bg_color('#00FF99')
		bold = workbook.add_format({'bold': True, 'text_wrap': True})
		monetary = workbook.add_format({'text_wrap': True, 'num_format': '$#,##0.00'})
		monetary_color = workbook.add_format({'text_wrap': True, 'num_format': '$#,##0.00'})
		monetary_color.set_bg_color('#00FF99')
		sheet.set_column(3, 3, 25)
		sheet.set_column(1, 2, 25)
		sheet.set_column(4, 15, 15)
		sheet.set_column(0, 0, 15)

		report_data = self.GetKardexAllData()
		sheet.write(0, 0, "Fecha", bold)
		sheet.write(0, 1, "Ubicacion origen/destino", bold)
		sheet.write(0, 2, "Tipo Movimiento", bold)
		sheet.write(0, 3, "Movimiento", bold)
		sheet.write(0, 4, "Cantidad", bold)
		sheet.write(0, 5, "Precio unitario", bold)
		if not self.env.user.has_group('inventory_report_location.group_inventory_report_location_user'):
			sheet.write(0, 6, "Coste promedio", bold_color)
		sheet.write(0, 7, "Total Cantidad", bold)
		sheet.write(0, 8, "Total inventario", bold)
		i = 1
		for product in report_data:
			prod = report_data[product]
			sheet.write(i + 1, 0, 'Producto', bold_color_product)
			sheet.merge_range(i + 1, 1, i + 1, 2, product, bold_color_product)
			i += 1
			for ubi in prod:
				moves = prod[ubi]
				if moves:
					sheet.write(i + 1, 0, 'Bodega', bold_color_ubi)
					sheet.write(i + 1, 1, ubi, bold_color_ubi)
					i += 2
					for data in moves:
						sheet.write(i, 0, data['date'])
						sheet.write(i, 1, data['origen'])
						sheet.write(i, 2, 'Entrada' if data['type'] == 'in' else 'Salida')
						sheet.write(i, 3, data['name'])
						sheet.write(i, 4, data['qty'])
						sheet.write(i, 5, data['price_unit'], monetary)
						if not self.env.user.has_group('inventory_report_location.group_inventory_report_location_user'):
							sheet.write(i, 6, data['average_price'], monetary_color)
						sheet.write(i, 7, data['total_qty'])
						sheet.write(i, 8, data['inventory_value'], monetary)
						i += 1
		workbook.close()
		fp.seek(0)
		data = fp.read()
		fp.close()
		return data
