class VerboseLogger:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    def log(self, message: str):
        if self.enabled:
            print(message)