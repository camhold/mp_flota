from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import calendar
import random
import time
from datetime import datetime, timedelta

class GpsModel(models.Model):
    _name="gps.model"

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', _('El nombre del modelo de GPS debe ser único.')),
    ]

    #Añadir validaciones