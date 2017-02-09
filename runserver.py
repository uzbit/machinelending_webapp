from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from webapp import app as frontend
from lcApi import app as lcApi
from flask_wtf.csrf import CsrfProtect

CsrfProtect(frontend)

app = DispatcherMiddleware(frontend, {
	'/lcApi': lcApi
})
