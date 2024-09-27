import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    """This model is used to connect the frontend to the backend"""

    @http.route('/xlsx_reports', type='http', auth='public', methods=['POST'],
                csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name):
        """This function is called when a post request is made to this route"""
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(report_name + '.xlsx'))
                    ])
                report_obj.get_xlsx_report(options, response)
            response.set_cookie('fileToken', token)
            return response
        except Exception as exception:
            serialise = http.serialize_exception(exception)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': serialise
            }
            return request.make_response(html_escape(json.dumps(error)))
