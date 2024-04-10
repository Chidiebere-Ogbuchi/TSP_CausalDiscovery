#!/usr/bin/python

import time
import os
import shutil

from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, error, setLogLevel
import threading

setLogLevel('info')


network = Containernet(controller=Controller)

cwd = os.getcwd()

info('*** Adding controller\n')
network.addController('c0')

info('*** Adding docker containers\n')


# Specify the directory paths
results_dir = os.path.join(cwd, "results")
date_dir = os.path.join(cwd, "date")

# Check if the directories exist before attempting to remove them
if os.path.exists(results_dir):
    shutil.rmtree(results_dir)
    print(f"Directory '{results_dir}' removed successfully.")
else:
    print(f"Directory '{results_dir}' does not exist.")


# Create folders
create_folder = ["entrance", "hall1", "hall2", "hall3", "shop", "rest", "edge", "metaverse"]

for folder in create_folder:
    if not os.path.exists(cwd + "/results/" + folder):
        os.makedirs(cwd + "/results/" + folder)

print("Results directory created successfully.")


### Replace
Weekday = "Sunday"
Week = "02"

day = Weekday + "_" + Week



bdwidth = 3.0


##-------Broker-------

brokerDocker = network.addDocker(
	'broker',
	ip='10.0.0.240',
	dimage='emqx-experiments:latest',		
	dcmd="/opt/emqx/bin/emqx foreground",
	ports=[1883, 18083, 8883, 8083, 8084, 8780, 9900],
	port_bindings={1883: 1883, 18083: 18083, 8883: 8883, 8083: 8083, 8084: 8084, 8780: 8780, 9900:9900}
)

entranceDocker = network.addDocker(
	'entrance',
	ip='10.0.0.241',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/entrance:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900}
)

hall1Docker = network.addDocker(
	'hall1',
	ip='10.0.0.242',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/hall1:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900}
)

hall2Docker = network.addDocker(
	'hall2',
	ip='10.0.0.243',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/hall2:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900}
)

hall3Docker = network.addDocker(
	'hall3',
	ip='10.0.0.244',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/hall3:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900}
)

shopDocker = network.addDocker(
	'shop',
	ip='10.0.0.245',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/shop:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900}
)

restDocker = network.addDocker(
	'rest',
	ip='10.0.0.246',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/rest:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900}
)

edgeDocker = network.addDocker(
	'edge',
	ip='10.0.0.247',
	dimage="location:latest",
	ports=[1883, 9900],	
	volumes=[cwd + "/deployments/edge:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],			
	ports_binding={1883: 1883, 9900:9900}
)

metaverseDocker = network.addDocker(
	'metaverse',
	ip='10.0.0.248',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/metaverse:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900}
)

info('*** Adding switches\n')
edgeSwitch = network.addSwitch('s7')
metaverseSwitch = network.addSwitch('s8')
brokerSwitch = network.addSwitch('s9')

info('*** Creating links\n')
##Connecting hosts to switches
network.addLink(edgeDocker, edgeSwitch)
network.addLink(metaverseDocker, metaverseSwitch)
network.addLink(brokerDocker, brokerSwitch)



network.addLink(brokerDocker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(entranceDocker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall1Docker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall2Docker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall3Docker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(shopDocker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(restDocker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(edgeSwitch, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(metaverseSwitch, brokerSwitch, cls=TCLink, bw=bdwidth)


##Connecting switches to edge switch
# network.addLink(entranceDocker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(hall1Docker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(hall2Docker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(hall3Docker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(shopDocker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(restDocker, edgeSwitch, cls=TCLink, bw=2.0)


##Connecting switches to metaverse switch

network.addLink(entranceDocker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall1Docker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall2Docker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall3Docker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(shopDocker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(restDocker, metaverseSwitch, cls=TCLink, bw=bdwidth)


info('*** Starting network\n')
network.start()

info('*** Testing connectivity\n')
network.pingAll([])

info('*** Setting up experiment \n')

time.sleep(2)

info('\n*** Launching "entrance" Docker... \n')
entranceDocker.cmd('java -jar location.jar entrance&')

info('\n*** Launching "hall-1" Docker... \n')
hall1Docker.cmd('java -jar location.jar hall1 &')

info('\n*** Launching "hall-2" Docker... \n')
hall2Docker.cmd('java -jar location.jar hall2 &')

info('\n*** Launching "hall-3" Docker... \n')
hall3Docker.cmd('java -jar location.jar hall3 &')

info('\n*** Launching "shop" Docker... \n')
shopDocker.cmd('java -jar location.jar shop &')

info('\n*** Launching "rest" Docker... \n')
restDocker.cmd('java -jar location.jar rest &')

info('\n*** Launching "edge" Docker... \n')
edgeDocker.cmd('java -jar location.jar edge &')

info('\n*** Launching "metaverse" Docker... \n')
metaverseDocker.cmd('java -jar location.jar metaverse&')

info('\n*** Starting network \n')
info('*** Running CLI\n')
CLI(network)


day_dir = os.path.join(date_dir, day)

# Move the directory to the new path
# save_path = os.path.join(cwd, "date", day)
new_path = os.path.join(cwd, "results", day)
shutil.move(day_dir, new_path)

print(f"Directory moved successfully from {day_dir} to {new_path}")



# Construct the archive name without adding a "/" at the beginning
archive_name = day + "_" + str(bdwidth)

# After the process, zip the created directories
shutil.make_archive(os.path.join(cwd, archive_name), 'zip', os.path.join(cwd, "results"))


# # time.sleep(60)
info('*** Stopping network')
network.stop()

