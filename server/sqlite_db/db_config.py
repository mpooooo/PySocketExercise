import ConfigParser
import os

def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/db.conf'
    config.read(path)
    return config.get(section, key)

if __name__ == '__main__':
	print getConfig("user_db", "db_path")