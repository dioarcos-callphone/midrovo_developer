try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    # TODO saas-17: remove the try/except to directly import from misc
    import xlsxwriter
import io
from odoo import api, fields, models, tools, _

class CenReportXlsx(models.Model):
    _name = 'cen.report.xlsx'
    _description = "Modulo XLXS"

    @api.model
    def create_workbook(self, page_string=''):
        fp = io.BytesIO()
        # crear el reporte en memoria, no en archivo
        workbook = xlsxwriter.Workbook(fp, {'in_memory': True, 'constant_memory': False})
        worksheet = workbook.add_worksheet(page_string)
        FORMATS = {
            'title': workbook.add_format({'bold': True,'align': 'center', 'valign': 'vcenter','font_color': 'white','bg_color': '#0F1570','border':1}),
            'bold': workbook.add_format({'bold': True, 'text_wrap': True}),
            'border': workbook.add_format({'border':1}),
            'single_bold': workbook.add_format({'bold': True}),
            'center_cell': workbook.add_format({'align': 'center'}),
            'bold_border': workbook.add_format({'bold': True,'border':1}),
            'number': workbook.add_format({'num_format': '#,##0.00'}),
            'number_0f': workbook.add_format({'num_format': '#,##0'}),
            'porcentaje': workbook.add_format({'num_format': '0%_)'}),
            'money': workbook.add_format({'num_format': '$#,##0.00'}),
            'money0f': workbook.add_format({'num_format': '$#,##0'}),
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