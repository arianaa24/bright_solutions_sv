from odoo import api, fields, models, _
import logging

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    margen_total = fields.Float(string="Margen Total %", compute="_compute_margenes", store=True)
    margen_final = fields.Float(string="Margen Final %", compute="_compute_margenes", store=True)
    porcentaje_administrativo = fields.Float(string="Porcentaje Administrativo %", related='sale_order_template_id.porcentaje_administrativo', store=True)
    monto_administrativo = fields.Float(string="Monto Administrativo")
    monto_total = fields.Float(string="Monto Total")
    monto_final = fields.Float(string="Monto Final")

    @api.depends("order_line.vc", "order_line.price_subtotal", "order_line.monto_ejecutado")
    def _compute_margenes(self):
        for order in self:
            total_vc = sum(line.vc for line in order.order_line)
            total_price_subtotal = sum(line.price_subtotal for line in order.order_line)
            total_monto_ejecutado = sum(line.monto_ejecutado for line in order.order_line)
            order.margen_total = (total_vc / total_price_subtotal) - order.porcentaje_administrativo if total_price_subtotal != 0 else 0
            margen_final = total_price_subtotal - total_monto_ejecutado
            order.margen_final = (margen_final / total_price_subtotal) - order.porcentaje_administrativo if total_price_subtotal != 0 else 0
            order.monto_administrativo = total_price_subtotal * order.porcentaje_administrativo
            order.monto_total = total_price_subtotal * order.margen_total
            order.monto_final = total_price_subtotal * order.margen_final
    
    def btn_calcular_monto_ejecutado(self):
        for so_line in self.order_line:
            purchase_order_lines = self.env['purchase.order.line'].search([('order_id.sale_order_id','=',self.id), ('state','in',['purchase','done']), ('product_id','=',so_line.product_id.id)])
            so_line.monto_ejecutado = sum(purchase_order_lines.mapped('price_subtotal'))

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dias = fields.Integer(string="Días")
    precio_unitario_dias = fields.Float(string="Precio unitario por día", digits=(12,2))
    costo_total = fields.Monetary(string="Costo Total")
    vc = fields.Monetary(string="VC")
    margen = fields.Float(string="Margen %")
    monto_ejecutado = fields.Float(string="Monto Ejecutado")
    costo_total_recuperacion = fields.Monetary(string="Costo total de recuperación")

    @api.onchange("product_id")
    def _onchange_producto(self):
        self.precio_unitario_dias = self.product_id.list_price

    @api.onchange("dias", "precio_unitario_dias","product_uom_qty")
    def _onchange_price(self):
        self.price_unit = self.dias * self.precio_unitario_dias

    @api.onchange("x_studio_costo","precio_unitario_dias", "product_uom_qty", "dias")
    def _onchange_product_brighsolutions(self):
        for record in self:
            record.costo_total = record.product_uom_qty * record.dias * record.x_studio_costo
            record.costo_total_recuperacion = record.product_uom_qty * record.dias * record.product_id.costo_recuperacion
            record.vc = record.price_subtotal - record.costo_total - record.costo_total_recuperacion
            if record.price_subtotal:
                record.margen = record.vc / record.price_subtotal
