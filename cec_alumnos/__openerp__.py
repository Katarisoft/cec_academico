# -*- coding: utf-8 -*-
##############################################################################
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
#  AUTOR  = Paul Ochoa

{
    'name' : 'CEC Alumnos',
    'version' : '1.0',
    'author' : 'CEC EP',
    'category' : 'Registro alumnos',
    'description' : """
    Registro de estudiantes par cursos del CEC
    """,
    'website': 'http://www.cecep-iaen.edu.ec',
    'data': [
        'views/cec_alumnos_views.xml',
        'views/cec_alumnos_actions.xml',
        'views/cec_alumnos_menus.xml',
	],
    'update_xml': [
        #'security/ir.model.access.csv',
    ],
    'depends': [
        'cec_base',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
