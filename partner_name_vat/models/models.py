# -*- coding: utf-8 -*-
# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def name_get(self):
        result = []
        orig_name = dict(super(ResPartner, self).name_get())
        for partner in self:
            name = orig_name[partner.id]
            if partner.vat:
                name = "%s (%s)" % (name, partner.vat)

            result.append((partner.id, name))

        return result
