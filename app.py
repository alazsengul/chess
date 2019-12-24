from flask import Flask, render_template, redirect, url_for, request

# initialization

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    response.cache_control.max_age = 604800
    return(response)

# FUNCTIONS

# MAIN PAGE

@app.route('/')
def index():
    return(render_template('index.html'))

###

if __name__ == '__main__':
    app.run(debug=True)
