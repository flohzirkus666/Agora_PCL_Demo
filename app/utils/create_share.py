from netapp_ontap import HostConnection
from netapp_ontap.error import NetAppRestError
from netapp_ontap.resources import CifsShare, Volume

from .connection_handler import ConnectionHandler
from .create_snapmirror import create_snapmirror

# Hardcoded connection for LoD usage
connections = ConnectionHandler(
    source=HostConnection(
        host="cluster1.demo.netapp.com",
        username="admin",
        password="Netapp1!",
        verify=False,
    ),
    destination=HostConnection(
        host="cluster2.demo.netapp.com",
        username="admin",
        password="Netapp1!",
        verify=False,
    ),
)


def create_cifs_share(
    share_name: str,
    size: str,
    permissions: str,
    mirror: bool,
) -> bool:
    """A simple example for implementing a share creation."""
    # first step: creating a volume
    new_vol = Volume(
        name=f"{share_name}_vol",
        svm={"name": "svm1"},
        size=size,
        nas={"path": f"/{share_name}".lower()},
        aggregates=[{"name": "cluster1_01_aggr1"}],
    )
    # second step will be creating a share
    new_share = CifsShare()
    # we are setting here share acls according to our order
    new_share.acls = [
        {"permission": "full_control", "user_or_group": permissions, "type": "windows"}
    ]
    new_share.svm = {"name": "svm1"}
    new_share.path = f"/{share_name}".lower()
    new_share.name = share_name
    with connections.source:
        try:
            # volume creation should be a blocking event
            new_vol.post(hydrate=True, poll=True)
            new_share.post(hydrate=True)
            # for showing off
            print(new_vol, new_share)
            # if creating was successul, return true
        except NetAppRestError:
            return False

    # snapmirror part
    share_status = True
    if mirror:
        share_status = create_snapmirror(
            connection=connections.destination, volume_name=share_name
        )
    return share_status
