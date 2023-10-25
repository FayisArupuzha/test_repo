from odoo import fields, models, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    tds = fields.Float(string="TDS")
