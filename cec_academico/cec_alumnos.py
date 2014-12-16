# -*- coding: utf-8 -*-
# #############################################################################
#
# OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import openerp
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
import openerp.addons.decimal_precision as dp
import openerp.tools.image as imageoerp
import xml.etree.ElementTree as ET
from urllib2 import URLError
import re


class cec_alumnos(osv.osv):
    _name = "cec.alumnos"
    _inherits = {'res.partner':'partner_id'}
    _columns = {
        "senescyt": fields.char("Registro SENESCYT", help="En caso de tener títulos registrados ingrese el número de registro"),
        "work_institution": fields.char("Institución de trabajo", size=255),
        "charge": fields.char("Cargo", size=200),
        "work_email": fields.char("E-mail de trabajo", size=255),
        "work_city": fields.many2one("canton", "Ciudad de Trabajo"),
        "work_address": fields.char("Dirección del trabajo", size=255),
        "partner_id": fields.many2one('res.partner', 'partner', required=True, ondelete="cascade"),
        "is_alumn": fields.boolean("Es alumno?"),
    }
    _defaults = {
        "is_alumn": True
    }
    
    def create(self, cr, uid, vals, context=None):
        res = {}
        res_id = super(cec_alumnos, self).create(cr, uid, vals, context=context)
        cecalumnos_obj = self.browse(cr,uid,res_id)
        res = {'active' : True,
               'login' : vals['email'],
               'password' : vals['identification_number'],
               #'company_id' : vals['company'],
               'partner_id' : cecalumnos_obj.partner_id.id,
           }
        usr_id = self.pool.get('res.users').create(cr, uid, res)

        return cecalumnos_obj.id
    def city_change(self, cr, uid, ids, city, context=None):
        value = {}
        value['residence_city_id'] = city
        if city:
            city_obj = self.pool.get('canton').browse(cr, uid, city)
            if city_obj:
                value['state_id'] = city_obj.country_state_id.id
                value['country_id'] = city_obj.country_state_id.country_id.id
        return {'value': value}
