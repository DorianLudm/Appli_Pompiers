from .app import app

@app.route('/')
def home():
    return "<h1>Les Pompiers !</h1>"