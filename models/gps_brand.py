from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import calendar
import random
import time
from datetime import datetime, timedelta

class GpsBrand(models.Model):
    _name="gps.brand"

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', _('El nombre de la marca de GPS debe ser única.')),
    ]


    #Añadir validaciones