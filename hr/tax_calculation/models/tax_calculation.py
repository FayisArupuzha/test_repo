from odoo import fields, models, api


class RuleSetupOvertime(models.Model):
    _inherit = 'hr.payslip'

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
    def _compute_input_line_ids(self):
        res = super(RuleSetupOvertime, self)._compute_input_line_ids()
        if self.input_line_ids:
            for each in self.input_line_ids:
                if each:
                    print("...............................................",each)
                    each.unlink()
                else:
                    pass



        for each in self:
            if each.employee_id:
                employee = each.employee_id
                existing_rule = self.struct_id.rule_ids.filtered(lambda x: x.code == "PF100")
                # hr.work.entry.type
                if existing_rule:
                    pf_amount = (self.normal_wage * 12.5) / 100
                    input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "PF")], limit=1)
                    to_add_vals = [(0, 0, {
                        'amount': -(pf_amount),
                        'input_type_id': input_type_id.id,
                        'name': "PF"
                    })]
                    input_line_vals = to_add_vals
                    self.update({'input_line_ids': input_line_vals})


                existing_rule_new = self.struct_id.rule_ids.filtered(lambda x: x.code == "TDS100")

                # hr.work.entry.type
                if existing_rule_new:
                    if self.normal_wage * 12 <= 250000:
                        input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "TDS")], limit=1)
                        to_add_vals = [(0, 0, {
                            'amount': 0,
                            'input_type_id': input_type_id.id,
                            'name': "TDS"
                        })]
                        input_line_vals = to_add_vals
                        self.update({'input_line_ids': input_line_vals})
                    #above 250001 and under 500000
                    elif self.normal_wage * 12 >= 250001 and self.normal_wage * 12 <= 500000:
                        tds_amount = (self.normal_wage * 5) / 100
                        input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "TDS")], limit=1)
                        to_add_vals = [(0, 0, {
                            'amount': -(tds_amount),
                            'input_type_id': input_type_id.id,
                            'name': "TDS"
                        })]
                        input_line_vals = to_add_vals
                        self.update({'input_line_ids': input_line_vals})
                    # above 500001 and under 1000000
                    elif self.normal_wage * 12 >= 500001 and self.normal_wage * 12 <= 1000000:
                        tds_amount =12500 /12 + (self.normal_wage * 20) / 100
                        input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "TDS")], limit=1)
                        to_add_vals = [(0, 0, {
                            'amount': -(tds_amount),
                            'input_type_id': input_type_id.id,
                            'name': "TDS"
                        })]
                        input_line_vals = to_add_vals
                        self.update({'input_line_ids': input_line_vals})
                    #above 1000000
                    elif self.normal_wage * 12 >1000000:
                        tds_amount =112500 /12 + (self.normal_wage * 30) / 100
                        input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "TDS")], limit=1)
                        to_add_vals = [(0, 0, {
                            'amount': -(tds_amount),
                            'input_type_id': input_type_id.id,
                            'name': "TDS"
                        })]
                        input_line_vals = to_add_vals
                        self.update({'input_line_ids': input_line_vals})
#
#
        return res