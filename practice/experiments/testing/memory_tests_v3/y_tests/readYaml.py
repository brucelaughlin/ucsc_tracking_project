import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


#stream = open("data.yml",'r')
stream = open("run_config_test.yml",'r')
nary = yaml.safe_load(stream)
#nary = yaml.load(stream)
for key, value in nary.items():
    print (key + " : " + str(value)) 
