# -*- coding: utf-8 -*-
# #############################################################################
#
#    OpenERP, Open Source Management Solution
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


class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
    "identification_type_id": fields.many2one("identification.type", u"Tipo de Identificación", required=True),
    "identification_number": fields.char(u"Nro.", size=13, required=True,
                                         help="Cedula de Identidad, Pasaporte, CCI, DNI"),
    "gender_id": fields.many2one("gender", "Género", required=True),
    "residence_city_id": fields.many2one("canton", "Ciudad de Residencia", required=False),
    "state_id": fields.many2one("res.country.state", "Estado/Provincia", required=False),
    "nationality_id": fields.many2one("nationality", "Nacionalidad", required=True),
    "Street2": fields.char(required=False),
    "location_reference": fields.text("Referencia de Ubicación"),
    "senescyt": fields.char("Registro SENESCYT",
                            help="En caso de tener títulos registrados ingrese el número de registro"),
    "work_institution": fields.char("Institución de trabajo", size=255),
    "charge": fields.char("Cargo", size=200),
    "work_email": fields.char("E-mail de trabajo", size=255),
    "work_city": fields.many2one("canton", "Ciudad de Trabajo"),
    "work_address": fields.char("Dirección del trabajo", size=255),
    "disability": fields.boolean("Discapacidad"),
    "disability_id": fields.many2one("type.disability", "Tipo de Discapacidad"),
    "conadis_number": fields.char("N° Carnet del CONADIS", size=10, require=True),

    "is_alumn": fields.boolean("Es alumno?"),

    }

    #        _defaults = {
    #                "is_alumn" : True
    #        }
    _sql_constraints = [('identification_number_unique', 'unique(identification_number)',
                         _(u'Ya existe un registro con ese número de identificación.'))]

    def on_name(self, cr, uid, ids, name):
        if name:
            print "%s_PA.pdf" % (name)
            return {'value': {'proposal_file_name': "%s_PA.pdf" % (name.upper())}}
        else:
            return {'value': {}}

    def on_city(self, cr, uid, ids, city):
        if city:
            values = {}
            url = 'http://api.geonames.org/search?q=machala&maxRows=10&style=LONG&lang=es&username=_mfierro'
            response = urllib2.urlopen(url).read()

            root = ET.fromstring(response)
            for child in root:
                if child.tag == 'geoname' and child[5].text == 'EC':
                    return child[6].text

    def on_indi(self, cr, uid, ids, id_etnia):
        if id_etnia:
            obj = self.pool.get('ethnic.group').browse(cr, uid, id_etnia)
            if obj.name.lower().find(u'indígena') >= 0:
                return {'value': {'use_indi': 'i'}}
            else:
                return {'value': {'use_indi': 'o', 'india_id': ''}}

    def only_numbers(self, cr, uid, ids):
        """ Valida que una cadena contenga únicamente dígitos. """
        for record in self.browse(cr, uid, ids):
            if not re.match("^[0-9]+$", record.phone) or not re.match("^[0-9]+$", record.mobile): return False
        return True

    def get_ids(self, cr, uid, ids, model, name):
        domain = [('name', 'ilike', name)]
        obj = self.pool.get(model).search(cr, uid, domain)
        #pdb.set_trace()

        try:
            return obj[0]
        except IndexError:
            return None



    #_constraints = [(only_numbers, u'Los números telefónicos deben contener únicamente dígitos.', ['phone','mobile'])]
