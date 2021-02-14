from . import api2, g, session, request

@api2.before_request
def before_request():
    g.project_id = None
    g.username = None
    
    if request.json is not None:
        if 'project_id' in request.json:
            g.project_id = request.json['project_id']
        if 'username' in request.json:
            g.username = request.json['username']

    if "session" in locals():
        if 'project_id' in session:
            g.project_id = session['current_project_id']
        if 'username' in session:
            g.username = session['username']
    
    if (g.username is None) or (g.project_id is None):
        # return {message:"Cannot determine user name or project id"}, 412
        session['username'] = 'dvirh'
        session['current_project_id'] = 1
        g.project_id = session['current_project_id']
        g.username = session['username']
