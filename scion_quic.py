#!/usr/bin/env python3

from seedemu.compiler import Docker, Graphviz
from seedemu.core import Emulator, Binding, Filter
from seedemu.layers import ScionBase, ScionRouting, ScionIsd, Scion, Ospf, Ibgp
from seedemu.layers.Scion import LinkType as ScLinkType
from seedemu.services import ScionSIGService



# Initialize
emu = Emulator()
base = ScionBase()
routing = ScionRouting()
scion_isd = ScionIsd()
scion = Scion()
ospf = Ospf()
sig = ScionSIGService()
ibgp = Ibgp()

# SCION ISDs
base.createIsolationDomain(1)

# Internet Exchange
base.createInternetExchange(100)



# AS-150
as150 = base.createAutonomousSystem(150)
scion_isd.addIsdAs(1, 150, is_core=False)
scion_isd.setCertIssuer((1, 150), issuer=152)
as150.createNetwork('net0')
as150_cs = as150.createControlService('cs1').joinNetwork('net0')
as150_router = as150.createRouter('br0')
as150_router.joinNetwork('net0').joinNetwork('ix100')

# AS-151
as151 = base.createAutonomousSystem(151)
scion_isd.addIsdAs(1, 151, is_core=False)
scion_isd.setCertIssuer((1, 151), issuer=152)
as151.createNetwork('net0')
as151.createControlService('cs1').joinNetwork('net0')
as151_router = as151.createRouter('br0').joinNetwork('net0').joinNetwork('ix100')

# AS-152
as152 = base.createAutonomousSystem(152)
scion_isd.addIsdAs(1, 152, is_core=True)
as152.createNetwork('net0')
as152.createControlService('cs1').joinNetwork('net0')
as152_router = as152.createRouter('br0').joinNetwork('net0').joinNetwork('ix100')

# SCION links
scion.addIxLink(100, (1, 150), (1, 152), ScLinkType.Transit)
scion.addIxLink(100, (1, 151), (1, 152), ScLinkType.Transit)

# Rendering
emu.addLayer(base)
emu.addLayer(routing)
emu.addLayer(scion_isd)
emu.addLayer(scion)
emu.addLayer(ospf)
emu.addLayer(sig)
emu.addLayer(ibgp)

emu.render()

# Compilation
emu.compile(Docker(internetMapEnabled=True, internetMapClientImage="bruol0/seedemu-client"), './output', override=True)
emu.compile(Graphviz(), './output/graphviz', override=True)