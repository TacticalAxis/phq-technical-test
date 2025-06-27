# main.py
import os
import securescaffold
from flask import render_template, send_from_directory

app = securescaffold.create_app(__name__)

@app.route("/")
def root():
    return render_template(
        "index.html", some_injected_value="piv_test", authenticated=False
    )


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    # This is used when running locally only.
    app.run(host="127.0.0.1", port=8080, debug=True)
