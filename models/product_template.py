from odoo import api,models,fields

class ProductTemplate(models.Model):
    _inherit="product.template"
    
    technical = fields.One2many(comodel_name="technical.data", inverse_name="product_tmpl_id", string="Technical Data")  

    
    

class ProductProduct(models.Model):
    _inherit="product.product"

    technical = fields.One2many(comodel_name="technical.data", inverse_name="product_id", string="Technical Data")
                

    

    
