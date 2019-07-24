# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Sale Order Ambugest',
    'summary': 'This module adds Ambugest specific data to sale orders',
    'version': '11.0.0.1.1',
    'category': 'Sales',
    'author': 'NuoBiT Solutions, S.L., Eric Antones',
    'website': 'https://www.nuobit.com',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}