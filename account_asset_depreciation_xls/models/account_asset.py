# -*- coding: utf-8 -*-
# Copyright 2009-2017 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from openerp import api, models

_logger = logging.getLogger(__name__)


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    @api.model
    def post_first_asset(self):
        assets = self.env['account.asset'].search([
            ('state', '=', 'open'),
            ('number', 'not in', (
                'TE12181-000180',
                'TE12151-000159',
                'TE12151-000029',
                'TE12151-000678',
                'TE12161-000002',
                'TE12151-000010',
                'TE12151-000396',
            )),
        ])
        for asset in assets:
            try:
                if len(asset.depreciation_line_ids) == 2:
                    if asset.depreciation_line_ids[1].type == 'depreciate':
                        asset.depreciation_line_ids[1].create_move()
                        self._cr.commit()
            except Exception:
                _logger.info(asset.number)

    @api.model
    def _xls_acquisition_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'account', 'name', 'operating_unit_id', 'code', 'date_start',
            'depreciation_base', 'salvage_value',
        ]

    @api.model
    def _xls_active_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'account', 'name', 'date_purchase', 'date_start', 'purchase_value',
            'asset_value_previous', 'percent', 'salvage_value',
            'asset_line_amount', 'depreciated_value', 'remaining_value',
            'operating_unit_id', 'code', 'note',
        ]  # 'depreciation_base' 'fy_start_value' 'fy_depr', 'fy_end_value',
        # 'fy_end_depr', 'method', 'method_number', 'prorata', 'residual_value'

    @api.model
    def _xls_removal_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            'account', 'name', 'date_purchase', 'date_start', 'date_remove',
            'purchase_value', 'asset_value_previous', 'percent',
            'salvage_value', 'asset_line_amount',
            'depreciated_value', 'remaining_value',
            'operating_unit_id', 'code', 'note',
            # 'depreciation_base',

        ]

    @api.model
    def _xls_acquisition_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_active_template(self):
        """
        Template updates

        """
        return {}

    @api.model
    def _xls_removal_template(self):
        """
        Template updates

        """
        return {}
