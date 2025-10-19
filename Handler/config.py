import configparser
conf = configparser.ConfigParser()
conf.read('config.conf')
config = {}
for section in conf:
    for variable in conf[section]:
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

def set_chat(id):
    strs = open("config.conf").read().split("\n")
    with open("config.conf", "w") as file:
        for st in strs:
            if(st.startswith("your_chat")):
                file.write("your_chat = " + str(id))
            else:
                file.write(st + "\n")