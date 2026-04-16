from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class TopologyController(object):

    def __init__(self):
        core.openflow.addListeners(self)
        log.info("Controller initialized")

    def _handle_ConnectionUp(self, event):
        log.info("Switch %s connected", event.dpid)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        log.info("Packet received on port %s", in_port)

        # Flood packet
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)

        # Install flow rule
        match = of.ofp_match.from_packet(packet, in_port)

        flow_mod = of.ofp_flow_mod()
        flow_mod.match = match
        flow_mod.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        flow_mod.priority = 10

        event.connection.send(flow_mod)

    def _handle_PortStatus(self, event):
        log.info("TOPOLOGY CHANGE DETECTED on switch %s", event.dpid)

def launch():
    core.registerNew(TopologyController)
