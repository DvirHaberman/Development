from model import *
import importlib

module = importlib.import_module('my_mod')
req_class = getattr(module,'my_class')
req_class.print_nums(1,2)

OctopusUtils.get_all_functions()