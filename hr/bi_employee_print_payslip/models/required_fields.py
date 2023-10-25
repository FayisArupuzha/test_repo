from odoo import models,fields

class EmployeeRequiredFields(models.Model):
    _inherit="hr.employee"
    pan_card=fields.Char(string="PAN Number")
    esi_number = fields.Char(string="ESI Number")
    uan_number = fields.Char(string="UAN Number")