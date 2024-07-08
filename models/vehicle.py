from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
        
class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    is_in_use_by_contract = fields.Boolean(
        string='In Use by Contract',
        compute='_compute_is_in_use_by_contract',
        store=True  
    )

    #Nuevos campos en base a requerimientos
    #fecha_recepcion
    #fecha_expiracion

    reception_date = fields.Date(
        'Fecha recepción de vehículo', default=fields.Date.context_today,
        help='Fecha en que vehículo fue recepcionado',
        required=True)
    expiration_date = fields.Date(
        'Fecha expiración de vehículo', 
        help='Fecha en que expira vehículo',
        default=lambda self:
        self.compute_next_month_date(fields.Date.context_today(self)),
        required=True)
    #imei
    imei = fields.Char("IMEI",  store=True, readonly=False,required=True)
    #n_telefono
    phone_number = fields.Char("Número de telefono",  store=True, readonly=False,required=True)
    #modelo_gps
    gps_model = fields.Many2one('gps.model', string='Modelo GPS',required=True)

    #marca_gps
    gps_brand = fields.Many2one('gps.brand', string='Marca GPS',required=True)
    #

    #Solo para numeros chile
    def validate_phone_number(self, number):
        if len(number) == 12 and number[0]=="+" and number[1:].isdigit():
            number = number
            return True
        if len(number) == 9 and number.isdigit():
            number = "+56" + number
            return True
        if (len(number) == 11 and number.startswith('56') and number.isdigit()):
            number = "+" + number
            return True
        else:
            return False
        
    #Solo para numeros chile
    def format_phone_number(self):
         for record in self:
            number = record.phone_number
            
            if len(number) == 12 and number[0]=="+" and number[1:].isdigit():
                return number
            if len(number) == 9 and number.isdigit():
                record.phone_number = "+56" + number
                return record.phone_number
            if (len(number) == 11 and number.startswith('56') and number.isdigit()):
                record.phone_number = "+" + number
                return record.phone_number
            else:
                return record.phone_number
        
    @api.constrains('phone_number')
    def _check_phone_number(self):
        for record in self:
            if not self.validate_phone_number(record.phone_number):
                raise ValidationError("Formato de número de teléfono no válido.")
            
            self.format_phone_number()
            
    contract_count = fields.Integer(compute="_compute_count_all", string='Contract Count',store=True)
            
    @api.depends('log_contracts', 'log_contracts.state', 'contract_state')
    def _compute_is_in_use_by_contract(self):
        LogContract = self.env['fleet.vehicle.log.contract']
        
        for record in self:
            record.contract_count = LogContract.search_count([('vehicle_id', '=', record.id), ('state', '!=', 'closed'), ('active', '=', record.active)])
            #print("CONTRACT COUNT", record.contract_count)
            record.is_in_use_by_contract = bool(record.contract_count)

    @api.model
    def create(self, values):
        existing_imei = self.search([('imei', '=', values.get('imei'))])
        if existing_imei:
            raise ValidationError("Valor de IMEI ya se encuentra en otro vehículo")
        existing_phone_number=self.search([('phone_number', '=', values.get('phone_number'))])
        if existing_phone_number:
            raise ValidationError("Número de teléfono ya se encuentra en otro vehículo.")

        return super(Vehicle, self).create(values)

    def write(self, values):
        if 'imei' in values:
            existing_imei = self.search([('imei', '=', values['imei']), ('id', '!=', self.id)])
            if existing_imei:
                raise ValidationError("Valor de IMEI ya se encuentra en otro vehículo")
        if 'phone_number' in values:
            existing_phone_number=self.search([('phone_number', '=', values['phone_number']),  ('id', '!=', self.id)])
            
            if existing_phone_number:
                raise ValidationError("Número de teléfono ya se encuentra en otro vehículo.")

        return super(Vehicle, self).write(values)
    


    ##constrains

    @api.constrains('reception_date', 'expiration_date')
    def _check_dates(self):
        for record in self:
            if record.expiration_date and record.reception_date and \
                    record.expiration_date < record.reception_date:
                
                ##Revisar si puede ser mismo dia expiracion
                raise ValidationError("La fecha de expiración debe ser posterior a la fecha de recepción.")
            
    @api.constrains('imei')
    def _check_imei(self):
        for record in self:
            if not record.imei.isnumeric():
                raise ValidationError("IMEI en formato inválido")

            if not self.is_valid_imei(int(record.imei)):
                raise ValidationError("IMEI no es válido")

            

    def is_valid_imei(self,n):

        def sumDig( n ):
            a = 0
            while n > 0:
                a = a + n % 10
                n = int(n / 10)
        
            return a
        s = str(n)
        l = len(s)
    
        if l != 15:
            return False
    
        d = 0
        sum = 0
        for i in range(15, 0, -1):
            d = (int)(n % 10)
            if i % 2 == 0:

                d = 2 * d
            sum = sum + sumDig(d)
            n = n / 10
        return (sum % 10 == 0)
    
    def compute_next_year_date(self, strdate):
        oneyear = relativedelta(years=1)
        start_date = fields.Date.from_string(strdate)
        return fields.Date.to_string(start_date + oneyear)
    
    def compute_next_month_date(self, strdate):
        onemonth = relativedelta(months=1)
        start_date = fields.Date.from_string(strdate)
        return fields.Date.to_string(start_date + onemonth)


#16-01 Vista vehiculo añadir pestaña, otros datos
            #fecha recepcion
            #fecha expiracion
            #imei gps
            #numero telefono
            #modelo gps
            #marca