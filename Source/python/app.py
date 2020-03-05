from flask import Flask, redirect, render_template, request
from model import *

app = Flask(__name__)
db.session()
