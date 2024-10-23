# -*- encoding: utf-8 -*-
from odoo.tools.misc import formatLang, format_date
from functools import partial
from odoo import api, models
from datetime import datetime
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter
import io

class ReportEcKardexAllStockXls(models.AbstractModel):
    _name = 'report.ec_kardex.report_kardex_all_stock_xls'

    def create_workbook(self, page_string=''):
        fp = io.BytesIO()
        # crear el reporte en memoria, no en archivo
        workbook = xlsxwriter.Workbook(fp, {'in_memory': True, 'constant_memory': False})
        worksheet = workbook.add_worksheet(page_string) 
        FORMATS = {
            'title': workbook.add_format(
                {'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_color': 'white', 'bg_color': '#0F1570',
                 'border': 1}),
            'bold': workbook.add_format({'bold': True, 'text_wrap': True}),
            'single_bold': workbook.add_format({'bold': True}),
            'bold_border': workbook.add_format({'bold': True, 'border': 1}),
            'number': workbook.add_format({'num_format': '#,##0.00'}),
            'number_0f': workbook.add_format({'num_format': '#,##0'}),
            'money': workbook.add_format({'num_format': '$#,##0.00'}),
            'number_bold': workbook.add_format({'num_format': '#,##0.00', 'bold': True}),
            'money_bold': workbook.add_format({'num_format': '$#,##0.00', 'bold': True}),
            'date': workbook.add_format({'num_format': 'dd/mm/yyyy'}),
            'datetime': workbook.add_format({'num_format': 'dd/mm/yyyy h:m:s'}),
            'date_bold': workbook.add_format({'num_format': 'dd/mm/yyyy', 'bold': True}),
            'datetime_bold': workbook.add_format({'num_format': 'dd/mm/yyyy h:m:s', 'bold': True}),
            'merge_center': workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True}),
            'merge_center_single': workbook.add_format({'align': 'center', 'valign': 'vcenter'}),
            'merge_left': workbook.add_format({'align': 'left', 'valign': 'vcenter', 'bold': True}),
            'merge_right': workbook.add_format({'align': 'right', 'valign': 'vcenter', 'bold': True}),
            'aqua': workbook.add_format({'font_color': '#909C9D', 'num_format': '#,##0.00'}),
        }
        return fp, workbook, worksheet, FORMATS

    @api.model
    def get_workbook_binary(self, fp, workbook):
        workbook.close()
        fp.seek(0)
        data = fp.read()
        fp.close()
        return data

    def get_report_xls(self):
        current_row = 0

        def set_cabecera(workbook, current_row):
            worksheet.write(current_row, 0, u"Codigo", FORMATS['title'])
            worksheet.write(current_row, 1, u"Nombre", FORMATS['title'])
            worksheet.write(current_row, 2, u"Unidad de Medida", FORMATS['title'])
            worksheet.write(current_row, 3, u"Existencia", FORMATS['title'])
            worksheet.write(current_row, 4, u"Tipo de Producto", FORMATS['title'])
            # if context.get('type', False) == 'today':
            #     worksheet.write(current_row, 3, u"Virtual", FORMATS['title'])
            #     worksheet.write(current_row, 4, u"Costo Unit", FORMATS['title'])
            #     worksheet.write(current_row, 5, u"Costo Total", FORMATS['title'])
            # else:
            if context.get('mostrar_costos', False) == True:
                worksheet.write(current_row, 5, u"Costo Unit", FORMATS['title'])
                worksheet.write(current_row, 6, u"Costo Total", FORMATS['title'])


        def set_line(workbook, current_row, d):

            worksheet.write(current_row, 0, d['product_code'], )
            worksheet.write(current_row, 1, d['product_name'], )
            worksheet.write(current_row, 2, d['product_uom_name'], )
            worksheet.write(current_row, 3, d['quantity'], )
            worksheet.write(current_row, 4, d['detailed_type'], )
            # if context.get('type', False) == 'today':
            #     virtual_available = self.env['product.product'].browse(d['product_id']).virtual_available
            #     worksheet.write(current_row, 3, virtual_available, )
            #     worksheet.write(current_row, 4, d['costo_unit'], )
            #     worksheet.write(current_row, 5, d['tot_costo_unit'], )
            # else:
            if context.get('mostrar_costos', False) == True:
                worksheet.write(current_row, 5, d['costo_unit'], )
                worksheet.write(current_row, 6, d['tot_costo_unit'], )

        fp, workbook, worksheet, FORMATS = self.create_workbook("REPORTE ALMACEN")
        context = self.env.context.copy()
        report_model = self.env['report.stock.utils']
        data = report_model.with_context(context).GetKardexAllStockData()
        worksheet.write(current_row, 0, u"DESDE", FORMATS['title'])
        worksheet.write(current_row, 1, str(context.get('start_date', False)),)
        current_row += 1
        worksheet.write(current_row, 0, u"HASTA", FORMATS['title'])
        worksheet.write(current_row, 1, str(context.get('end_date', False)),)
        current_row += 1
        location_id = self.env['stock.location'].browse(context['location_id'])
        worksheet.write(current_row, 0, u"UBICACION", FORMATS['title'])
        worksheet.write(current_row, 1, location_id.name,)
        current_row += 1
        set_cabecera(workbook, current_row)
        worksheet.autofilter(current_row, 0, current_row, 2)
        current_row += 1
        total = 0
        total_virtual=0
        for d in data:
            total+=int(d['quantity'])
            if context.get('type', False) == 'today':
                total_virtual+= self.env['product.product'].browse(d['product_id']).virtual_available
            set_line(workbook, current_row, d)
            current_row += 1

        worksheet.write(current_row, 2, total, )
        # if context.get('type', False) == 'today':
        #     worksheet.write(current_row, 3, total_virtual, )
        #     worksheet.write(current_row, 4, d['costo_unit'], )
        #     worksheet.write(current_row, 5, d['tot_costo_unit'], )
        # else:
        if context.get('mostrar_costos', False) == True:
            worksheet.write(current_row, 4, d['costo_unit'], )
            worksheet.write(current_row, 5, d['tot_costo_unit'], )


        COLUM_SIZES = [20, 25, 15, 15, 15, 15]
        for position in range(len(COLUM_SIZES)):
            worksheet.set_column(position, position, COLUM_SIZES[position])
        return self.get_workbook_binary(fp, workbook)


class ReportEcKardexAllStock(models.AbstractModel):
    _name = 'report.ec_kardex.report_kardex_all_stock'

    @api.model
    def _get_report_values(self, docids, data=None):
        context = self.env.context.copy()
        if data:
            context.update(data)
        report_model = self.env['report.stock.utils']
        data = report_model.with_context(context).GetKardexAllStockData()
        return {
            'formatLang': partial(formatLang, self.env),
            'format_date': partial(format_date, self.env),
            "products": data
        }
