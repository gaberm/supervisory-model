class Timestamp:
    timestamp: float

    def _validate_timestamp(self):
        if self.timestamp < 0:
            raise ValueError("Timestamp must be non-negative.")
