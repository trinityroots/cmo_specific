# -*- coding: utf-8 -*-

from openerp import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.multi
    # @api.depends('order_line.price_subtotal')
    # def _amount_all(self):
    #     res = super(SaleOrder, self)._amount_all()
    #     for order in self:
    #         if order.project_related_id:
    #             project_id = order.project_related_id
    #             project_id.date_last_modify = fields.datetime.now()
    #     return res

    @api.onchange('state', 'amount_total')
    def _onchange_project_track(self):
        if self.project_related_id:
            self.project_related_id.date_last_modify = fields.datetime.now()