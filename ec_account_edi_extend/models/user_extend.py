from odoo import models, fields, api
from odoo.exceptions import UserError

class UserExtend(models.Model):
    _inherit = 'res.users'
    
    shop_ids = fields.Many2many(
        'sale.shop',
        'rel_user_shop',
        'user_id',
        'shop_id',
        string='Establecimientos Permitidos', 
    )
    
    printer_default_ids = fields.Many2many(
        'sri.printer.point',
        string='Puntos de emisión',
        required=False,
        index=True,
        auto_join=True,
        help= """Para seleccionar el punto de emision primero debe pertenecer a uno o varios establecimientos."""
    )
    
    filter_orders = fields.Boolean(
        string='Mostrar Solo pedidos de su Establecimiento?',
        readonly=False, 
    )
    
    
    @api.onchange('shop_ids')
    def on_change_shop_ids(self):
        if self.shop_ids:
            # Verificar si hay puntos de emisión que no están asociados a los establecimientos restantes
            shop_ids_set = set(self.shop_ids.ids)

            # Si un punto de emisión está asociado con un establecimiento eliminado
            for printer in self.printer_default_ids:
                if printer.shop_id.id not in shop_ids_set:
                    # Eliminar el punto de emisión de printer_default_ids
                    self.printer_default_ids = [(3, printer.id)]  # Eliminar de Many2many

        else:
            # Si no hay establecimientos, restablecer los puntos de emisión
            self.printer_default_ids = False
    
    
    @api.model
    def get_printer_point(self, user_id=False, get_all=True, raise_exception=True):
        """
        Valida que el usuario tenga configurado establecimiento y punto de emisión.
        @param user_id: int, ID del usuario del que obtener los datos, en caso de no pasar, se tomará el usuario actual (uid)
        @return: list(tuple(printer_id, shop_id), ......)
        """
        if not user_id:
            user_id = self.env.uid
        user = self.browse(user_id)
        res = []
        company_id = False

        # Verificamos la existencia de empresas en el entorno
        if len(self.env.companies) >= 1:
            company_id = self.env.companies[0]

        if company_id:
            # Ahora se trabaja con un Many2many, por lo que se debe iterar sobre todos los registros relacionados
            for printer in user.printer_default_ids:  # Iteramos sobre los registros de la relación Many2many
                if printer.shop_id.company_id == company_id:
                    temp = (printer.id, printer.shop_id.id)
                    if temp not in res:
                        res.append(temp)

            if not res or get_all:
                # Aquí se sigue buscando impresoras asociadas a los puntos de venta del usuario
                for shop in user.shop_ids:
                    if shop.company_id != company_id:
                        continue
                    for printer in shop.printer_point_ids:
                        temp = (printer.id, shop.id)
                        if temp not in res:
                            res.append(temp)

            # Si no se han encontrado resultados y se requiere una excepción
            if not res and raise_exception:
                raise UserError(_(u'Su usuario no tiene configurado correctamente los permisos(Establecimiento, Punto de Emisión), por favor verifique con el administrador'))
        else:
            # Si no hay una sola compañía configurada, se lanza un error
            raise UserError(_(u'Para poder facturar debe seleccionar una sola compañía, por favor verifique con el administrador'))

        # Si no se han encontrado resultados y se requiere una excepción
        if not res and raise_exception:
            raise UserError(_(u'Su usuario no tiene configurado correctamente los permisos(Establecimiento, Punto de Emisión), por favor verifique con el administrador'))

        return res


        
