from odoo import api,models,fields,_
from odoo.exceptions import ValidationError

class TechnicalData(models.Model):
    _name="technical.data"
    _description="Displays technical data for products"
    _order = "para_id"
    
   
    
    product_tmpl_id =fields.Many2one(comodel_name="product.template" , readonly=False, ondelete="cascade")
    product_id = fields.Many2one(string="Product variant", comodel_name="product.product", ondelete="cascade")
    
    para_id = fields.Many2one(comodel_name="parameter.model", string="Parameter", required=True)
    prop = fields.Char(string="Property")
    value = fields.Char(string="Value")
    uom_id = fields.Many2one(comodel_name="uom.uom", string="Unit")
    category_id = fields.Many2one(comodel_name="uom.category", string="UOM Category")
    product_id_prop = fields.Boolean(string="Property of Variant")

    
    @api.constrains('prop','value')
    def _empty_exception(self):
        for rec in self:
            if rec.prop == False and rec.value==False:
                raise ValidationError('Please put data into Property and Value')

    @api.onchange('uom_id')
    def _change_uom_category(self):
        self.category_id = self.para_id.uom_category_id

    @api.onchange('para_id')
    def _change_param_category(self):
        self.category_id = self.para_id.uom_category_id
    

    @api.onchange('para_id')
    def _onchange_para_id(self):
        res = {}
        if self.para_id:
            res['domain'] = {'uom_id': [('category_id', '=', self.para_id.uom_category_id.id)]}
        self.uom_id = False
        return res
    
    @api.model
    def create(self, vals):
        if vals.get('product_tmpl_id') == False or 'product_tmpl_id' not in vals:
            product = self.env['product.product'].browse(vals.get('product_id'))
            product_tmpl = product.product_tmpl_id     
            
            vals['product_tmpl_id']=product_tmpl.id

            existing_product_property = self.env['technical.data'].search([
                ('para_id', '=', vals.get('para_id')),
                ('product_tmpl_id', '=', product_tmpl.id)
            ], limit=1)

            if existing_product_property:
                new_record_draft = {
                            'para_id' : existing_product_property.para_id.id,
                            'prop' : existing_product_property.cond,
                            'value' : existing_product_property.mini,
                            'uom_id': existing_product_property.uom_id.id,
                            'product_tmpl_id' : product_tmpl.id,
                            'product_id_prop' : True,
                        }
                
                existing_product_property.unlink()

                product_vars = product_tmpl.product_variant_ids
                for variant_record in product_vars:
                    if product != variant_record:
                        
                        variant_record.write({
                            'technical': [(0,0,new_record_draft)]
                        })
          
        return super(TechnicalData, self).create(vals)
    
    