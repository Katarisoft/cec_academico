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


class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {

        "senescyt": fields.char("Registro SENESCYT",
                                help="En caso de tener títulos registrados ingrese el número de registro"),
        "work_institution": fields.char("Institución de trabajo", size=255),
        "charge": fields.char("Cargo", size=200),
        "work_email": fields.char("E-mail de trabajo", size=255),
        "work_city": fields.many2one("canton", "Ciudad de Trabajo"),
        "work_address": fields.char("Dirección del trabajo", size=255),
        "is_alumn": fields.boolean("Es alumno?"),


    }
    _defaults = {
        "is_alumn": True
    }