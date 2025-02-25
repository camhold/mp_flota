# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'MP_Flotas',
    'version' : '0.1',
    'sequence': 185,
    'category': 'Human Resources/Fleet',
    'website' : 'https://www.odoo.com/app/fleet',
    'summary' : 'Manage your fleet and track car costs',
    'description' : """
Vehicle, leasing, insurances, cost
==================================
With this module, Odoo helps you managing all your vehicles, the
contracts associated to those vehicle as well as services, costs
and many other features necessary to the management of your fleet
of vehicle(s)

Main Features
-------------
* Add vehicles to your fleet
* Manage contracts for vehicles
* Reminder when a contract reach its expiration date
* Add services, odometer values for all vehicles
* Show all costs associated to a vehicle or to a type of service
* Analysis graph for costs
""",
    'depends': [
        'fleet',
        'base',
    ],
    'data': [
    'security/ir.model.access.csv',
    'views/flota_view.xml',
    'views/vehicle_view.xml',
    'data/gps_brand_data.xml',
    'data/gps_model_data.xml'
    #'views/configuracion_view.xml',
    #'views/reportes_view.xml',
    ],

    #'demo': ['data/fleet_demo.xml'],


    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'fleet/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
}
