from odoo import api, fields, models, _

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    porcentaje_administrativo = fields.Float(string="Porcentaje Administrativo %")