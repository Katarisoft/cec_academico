# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import logging
import werkzeug

import openerp
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.web.controllers.main import ensure_db
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, ustr

_logger = logging.getLogger(__name__)

class AuthSignupHome(openerp.addons.web.controllers.main.Home):
    
    @http.route('/web/teachers', type='http', auth='public', website=True)
    def web_auth_signup_teachers(self, *args, **kw):
        print "algo"

    def do_signup(self, qcontext):
        #raise SignupError(_('sa'))
        values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password'))
        assert any([k for k in values.values()]), "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."
        #self._signup_with_values(qcontext.get('token'), values)
        #request.cr.commit()

        if qcontext.get('token'):
            return super(AuthSignupHome, self).do_signup(qcontext)
        else:
            try:
                request.registry['cec.alumnos'].create(request.cr, openerp.SUPERUSER_ID,{'name' : values.get('name'), 'email' : values.get('login')}, {"password" : values.get('password')} )
                request.cr.commit()
            except Exception, e:
                raise SignupError(ustr(e))
                #raise SignupError(ustr(e)) 
        print request.cr.dbname
        uid = request.session.authenticate(request.cr.dbname, values.get('login'), values.get('password'))
        if not uid:
            raise SignupError(_('Authentification Failed.'))



# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
