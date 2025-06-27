# main.py
import securescaffold
from flask import render_template

app = securescaffold.create_app(__name__)

@app.route("/")
def root():
  return render_template("index.html", some_injected_value="piv_test")

if __name__ == "__main__":
    # This is used when running locally only.
    app.run(host="127.0.0.1", port=8080, debug=True)
