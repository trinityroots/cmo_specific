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
        if len(po_approved) > 0:
            raise UserError(_('You can not Payment to reconcile invoice  '
                              'for purchase order that not Purchase Confirmed. %s' 
                              % tuple(set(po_approved))))


        return super(AccountVoucher, self).proforma_voucher()
