# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        for line in order.order_line:
            sum_qty_product = 0
            if line.product_id.tracking == 'lot':
                stock_quants = self.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('on_hand', '=', True)])
                for stock_line in stock_quants :
                    removal_date = stock_line.removal_date
                    if removal_date and (removal_date > fields.Datetime.now()) :
                        sum_qty_product += stock_line.inventory_quantity_auto_apply
                if sum_qty_product < line.product_uom_qty:
                    warning_message = f" Attention : Le lot du produit {line.product_id.name} expire très prochainement."
                    raise UserError(warning_message)

        return order