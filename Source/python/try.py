from model import *
import importlib
import json
import sys

print (not r'C:\Git_Rep\Development\functions' in sys.path)
sys.path.append(r'C:\Git_Rep\Development\functions')
module = importlib.import_module('calc')
req_func = getattr(module,'plus_func')
print(req_func(1,2))
print (not r'C:\Git_Rep\Development\functions' in sys.path)
print(sys.path)

# OctopusUtils.get_all_functions()
# d = {a:5,b:7}
# print(json.loads(d))