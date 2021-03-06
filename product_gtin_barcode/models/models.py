# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError

import re
import math

VALID_GTIN_LENGTH = [8, 12, 13, 14]


def validate_gtin_barcode(barcode):
    # https://www.gs1.org/services/how-calculate-check-digit-manually
    raw_barcode, raw_cheksum = barcode[:-1], int(barcode[-1])

    revl_barcode = map(lambda x: int(x), reversed(raw_barcode))
    factors = reversed([1, 3] * int(math.ceil(len(raw_barcode) / 2)))
    factor_sum = sum(map(lambda x: x[0] * x[1], zip(revl_barcode, factors)))
    f_mod10 = factor_sum % 10
    checksum = (f_mod10 and factor_sum + 10 - f_mod10 or factor_sum) - factor_sum
    return checksum == raw_cheksum, checksum


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('barcode')
    def _check_gtin_barcode(self):
        for record in self:
            if record.barcode:
                m = re.match(r'^([0-9]+)$', record.barcode)
                if not m:
                    raise ValidationError(_("A GTIN barcode must contain numeric digits "
                                            "only (spaces are not allowed either)"))
                barcode = m.group(1)
                if len(barcode) not in VALID_GTIN_LENGTH:
                    raise ValidationError(_("A GTIN barcode must have the following lengths %s") % VALID_GTIN_LENGTH)

                valid, checksum = validate_gtin_barcode(barcode)
                if not valid:
                    raise ValidationError(_("Wrong check digit! The last digit should be %d") % checksum)

                m = re.match(r'^0*([0-9]+)$', barcode)
                product_barcode_trim = m.group(1)
                products = self.env['product.product'].with_context(active_test=False).search([
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id),
                    ('barcode', '=like', '%' + product_barcode_trim),
                ])
                products_match = products.filtered(
                    lambda x: re.match(r'^0*(%s)$' % product_barcode_trim, x.barcode))
                if products_match:
                    raise ValidationError(_("The GTIN is already assigned to following products: %s") % (
                        products_match.mapped('display_name'),
                    ))
