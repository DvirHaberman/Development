from model import *
import importlib
import json
import sys


basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir + r'/../Functions')
sys.path.append(basedir + r'/../Infras/Fetches')
sys.path.append(basedir + r'/../Infras/Utils')

sys.path.append(r'C:\Git_Rep\Development\functions')
module = importlib.import_module('calc')
req_func = getattr(module,'plus_func')
print(req_func(1,2))
print (not r'C:\Git_Rep\Development\functions' in sys.path)
print(sys.path)

# OctopusUtils.get_all_functions()
# d = {a:5,b:7}
# print(json.loads(d))