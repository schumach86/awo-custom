# -*- coding: utf-8 -*-
# Copyright 2016 Rooms For (Hong Kong) Limited T/A OSCG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    return_category = fields.Selection(
        [('repair', 'Repair'),
        ('return_company', 'Return ­ Company'),
        ('return_vci', 'Return - VCI'),
        ('return_no_ownership_change', 'Return ­ No Ownership Change')],
        string='Return Category',
        default='return_no_ownership_change',
    )

    @api.model
    def _validate_owner(self):
        if self.picking_type_id.code != 'incoming':
            return True
        if not self.owner_id:
            return True
        if self.owner_id == self.company_id.partner_id:
            return True
        if self.owner_id.customer:
            if self.owner_id == self.partner_id:
                return True
        if self.owner_id.supplier:
            for move in self.move_lines:
                if move.reserved_quant_ids:
                    for quant in move.reserved_quant_ids:
                        if quant.owner_id:
                            if self.owner_id != quant.owner_id:
                                return False
        return True

    @api.one
    @api.onchange('owner_id')
    def onchange_owner(self):
        if not self._validate_owner():
            raise Warning(_('You can not set owner other than customer on \
                return shipment or supplier on reserved quants of moves.'))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
