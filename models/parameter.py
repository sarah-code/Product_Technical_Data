from odoo import api,fields,models

class Parameter(models.Model):
    _name='parameter.model'
    _description='Provides symbols and parameter'

    name=fields.Char(string="Parameter")
    uom_category_id=fields.Many2one(comodel_name="uom.category", string="Uom Category")