{
    'name': 'Product Technical Data',
    'version': '1.0',
    'description': 'Administration of technical data in the backend, presentation of these in the frontend. Supports the native UOM of Odoo to add own units.',
    'summary': 'Technical Data on the product page',
    'author': 'sarah-code',
    'website': 'https://www.github.com/sarah-code',
    'license': 'LGPL-3',
    'category': 'uncategorized',
    'depends': [
        'product',
        'website_sale',
    ],
    'data': [
        'views/technical_data_view.xml',
        'views/web_template.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        ''
    ],
    'auto_install': False,
    'application': False,
}