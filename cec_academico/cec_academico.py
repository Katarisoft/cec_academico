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
import re
import datetime
import pdb
#from validation import validation

# Creación inicia de cursos de capacitacióy y educación continua


class course(osv.osv):
    _name = "course"
    _description = u"Creación de los cursos de educación continua"

    def compare(self, cr, uid, ids, ds, df, error=0, context=None):
        if ds > df:
            if error == '1':
                raise osv.except_osv(_('ERROR!'),
                                     _('La fecha de inicio de curso no puede ser menor a la de inscripción'))
            elif error == 'm':
                raise osv.except_osv(_('ERROR!'), _('La calificación máxima debe ser mayor a la mínima'))
            elif error == 's':
                raise osv.except_osv(_('ERROR!'), _('EL número máximo de estudiantes debe ser mayor a la mínima'))
            raise osv.except_osv(_('ERROR!'), _('La fecha de fin debe ser mayor a la de inicio'))
        return True

    def carga_unidades(self, cr, uid, ids, context=None):
        print ids
        query = "delete from course_docentes where course_id = %s" % (str(ids[0]))
        cr.execute(query)
        course_obj = self.browse(cr, uid, ids)
        print course_obj
        print course_obj.learning_unit_id
        for unit in course_obj.learning_unit_id:
            unit_ids = self.pool.get('learning.unit').search(cr, uid, [('superior', '=', unit.id)])
            unit_obj = self.pool.get('learning.unit').browse(cr, uid, unit_ids)
            print unit_obj
            for unit in unit_obj:
                self.pool.get('course.docentes').create(cr, uid, {'name': unit.name, 'course_id': ids[0],
                                                                  'learning_unit_id': unit.id})
        return True

    def _is_active(self, cr, uid, ids, fields, arg, context=None):
        res = dict()
        for course in self.browse(cr, uid, ids, context=context):
            if datetime.datetime.strptime(course.finish_date, '%Y-%m-%d') > datetime.datetime.now():
                res[course.id] = True
            else:
                res[course.id] = False
        return res

    def _is_open(self, cr, uid, ids, fields, arg, context=None):
        res = dict()
        for course in self.browse(cr, uid, ids, context=context):
            if (datetime.datetime.strptime(course.start_date_inscription, '%Y-%m-%d') <= datetime.datetime.now()) and (
                        datetime.datetime.strptime(course.finish_date_inscription,
                                                   '%Y-%m-%d') >= datetime.datetime.now()):
                res[course.id] = True
            else:
                res[course.id] = False
        return res

    _columns = {
        "name": fields.char("Nombre del Curso", size=255),
        "project": fields.char("Proyecto", size=255),
        "start_date": fields.date("Fecha inicio clase"),
        "finish_date": fields.date("Fecha final clase"),
        "start_date_inscription": fields.date("Fecha inicio Inscripción"),
        "finish_date_inscription": fields.date("Fecha final Inscripción"),
        "min_students": fields.integer("Num. minimo de estudiantes"),
        "max_students": fields.integer("Num. maximo de estudiantes"),
        "min_mark": fields.integer("Calificacion minima del curso", size=3),
        "max_mark": fields.integer("Calificacion maxima del curso", size=3),
        "assistance": fields.char("Asistencia minima para el curso", size=3),
        "learning_unit_id": fields.many2many("learning.unit", "course_unit_rel", "course_id", "unit_id", "Módulos"),
        "active": fields.function(_is_active, type="boolean", store=True, string="Activo"),
        "open": fields.function(_is_open, type="boolean", store=True, string="abierto"),
        "course_docentes_ids": fields.one2many('course.docentes', 'course_id', 'Unidades de Aprendisajes',
                                               delete='cascade', ),
    }


class learning_unit(osv.osv):
    _name = "learning.unit"
    _order = "superior, module"
    _description = u"Creación de modulos y unidades de aprendisaje para un curso"
    _columns = {
        "name": fields.char("Nombre", size=255),
        "module": fields.boolean("Es Módulo?"),
        "superior": fields.many2one("learning.unit", "Padre", "Módulo", group_operator="avg"),
        #"teaching": fields.many2one("res_parther", "name"),
    }


class course_docentes(osv.osv):
    _name = "course.docentes"
    _inherit = "learning.unit"
    _description = u"Creación de modulos y unidades de aprendisaje para un curso"
    _columns = {
        "learning_unit_id": fields.many2one('learning.unit', 'Materia'),
        "teacher": fields.many2one("res.partner", "Docente"),
        "course_id": fields.many2one("course", 'Curso', required=True),

    }


class course_student(osv.osv):
    _name = "course.student"
    _description = ""

    def _mark(self, cr, uid, ids, fields, arg, context=None):
        res = dict()
        for cs in self.browse(cr, uid, ids):
            suma = 0
            i = 0
            for notas in cs.course_student_mark_ids:
                suma += notas.mark
                i = i + 1
            if suma:
                res[cs.id] = suma / i
            else:
                res[cs.id] = 0
        return res

    def _assistance(self, cr, uid, ids, fields, arg, context=None):
        res = dict()
        for cs in self.browse(cr, uid, ids):
            suma = 0
            for asistencia in cs.course_student_mark_ids:
                suma += asistencia.assistance
            res[cs.id] = suma
        return res

    def _aprobate(self, cr, uid, ids, fields, arg, context=None):
        res = dict()
        for cs in self.browse(cr, uid, ids):
            if (cs.mark >= cs.course_id.min_mark) and (cs.assistance >= int(cs.course_id.assistance)):
                res[cs.id] = True
            else:
                res[cs.id] = False
        return res

    def _get_mark_ids(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        print ids
        for mark in self.browse(cr, uid, ids, context=context):
            print mark
            partner_obj = self.pool.get('res.users').browse(cr, uid, uid)
            res[mark.id] = self.pool.get('course.student.mark').search(cr, uid,
                                                                       [('partner_id', '=', partner_obj.partner_id.id),
                                                                        ('course_student_id', '=', mark.id)])
        print res
        return res

    _columns = {
        'partner_id': fields.many2one('cec.alumnos', 'Alumno'),
        'course_id': fields.many2one('course', 'Curso'),
        'mark': fields.function(_mark, type="integer", store=True, string='Promedio General', size=3),
        'assistance': fields.function(_assistance, type='integer', store=True, string='Asistencia', size=3),
        'approbate': fields.function(_aprobate, type='boolean', store=True, string='Aprobado?', ),
        'course_student_mark_ids': fields.one2many('course.student.mark', 'course_student_id', 'Notas x materi', ),
        #'course_student_mark_ids' : fields.function(_get_mark_ids, type="one2many", method=True,relation='course.student.mark',string='Notas x materia'),
    }

    _sql_constraints = [
        ('course_id_unique_student', 'unique (partner_id,course_id)', 'El estudiante ya está inscrito en este curso !')
    ]


class course_student_mark(osv.osv):
    _name = "course.student.mark"
    _description = ""
    _columns = {
        'course_student_id': fields.many2one('course.student', "Curso x estudiante"),
        'learning_unit_id': fields.many2one('learning.unit', "Materia"),
        'mark': fields.integer("Nota", size=3),
        'assistance': fields.integer('Asistencia', size=3),
        'partner_id': fields.many2one('res.partner', 'Profesor'),
    }


class course_student_inscription(osv.osv_memory):
    _name = "course.student.inscription"

    def inscribir(self, cr, uid, ids, context=None):
        inscription_obj = self.browse(cr, uid, ids)
        res = {}
        for inscription in inscription_obj:
            course_student_ids = self.pool.get('course.student').search(cr, uid,
                                                                        [('course_id', '=', inscription.course_id.id)])
            if course_student_ids:
                if len(course_student_ids) == inscription.course_id.max_students:
                    raise osv.except_osv(_('ADVERTENCIA!'), _('El cupo maximo del curso %s se ha completado') % (
                        inscription.course_id.name))

            res = {'partner_id': inscription.partner_id.id, 'course_id': inscription.course_id.id, }
            course_student_id = self.pool.get('course.student').create(cr, uid, res)
            res = {}
            #pdb.set_trace()
            if not inscription.course_id.course_docentes_ids:
                self.pool.get('course').carga_unidades(cr, uid, [inscription.course_id.id])
            for course in inscription.course_id.course_docentes_ids:
                res = {'course_student_id': course_student_id, 'learning_unit_id': course.learning_unit_id.id,
                       'partner_id': course.teacher.id}
                self.pool.get('course.student.mark').create(cr, uid, res)

        return True


    _columns = {
        'partner_id': fields.many2one('cec.alumnos', string='Alumno'),
        'course_id': fields.many2one('course', 'Curso'),
    }
