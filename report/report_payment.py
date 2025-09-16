# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.addons.l10n_sv import a_letras

class ReportAbstractPayment(models.AbstractModel):
    _name = 'bright_solutions_sv.abstract.reporte_account_payment'
    
    def totales(self, o):
        t = {'debito': 0, 'credito': 0}
        for l in o.move_id.line_ids:
            t['debito'] += l.debit
            t['credito'] += l.credit
        return t
    
    def a_letras(self,monto):
        return a_letras.num_a_letras(monto)
    
    def _get_report_values(self, docids, data=None):
        model = 'account.payment'
        docs = self.env['account.payment'].browse(docids)
        
        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'a_letras': self.a_letras,
            'totales': self.totales,
        }
        
class ReportPayment1(models.AbstractModel):
    _name = 'report.bright_solutions_sv.reporte_account_payment1'
    _inherit = 'bright_solutions_sv.abstract.reporte_account_payment'
    
class ReportPayment2(models.AbstractModel):
    _name = 'report.bright_solutions_sv.reporte_account_payment2'
    _inherit = 'bright_solutions_sv.abstract.reporte_account_payment'

class ReportPayment3(models.AbstractModel):
    _name = 'report.bright_solutions_sv.reporte_account_payment3'
    _inherit = 'bright_solutions_sv.abstract.reporte_account_payment'
