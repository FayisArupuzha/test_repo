from odoo import fields,models,api

class RuleSetupOvertime(models.Model):
    _inherit ="hr.payslip"

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
    def _compute_input_line_ids(self):
        res = super(RuleSetupOvertime, self)._compute_input_line_ids()
        for each in self:
            if each.employee_id:
                employee = each.employee_id


                loan_obj = self.env["overtime"].search([("employee_id", "=", employee.id),])
                date_from = each.date_from if each.date_from else date_from
                date_to = each.date_to if each.date_to else date_to

                existing_rule = self.struct_id.rule_ids.filtered(lambda x: x.code == "PF")
                # hr.work.entry.type
                if existing_rule:
                    


                    power =self.env['hr.work.entry.type'].search([('code','=','LEAVE90')])
                    for line in self.worked_days_line_ids:
                        if line.work_entry_type_id.id == power.id:
                            s= line.number_of_days 
                    if power.code  in self.worked_days_line_ids.mapped("code") and s >= 4:
                        pf_amount = 0
                    else:
                        pf_amount =  (self.normal_wage * 12.5) / 100
                            
                    input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "PF")], limit=1)
                    to_add_vals = [(0, 0, {
                        'amount': -(pf_amount),
                        'input_type_id': input_type_id.id,
                        'name': "PF"
                    })]
                    input_line_vals = to_add_vals
                    self.update({'input_line_ids': input_line_vals})
                            
                            
                      


        return res