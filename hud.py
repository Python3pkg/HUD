#!/usr/bin/env python3
try:
	import homeassistant.remote as remote
except:
	print("Unable to import HomeAssistant! (try pip3 install homeassistant maybe?)")
	exit(1)
try:
	import pygame
	from pygame.locals import *
except:
	print("Unable to import pygame! (See the readme for installing pygame for python3)")
	exit(1)
try:
	from pgu import gui
except:
	print("Unable to import pgu.gui! (See the readme for installing pgu)")

import elements

import sys
import argparse
import configparser
import logging
p = argparse.ArgumentParser()

p.add_argument('-c','--config',help="config file to use",required=True,type=argparse.FileType('r'))
p.add_argument('-H','--homeassistant',default=None,help="The location of home-assistant")
p.add_argument('-p','--port',default=None,help="the port to use for home-assistant (default: 8123)",type=int)
p.add_argument('-k','--key',default=None,help="The api password to use (default: None)",type=str)
p.add_argument('-s','--ssl',help="Use ssl (default false)",default=False,action="store_true")
p.add_argument('-v','--verbose',help="Log output",default=False,action="store_true")
p.add_argument('-l','--logfile',help="Instead of logging to stdout, log to this file",default=None)
args = p.parse_args();

# Setup logger
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

if args.verbose:
	if not args.logfile:
		consoleHandler = logging.streamHander(sys.stdout)
		consoleHandler.setFormatter(logFormatter)
		rootLogger.addHandler(consoleHandler)
	else:
		fileHandler = logging.FileHandler(str(args.logfile))
		fileHandler.setFormatter(logFormatter)
		rootLogger.addHandler(fileHandler)

# Setup Home assistant config

config = configparser.ConfigParser()
config.read(args.config.name)
print(config.sections())
try:
	haconfig = {
		"host" : (args.homeassistant if args.homeassistant else config["HomeAssistant"]["Host"]),
		"port" : (args.port if args.port else config["HomeAssistant"]["Port"]),
		"ssl" : (args.ssl if args.ssl else config["HomeAssistant"]["SSL"]),
		"key": (args.key if args.key else config["HomeAssistant"]["Password"])
	}
except KeyError as e:
	print ("Cannot find section [{}] in config file '{}'!".format(str(e),str(args.config.name)))
	exit(1)

# Setup home assistant connection

hass = remote.API(haconfig['host'],haconfig['key'],haconfig['port'],haconfig['ssl'])
try:
	validation = remote.validate_api(hass)
	if str(validation) != "ok":
		raise Exception(validation)

except Exception as e:
	print ("hass connection verification failed: {}".format(str(validation)))
	exit(1)


# For now, only use our "Light" section

# try to get the state of the entity

app = gui.Desktop(theme=gui.Theme("./pgu.theme"))
app.connect(gui.QUIT,app.quit,None)

container=gui.Table(width=230)

for section in config.sections():
	if section != "HomeAssistant":
		c = gui.Table(width=320)
		c.tr()
		c.td(gui.Label(section))
		
		state = remote.get_state(hass,"group.{}".format(str(config[section]["group"])))
		if state == None:
			c.tr()
			c.td(gui.Label("Unable to find group.{}".format(str(config[section]["group"]))))
		else:
			entity_ids = state.attributes['entity_id']
			for entity_id in entity_ids:
				c.tr()
				entity = remote.get_state(hass,entity_id)
				# Changeable, lights are hmmMMmmm
				if (entity.domain == "light"):
					widget = gui.Table(width=320)
					widget.tr()
					widget.td(elements.Light(hass,entity,width=300,height=30))
					widget.td(elements.LightSwitch(hass,entity,width=20,height=30))
					
					c.td(widget)
				elif (entity.domain == "sensor"):
					widget = gui.Label("{} : {}".format(str(entity.name),str(entity.state)))
					c.td(widget)
		container.tr()
		container.td(c)

main = gui.Container(width=230,height=600)
header = gui.Label('Home Assistant',cls='h1')
header.style.background="#0088FF"
main.add(header,10,10)
main.add(container,0,40)
app.run(main)

