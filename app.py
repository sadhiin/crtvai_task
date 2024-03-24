import boto3
import json
from flask import Flask, render_template, request, redirect, url_for
from src.utility.local_loger import logger
app = Flask(__name__)

@app.route("/")
def upload_file():
    return render_template('home.html')


if __name__=="__main__":
    logger.info("Application running.")
    app.run(debug=True)