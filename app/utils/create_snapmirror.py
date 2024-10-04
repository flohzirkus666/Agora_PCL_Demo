from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapmirrorRelationship
from netapp_ontap.error import NetAppRestError


def create_snapmirror(connection: HostConnection, volume_name: str) -> bool:
    """Creating a SnapMirror relationship"""

    params = {
        "source": {"path": f"cluster1://svm1/{volume_name}_vol"},
        "destination": {"path": f"cluster2://svm1_dr/{volume_name}_dr"},
        "state": "snapmirrored",
        "create_destination": {"enabled": True},
    }
    snapmirror = SnapmirrorRelationship.from_dict(params)
    with connection:
        try:
            snapmirror.post(hydrate=True)
            print(snapmirror)
            return True
        except NetAppRestError as err:
            print(err)
            return False
