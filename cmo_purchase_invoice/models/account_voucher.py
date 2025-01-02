# -*- coding: utf-8 -*-
from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    @api.multi
    def proforma_voucher(self):
        """ You can not Payment to reconcile invoice  
            for purchase order that not Purchase Confirmed """
        po_approved = []
        for rec in self.line_dr_ids:
            if rec.move_line_id:
                move_id = rec.move_line_id
                move_line = self.env['account.move.line'].search(
                    [('id', '=', move_id.id)]
                )
                print('\n move_line',move_line)
                print('\n move_line.invoice',move_line.invoice, move_line.invoice.name)
                po = self.env['purchase.order'].search([('invoice_ids', 'in', move_line.invoice.ids)])
                if po and po.state != 'approved':
                    po_approved.append(po.name)
                print('\n po',po)
                # open_invoices = self.invoice_ids.filtered(lambda l: l.state in ['open', 'paid'])
        if len(po_approved) > 0:
            raise UserError(_('You can not Payment to reconcile invoice  '
                              'for purchase order that not Purchase Confirmed. %s' 
                              % tuple(set(po_approved))))
        # for voucher in self:
        #     # auto reconcile special account, get all releated move_lines
        #     v_mlines = voucher.mapped('move_id.line_id')
        #     i_mlines = voucher.mapped('line_ids.invoice_id.move_id.line_id')
        #     tt_mlines = \
        #         voucher.mapped('recognize_vat_move_id.line_id')
        #     print tt_mlines
        #     mlines = v_mlines | i_mlines | tt_mlines
        #     mlines.reconcile_special_account()
        a=a
        res = super(AccountVoucher, self).proforma_voucher()

        return res
