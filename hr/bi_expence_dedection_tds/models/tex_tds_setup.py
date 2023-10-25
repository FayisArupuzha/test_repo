from odoo import fields,models,api

class TdsCalculationSetup(models.Model):
    _name ="account.tds.setup"
    _rec_name ='year'

    year = fields.Integer(string="year")
    line_ids = fields.One2many('account.tds.setup.line','line_id',string="Line ids")


class TdsCalculationSetup(models.Model):
    _name ="account.tds.setup.line"

    line_id = fields.Many2one('account.tds.setup',string='line id')

    amount_from = fields.Float(string='Amount From')
    amount_to = fields.Float(string='Amount To')
    tax_percentage = fields.Float(string='Tax')


