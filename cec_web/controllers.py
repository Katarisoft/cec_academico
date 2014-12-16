from openerp import http
from openerp.http import request, STATIC_CACHE

class notas(http.Controller):
    @http.route('/notas/', auth='user',website=True )
    def index(self):
        print request.uid
        users = request.registry['res.partner'].browse(request.cr,request.uid,[request.uid])
        print users
        Teachers = http.request.env['course']
        print  Teachers.search([])
        return http.request.render('cec_web.index', {'teachers': Teachers.search([])})
        
    @http.route('/notas/<int:id>/', auth='public', website=True)
    def teacher(self, id):
        #return '<h1>{}</h1>'.format(name)
        return '<h1>{} ({})</h1>'.format(id, type(id).__name__)

    @http.route('/notas/<model("course"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('cec_web.biography', {
            'person': teacher
        })
