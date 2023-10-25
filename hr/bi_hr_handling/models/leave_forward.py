from odoo import models,fields,api

class LeaveForward(models.Model):
    _inherit ='hr.leave'

    def action_done(self):
        pass