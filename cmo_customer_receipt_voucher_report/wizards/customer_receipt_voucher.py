# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class CustomerReceiptVoucher(models.TransientModel):
    _name = 'customer.receipt.voucher'

    voucher_ids = fields.Many2many(
        'account.voucher',
        string='Customer Payments',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
    )
    is_cheque = fields.Boolean(
        string='Cheque ?',
    )

    @api.multi
    def action_get_report(self):
        self.ensure_one()
        # Get Result Report
        Result = self.env['report.customer.receipt.voucher']
        dom = []
        if self.partner_id:
            dom += [('voucher_id.partner_id', '=', self.partner_id.id)]
        if self.voucher_ids:
            dom += [('voucher_id', 'in', self.voucher_ids.ids)]
        result = Result.search(dom)
        if not result:
            raise UserError(_('Error!'), _('No Data.'))
        # Get PDF Report
        report_name = \
            'cmo_customer_receipt_voucher_report.customer_receipt_voucher_pdf'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': report_name,
            'datas': {'ids': result.ids, 'model': result._name, },
        }
