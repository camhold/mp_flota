from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ContratoHijo(models.Model):
    _inherit = 'fleet.vehicle.log.contract'


    #_name="fleet.vehicle.log.contract"
    #test
    #contrato_padre_id = fields.Many2one('fleet.contrato.padre', 'Contrato padre', default=lambda self: self.env.contract)

    #contrato_padre_id = fields.Many2one('fleet.contrato.padre', 'Contrato padre', required=True, help='Help1')

    contrato_padre_id = fields.Many2one(
        'fleet.contrato.padre',
        'Contrato padre',
        required=True,
        help='Help contrato padre',
        #domain="[('codigo', '=', codigo)]" 
    )

    vehicle_contract_count = fields.Integer(
        related='vehicle_id.contract_count',
        string='Vehicle Contract Count',
        store=False,
        readonly=True
    )

   # vehicle_id = fields.Many2one(
   #     'fleet.vehicle',
   #     'Vehicle',
   #     required=True,
   #     help='Vehicle concerned by this log',
   #     check_company=True,
   #     domain="[('contract_count', '=', '0'))]"
   # )

   


    @api.onchange('contrato_padre_id')
    def onchange_contrato_padre_id(self):


        self.user_id=self.contrato_padre_id.user_id.id
        self.cost_subtype_id=self.contrato_padre_id.cost_subtype_id.id
        self.insurer_id=self.contrato_padre_id.insurer_id.id
        #self.vehicle_id=self.contrato_padre_id.vehicle_id.id
        self.company_id=self.contrato_padre_id.company_id.id
        #Costos
        self.amount=self.contrato_padre_id.amount
        self.cost_generated=self.contrato_padre_id.cost_generated
        self.cost_frequency=self.contrato_padre_id.cost_frequency
        #Fechas
        self.date=self.contrato_padre_id.date
        self.start_date=self.contrato_padre_id.start_date
        self.expiration_date=self.contrato_padre_id.expiration_date
       
        self.ins_ref = self.contrato_padre_id.ins_ref

   
    
    #Test update after change in padre
        
    def update_from_parent(self):
        self.user_id = self.contrato_padre_id.user_id.id
        self.cost_subtype_id = self.contrato_padre_id.cost_subtype_id.id
        self.insurer_id = self.contrato_padre_id.insurer_id.id
        self.company_id = self.contrato_padre_id.company_id.id
        self.amount = self.contrato_padre_id.amount
        self.cost_generated = self.contrato_padre_id.cost_generated
        self.cost_frequency = self.contrato_padre_id.cost_frequency
        self.date = self.contrato_padre_id.date
        self.start_date = self.contrato_padre_id.start_date
        self.expiration_date = self.contrato_padre_id.expiration_date
        self.ins_ref = self.contrato_padre_id.ins_ref

    def update_from_parent_state(self):
        self.state = self.contrato_padre_id.state



   
""" def _compute_contract_count(self):
        contract_data = self.env['fleet.vehicle.log.contract'].read_group(
            [('vehicle_id', 'in', self.ids), ('state', '!=', 'closed')],
            ['vehicle_id'],
            ['vehicle_id']
        )
        contract_count_dict = {data['vehicle_id'][0]: data['vehicle_id_count'] for data in contract_data}
        for vehicle in self:
            vehicle.contract_count = contract_count_dict.get(vehicle.id, 0) """