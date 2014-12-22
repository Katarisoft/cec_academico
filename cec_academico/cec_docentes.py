# -*- coding: utf-8 -*-
# #############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
# This program is free software: you can redistribute it and/or modify
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
import random
from _validation import validation


class title_info(osv.osv):
    """ Clase para registrar los titulos de un docente."""
    _name = "title.info"
    _description = "Subir documentacion de Títulos Academicos"
    _columns = {
        'name': fields.char('Titulo', size=124),
        #'register': fields.char('Registro Senescyt', size=124),
        'register': fields.boolean('Registro Senescyt'),
        'date': fields.date('Fecha Registro'),
        'partner_id': fields.many2one('res.partner'),
        'title_file': fields.binary('Subir Documentacion del titulo'),
        'title_file_name': fields.char('title_file_name', size=124),
    }
    _defaults = {
        'title_file_name': 'titulo.pdf'
    }


class experience_info(osv.osv):
    """ Clase para registrar los experiences de un docente."""
    _name = "experience.info"
    _description = "Experiencia Docente"
    _columns = {
        'name': fields.char('Institucion', size=124),
        'finicio': fields.date('Fecha Inicio'),
        'ffin': fields.date('Fecha Fin'),
        'actual': fields.boolean('Actualidad'),
        'partner_id': fields.many2one('res.partner'),
        'file': fields.binary('Certificado de Experiencia Laboral'),
        'title_file_name': fields.char('title_file_name', size=124),

    }
    _defaults = {
        'title_file_name': 'titulo.pdf'
    }


class publication_info(osv.osv):
    """ Clase para registrar las publicaciones y obras de un docente."""
    _name = "publication.info"
    _description = "Publicaciones y Obras"
    _columns = {
        'name': fields.char('Publicacion', size=124),
        'date': fields.char('Año de publicacion', size=124),
        'description': fields.text('Resumen'),
        'partner_id': fields.many2one('res.partner'),
        'file': fields.binary('Subir certificado de la Publicacion'),
        'title_file_name': fields.char('title_file_name', size=124),

    }
    _defaults = {
        'title_file_name': 'titulo.pdf'
    }


class evaluation_info(osv.osv):
    """ Clase para registrar las evaluaciones de desempeño de un docente."""
    _name = "evaluation.info"
    _description = "Evaluaciones de Desempeño"
    _columns = {
        'name': fields.char('Evaluacion', size=124),
        'date': fields.date('Fecha', ),
        'partner_id': fields.many2one('res.partner'),
        'file': fields.binary(u'Subir Evaluacion de Desempeño'),
        'title_file_name': fields.char('title_file_name', size=124),

    }
    _defaults = {
        'title_file_name': 'titulo.pdf'
    }


class instruction_info(osv.osv):
    """ Clase para registrar las capacitaciones de un docente."""
    _name = "instruction.info"
    _description = "Capacitaciones"
    _columns = {
        'name': fields.char('Capacitacion', size=124),
        'institucion': fields.char('Institucion', size=124),
        'finicio': fields.date('Fecha Inicio'),
        'ffin': fields.date('Fecha Fin'),
        'time': fields.integer('Duracion'),
        'type': fields.selection([('capacitador', 'Capacitador'), ('participante', 'Participante')], 'Tipo'),
        'partner_id': fields.many2one('res.partner'),
        'file': fields.binary('Subir certificado de la Capacitacion'),
        'title_file_name': fields.char('title_file_name', size=124),
    }
    _defaults = {
        'title_file_name': 'titulo.pdf'
    }


class project_info(osv.osv):
    """ Clase para registrar los proyectos de un docente."""
    _name = "project.info"
    _description = "Proyectos"
    _columns = {
        'name': fields.char('Proyecto', size=124),
        'institucion': fields.char('Institucion', size=124),
        'finish': fields.boolean('Culminados'),
        'date': fields.date('Fecha Inicio'),
        'partner_id': fields.many2one('res.partner'),
        'file': fields.binary('Subir certificado del Proyecto de Investigacion'),
        'title_file_name': fields.char('title_file_name', size=124),

    }
    _defaults = {
        'title_file_name': 'titulo.pdf'
    }


class tutoring_info(osv.osv):
    """ Clase para registrar las tutorías de doctorado y maestría de  un docente."""
    _name = "tutoring.info"
    _description = "Títulos Académicos"
    _columns = {
        'name': fields.char('Tema tutoría', size=124),
        'institucion': fields.char('Institucion', size=124),
        'date': fields.date('Fecha', size=124),
        'description': fields.text('Resumen', ),
        'partner_id': fields.many2one('res.partner'),
        'file': fields.binary(u'Subir certificados de Tutorías'),
        'title_file_name': fields.char('title_file_name', size=124),

    }
    _defaults = {
        'title_file_name': 'titulo.pdf'
    }


class language_info(osv.osv):
    """ Clase para registrar los titulos de un docente."""
    _name = "language.info"
    _description = "Títulos Academicos"
    _columns = {
        'name': fields.char('Idioma', size=124),
        'lectura': fields.integer('Nivel Lectura'),
        'escritura': fields.integer('Nivel Escritura'),
        'habla': fields.integer('Nivel Habla'),
        'partner_id': fields.many2one('res.partner'),
        'file': fields.binary(u'Subir certificados de Títulos Academicos'),
        'title_file_name': fields.char('title_file_name', size=124),

    }
    _defaults = {
        'title_file_name': 'titulo.pdf'
    }


def random_password():
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choice(chars) for i in xrange(8))


class cec_docentes(osv.osv):
    _name = "cec.docentes"
    _inherits = {'res.partner': 'partner_id'}
    _columns = {
        "proposal_file_name": fields.char('proposal_file_name', size=124),
        "curriculum": fields.binary("Hoja de Vida", filters=["*.pdf", "*.PDF"]),
        "id_copy": fields.binary("Copia de Cedula o Pasaporte", filters="*.pdf, *.PDF",),
        "title_info_ids": fields.one2many("title.info", "partner_id", "Subir documentacion de Títulos Academicos",
                                          requiered=False),
        #"proposal_info_ids": fields.one1many("proposal.info", "partner_id", "Propuesta Académica", requiered=False),
        "experience_info_ids": fields.one2many("experience.info", "partner_id",
                                               "Subir documentacion de Experiencia Docente", requiered=False),
        "publication_info_ids": fields.one2many("publication.info", "partner_id",
                                                "Subir documetntacion de Publicaciones y Obras", requiered=False),
        "evaluation_info_ids": fields.one2many("evaluation.info", "partner_id",
                                               "Subir documentacion de Evaluaciones de Desempeño", requiered=False),
        "instruction_info_ids": fields.one2many("instruction.info", "partner_id",
                                                "Subir documentacion de Capacitaciones", requiered=False),
        "project_info_ids": fields.one2many("project.info", "partner_id",
                                            "Subir documentacion de Proyectos de Investigacion", requiered=False),
        "tutoring_info_ids": fields.one2many("tutoring.info", "partner_id",
                                             "Subir documentacion de Tutorías de Tesis y Maestrias", requiered=False),
        "language_info_ids": fields.one2many("language.info", "partner_id", "Subir documentacion de Lenguajes",
                                             requiered=False),
        "horario": fields.selection([("cualquier_dia", "Cualquier día"),
                                     ("entre_semana", "Entre semana"),
                                     ("fin_de_semana", "Fin de semana")],
                                    "Jornada de labores"),
        "tematica_id": fields.many2many('tematica.type', 'tematica_res_partner', 'partner_id', 'tematica_id',
                                        "Tematicas"),
        "partner_id": fields.many2one('res.partner', 'partner', required=True, ondelete="cascade"),
        #"is_teacher": fields.boolean("Es profesor?"),
    }

    #_defaults = {
    #    "is_teacher": True
    #}

    def create(self, cr, uid, vals, context=None):
        res = {}
        res_id = super(cec_docentes, self).create(cr, uid, vals, context=context)
        cecdocentes_obj = self.browse(cr, uid, res_id)
        if not 'password' in context:
            vals['password'] = random_password()
            print vals['password']
        else:
            vals['password'] = context['password']

        res = {'active': True,
               'login': vals['email'],
               'password': vals['password'],
               'partner_id': cecdocentes_obj.partner_id.id,
        }
        usr_id = self.pool.get('res.users').create(cr, uid, res)
        return cecdocentes_obj.id

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

        try:
            return obj[0]
        except IndexError:
            return None

    def city_change(self, cr, uid, ids, city, context=None):
        value = {}
        value['residence_city_id'] = city
        if city:
            city_obj = self.pool.get('canton').browse(cr, uid, city)
            if city_obj:
                value['state_id'] = city_obj.country_state_id.id
                value['country_id'] = city_obj.country_state_id.country_id.id
        return {'value': value}

        #_constraints = [(only_numbers, u'Los números telefónicos deben contener únicamente dígitos.', ['phone','mobile'])]
