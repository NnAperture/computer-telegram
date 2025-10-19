import configparser
conf = configparser.ConfigParser()
conf.read('config.conf')
config = {}
for section in conf:
    for variable in conf[section]:
        print(section, variable)
        value = conf[section][variable]
        if(value == "true"):
            config.setdefault(section, {})[variable] = True
        elif(value == "false"):
            config.setdefault(section, {})[variable] = False
        else:
            try:
                config.setdefault(section, {})[variable] = int(value)
            except:
                config.setdefault(section, {})[variable] = value
