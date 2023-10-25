from odoo import fields, models, api


class RuleSetupOvertime(models.Model):
    _inherit = 'hr.payslip'

    @api.depends('employee_id', 'contract_id', 'struct_id', 'date_from', 'date_to')
    def _compute_input_line_ids(self):
        res = super(RuleSetupOvertime, self)._compute_input_line_ids()
        for each in self:
            if each.employee_id:
                employee = each.employee_id
                existing_rule = self.struct_id.rule_ids.filtered(lambda x: x.code == "TDS999")
                # hr.work.entry.type
                if existing_rule:
                    rec = self.env['hr.contract'].search([('employee_id','=',employee.id)])
                    input_type_id = self.env['hr.payslip.input.type'].search([('code', '=', "TDS999")], limit=1)
                    to_add_vals = [(0, 0, {
                        'amount': -(rec.tds),
                        'input_type_id': input_type_id.id,
                        'name': "TDS"
                    })]
                    input_line_vals = to_add_vals
                    self.update({'input_line_ids': input_line_vals})