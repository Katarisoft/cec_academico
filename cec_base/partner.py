# -*- coding: utf-8 -*-
# #############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
import re


#DATOS DE USUARIO DEL SISTEMA
class res_partner(osv.osv):
    _inherit = "res.partner"
    #_inherits = {'res.partner':'partner_id'}
    _columns = {
        "identification_type_id": fields.many2one("identification.type", u"Tipo de Identificación", required=True),
        "identification_number": fields.char(u"Nro. Identificación", size=13, required=True,
                                             help="Cedula de Identidad, Pasaporte, CCI, DNI"),
        "gender_id": fields.many2one("gender", "Género", required=True),
        "residence_city_id": fields.many2one("canton", "Ciudad de Residencia", required=False),
        "state_id": fields.many2one("res.country.state", "Estado/Provincia", required=False),
        "nationality_id": fields.many2one("nationality", "Nacionalidad", required=True),
        "street2": fields.char("Calle Secundaria", required=False),
        "location_reference": fields.text("Referencia"),
        "disability": fields.boolean("Tipo discapacidad"),
        "disability_id": fields.many2one("type.disability", "Discapacidad"),
        "conadis_number": fields.char("Carnet CONADIS", size=10, require=True),
        "etnia": fields.many2one("ethnic.group", "Grupo etnico"),
    }
    _sql_constraints = [('identification_number_unique', 'unique(identification_number)',
                         _(u'Ya existe un registro con ese número de identificación.'))]

    def city_change(self, cr, uid, ids, city, context=None):
        value = {}
        value['residence_city_id'] = city
        if city:
            city_obj = self.pool.get('canton').browse(cr, uid, city)
            if city_obj:
                value['state_id'] = city_obj.country_state_id.id
                value['country_id'] = city_obj.country_state_id.country_id.id
        return {'value': value}

    def on_name(self, cr, uid, ids, name):
        if name:
            print "%s_PA.pdf" % (name)
            return {'value': {'proposal_file_name': "%s_PA.pdf" % (name.upper())}}
        else:
            return {'value': {}}
