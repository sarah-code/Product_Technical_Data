from odoo import api,models,fields,_
from odoo.exceptions import ValidationError

class TechnicalData(models.Model):
    _name="technical.data"
    _description="Displays technical data for products"
    _order = "component_name"
    
   
    
    product_tmpl_id =fields.Many2one(comodel_name="product.template" , readonly=False, ondelete="cascade")
    product_id = fields.Many2one(string="Product variant", comodel_name="product.product", ondelete="cascade")
    
    component_name = fields.Many2one(comodel_name="parameter.model", string="Component", required=True)
    component_type = fields.Char(string="Component Type")
    value = fields.Char(string="Value")
    uom_id = fields.Many2one(comodel_name="uom.uom", string="Unit")
    category_id = fields.Many2one(comodel_name="uom.category", string="UOM Category")
    product_id_prop = fields.Boolean(string="Property of Variant")

    
    @api.constrains('component_type','value')
    def _empty_exception(self):
        for rec in self:
            if rec.component_type == False and rec.value==False:
                raise ValidationError('Please put data into Property and Value')

    @api.onchange('uom_id')
    def _change_uom_category(self):
        self.category_id = self.component_name.uom_category_id

    @api.onchange('component_name')
    def _change_param_category(self):
        self.category_id = self.component_name.uom_category_id
    

    @api.onchange('component_name')
    def _onchange_component_name(self):
        res = {}
        if self.component_name:
            res['domain'] = {'uom_id': [('category_id', '=', self.component_name.uom_category_id.id)]}
        self.uom_id = False
        return res
    
    @api.model
    def create(self, vals):
        if vals.get('product_tmpl_id') == False or 'product_tmpl_id' not in vals:
            product = self.env['product.product'].browse(vals.get('product_id'))
            product_tmpl = product.product_tmpl_id     
            
            vals['product_tmpl_id']=product_tmpl.id

            existing_product_property = self.env['technical.data'].search([
                ('component_name', '=', vals.get('component_name')),
                ('product_tmpl_id', '=', product_tmpl.id)
            ], limit=1)

            if existing_product_property:
                new_record_draft = {
                            'component_name' : existing_product_property.component_name.id,
                            'component_type' : existing_product_property.cond,
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
    
    