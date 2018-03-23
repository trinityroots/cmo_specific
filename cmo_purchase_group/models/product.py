# -*- coding: utf-8 -*-
from openerp import models, api
from .common import Common


class ProductProduct(models.Model, Common):
    _inherit = 'product.product'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(ProductProduct, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu)
        user = self.env.user
        manager_readonly_group = \
            'cmo_purchase_group.group_purchase_manager_readonly'
        if user.has_group(manager_readonly_group):
            res = self.set_right_readonly_group(res)
        return res


class ProductTemplate(models.Model, Common):
    _inherit = 'product.template'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(ProductTemplate, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu)
        user = self.env.user
        manager_readonly_group = \
            'cmo_purchase_group.group_purchase_manager_readonly'
        if user.has_group(manager_readonly_group):
            res = self.set_right_readonly_group(res)
        return res


class ProductCategory(models.Model, Common):
    _inherit = 'product.category'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(ProductCategory, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu)
        user = self.env.user
        manager_readonly_group = \
            'cmo_purchase_group.group_purchase_manager_readonly'
        if user.has_group(manager_readonly_group):
            res = self.set_right_readonly_group(res)
        return res
