from odoo import models, api, exceptions, fields
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        # Comprobar si se está intentando actualizar un registro creado por un usuario restringido
        for record in self:
            # Comprobar si el usuario pertenece al grupo con acceso limitado
            if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
                # Obtener la fecha de creación del registro
                fecha_creacion = record.create_date
                # Obtener la fecha y hora actual en la zona horaria de Odoo
                fecha_actual = datetime.now()

                # Comparar las fechas redondeando los microsegundos
                if fecha_creacion.replace(microsecond=0) == fecha_actual.replace(microsecond=0):
                    # Permitir la actualización si las fechas coinciden
                    return super(ResPartner, self).write(vals)
                else:
                    # Lanzar un error si no coinciden
                    raise exceptions.AccessError("No tienes permisos para actualizar contactos.")

        # Si no se encuentra una restricción, permitir la operación
        return super(ResPartner, self).write(vals)
    
    def unlink(self):
        # Verificar si el usuario pertenece al grupo restringido
        if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
            raise exceptions.AccessError("No tienes permiso para eliminar este registro.")
        
        # Lógica personalizada antes de eliminar, si es necesario
        return super(ResPartner, self).unlink()