
ACTION_NAME = 'SIGNAL_RESET'

class SignalResetAction:

    def __init__(self, signal=None):
        self.do = ACTION_NAME
        self.signal = signal

    def from_json(json_object):
        return SignalResetAction(json_object['signal'])