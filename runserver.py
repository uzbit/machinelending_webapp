from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from webapp import app as frontend
from lcApi import app as lcApi


app = DispatcherMiddleware(frontend, {
	'/lcApi': lcApi
})

run_simple('localhost', 5000, app, use_reloader=True)
