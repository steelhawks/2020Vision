try:
    import ujson as json
except ImportError:
    import json

from networktables import NetworkTables

__all__ = ["NTSerial"]


class NTSerial(object):
    """
    A utility class for synchronizing NetworkTables over a serial connection.
    """

    def __init__(self, update_callback):
        """
        :param update_callback: A callable with signature ```callable(update)``` for processing outgoing updates
        formatted as strings.
        """
        self.update_callback = update_callback
        NetworkTables.addGlobalListener(self._nt_on_change, immediateNotify=True)

    def process_update(self, update):
        """Process an incoming update from a remote NetworkTables"""
        data = json.loads(update)
        NetworkTables.getEntry(data["k"]).setValue(data["v"])

    def _send_update(self, data):
        """Send a NetworkTables update via the stored send_update callback"""
        if isinstance(data, dict):
            data = json.dumps(data)
        self.update_callback(data)

    def _nt_on_change(self, key, value, isNew):
        """NetworkTables global listener callback"""
        self._send_update({"k": key, "v": value, "n": isNew})

    def close(self):
        """
        Clean up NetworkTables listeners
        """
        NetworkTables.removeGlobalListener(self._nt_on_change)
