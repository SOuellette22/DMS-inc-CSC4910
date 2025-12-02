from flask import Flask, render_template

from src.app import create_app

flask_app = create_app()

@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=49162, debug=True)