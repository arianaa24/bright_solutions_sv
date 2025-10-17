from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    costo_recuperacion = fields.Monetary(string="Costo de recuperación")