""" ReadTOML """

settings = {}

with open("settings.toml") as fp:
    line = fp.readline().strip()
    while line:
        if "WIFI_SSID" in line:
            settings["WIFI_SSID"] = line[line.rfind(' "')+2:-1]
        if "WIFI_PASSWORD" in line:
            settings["WIFI_PASSWORD"] = line[line.rfind(' "')+2:-1]
            
        line = fp.readline().strip()

