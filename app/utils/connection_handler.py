from dataclasses import dataclass

from netapp_ontap import HostConnection


@dataclass
class ConnectionHandler:
    """Handles our connections between multiple clusters"""

    source: HostConnection
    destination: HostConnection
