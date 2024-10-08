from odoo import api, models
from odoo.exceptions import ValidationError
from datetime import datetime

class StockQuantityHistory(models.AbstractModel):
    _name = 'report.inventory_report_location.report_stock_quantity'
    _description = 'Stock Quantity History'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        productos = data['productos']
        localidad_fecha = ''
        
        locations = self.env.context.get('location',[])
        fecha = self.env.context.get('date',[])
        
        fecha_date = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').date()
        fecha_str_convertida = fecha_date.strftime('%d/%m/%Y')
        
        if locations:
            for location in locations:
                localidad = self.env['stock.location'].search([
                    ('id','=', location)
                ])
                localidad_fecha = str(localidad_fecha) + " " + str(localidad.complete_name)
                
            localidad_fecha += " - " + str(fecha_str_convertida)            
            
        if productos:
            return {
                'doc_ids': docids,
                'doc_model': 'report.stock.quantity.history',
                'options': productos,
                'total_cantidad': data['total_cantidad'],
                "total_valor_stock" : data['total_valor_stock'],
                'localidad_fecha': localidad_fecha if localidad_fecha != '' else fecha_str_convertida
            }
            
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")
                