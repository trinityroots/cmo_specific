# -*- coding: utf-8 -*-

from openerp import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.depends('order_line.price_subtotal')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            amount_discount = amount_before_discount = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += self._amount_line_tax(line)
                if order.order_type == 'sale_order' and \
                   order.use_multi_customer is True:
                    line.discount = 0
                amount_discount += cur.round(
                    line.product_uom_qty * line.price_unit *
                    line.discount / 100
                )
                amount_before_discount += (line.product_uom_qty *
                                           line.price_unit)
            order.amount_untaxed = cur.round(amount_untaxed)
            order.amount_tax = cur.round(amount_tax)
            order.amount_discount = cur.round(amount_discount)
            order.amount_total = order.amount_untaxed + order.amount_tax
            order.amount_before_discount = amount_before_discount
            if order.project_related_id:
                project_id = order.project_related_id
                project_id.write({
                    'date_sale_modify': fields.Datetime.now()
                })
