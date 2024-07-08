from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import calendar
import random
import time
from datetime import datetime, timedelta

class ContratoPadre(models.Model):
    _inherit = 'fleet.vehicle.log.contract'
    _name="fleet.contrato.padre"
    #Cambiar a formato CONT/año/mes/correlativo al crear"
    codigo = fields.Char(string="Código", required=True, index=True)
    #Override
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', required=False, help='Vehicle concerned by this log', check_company=True)

    contrato_padre_id = fields.Many2one(
        'fleet.contrato.padre',
        'Contrato padre',
        required=False,
        help='Help contrato padre',
    )

   

    
    

    #Language override

    user_id = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user, index=True)
    cost_subtype_id = fields.Many2one('fleet.service.type', 'Tipo', help='Cost type purchased with this cost', domain=[('category', '=', 'contract')])
    insurer_id = fields.Many2one('res.partner', 'Proveedor')
    ins_ref = fields.Char('Referencia', size=64, copy=False)
    company_id = fields.Many2one('res.company', 'Compañia', default=lambda self: self.env.company)
    amount = fields.Monetary('Coste de activación')
    cost_generated = fields.Monetary('Coste recurrente')
    date = fields.Date('Fecha de factura',help='Date when the cost has been executed')

    start_date = fields.Date(
        'Fecha de inicio del contrato', default=fields.Date.context_today,
        help='Date when the coverage of the contract begins')
    expiration_date = fields.Date(
        'Fecha de vencimiento del contrato', default=lambda self:
        self.compute_next_year_date(fields.Date.context_today(self)),
        help='Date when the coverage of the contract expirates (by default, one year after begin date)')
    cost_frequency = fields.Selection([
        ('no', 'No'),
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
        ('yearly', 'Anual')
        ], 'Frecuencia del coste recurrente', default='monthly', help='Frequency of the recuring cost', required=True)
   

    #Begin Testing update, comment if not needed

    contrato_hijos = fields.One2many('fleet.vehicle.log.contract', 'contrato_padre_id', string='Contrato Hijos')
    #cantidad_hijos = fields.Integer(string='Hijos', compute='_compute_number_of_children', store=True)

    #End Testing


    ##Agregar contabilidad analitica



    @api.onchange('start_date')
    def _compute_codigo(self):
    
        if not self.codigo:
            date=fields.Date.from_string(self.start_date)
            year = date.strftime('%Y')
            month = date.strftime('%m')
            id=self._get_next_id()
            #correlativo =self._compute_correlativo_date()
            correlativo=self._compute_correlativo_random()

            current_month = datetime.now().month
            current_year = datetime.now().year
    
            
            
            codigo = f"{id:03d}{current_year:02d}{current_month:02d}{correlativo}" 

            self.codigo=codigo



    @api.depends('start_date')
    def _compute_contract_name(self):
        for record in self:
            name = record.codigo
            if name and record.start_date:
                name = record.codigo
            record.name = name


    
    def _compute_correlativo_random(self):
        random_number = format(random.randint(1, 999999), '06')
        existing_contracts=self._compute_existing_contracts()

        formated_contract_number=self._format_contract_number(len(existing_contracts) + 1)
        return random_number+formated_contract_number

    def _get_next_id(self):
        highest_id = self.search([], order="id desc", limit=1).id
        return highest_id + 1 if highest_id else 1


    def _compute_correlativo_date(self):
        
        

        existing_contracts = self._compute_existing_contracts()
        current_time = datetime.now().strftime('%H%M%S')

        current_time_utc_minus_3 = (datetime.utcnow() - timedelta(hours=3)).strftime('%H%M%S')
        formated_contract_number=self._format_contract_number(len(existing_contracts) + 1)

        correlativo = current_time_utc_minus_3+formated_contract_number

        

        return correlativo
    
    def _format_contract_number(self, number):
        return f"{number:03d}" if number < 100 else str(number)
    
    def _compute_existing_contracts(self):
        #Current date
        date=fields.Date.context_today(self)
        year = date.strftime('%Y')
        month = date.strftime('%m')
        year_int = date.year
        month_int = date.month
         
        last_day_of_month = (calendar.monthrange(year_int,month_int)[1])
        last_day_of_month_str=str(last_day_of_month)

        existing_contracts = self.search([
                    ('start_date', '>=', f"{year}-{month}-01"),
                    ('start_date', '<=', f"{year}-{month}-{last_day_of_month_str}"),
                ])
        
        return existing_contracts
    

   

    #----Children test----
    #Override

    
    def write(self, vals):
        
        result = super(ContratoPadre, self).write(vals)

        #Si se necesita actualizar datos de hijos segun padre, usar self._update_child_contracts()
        #self._update_child_contracts()
        #Si se necesita cerrar  estado de hijos al cerrar el padre, usar self._update_child_states()
        #self._update_child_states()

        return result

    def _update_child_contracts(self):
        for contrato_hijo in self.contrato_hijos:
            contrato_hijo.update_from_parent()

    def _update_child_states(self):
        for contrato_hijo in self.contrato_hijos:
            contrato_hijo.update_from_parent_state()


    @api.depends('contrato_hijos')
    def _compute_number_of_children(self):
        for record in self:
            record.cantidad_hijos = len(record.contrato_hijos)


##TODO: close parent contract and close children



