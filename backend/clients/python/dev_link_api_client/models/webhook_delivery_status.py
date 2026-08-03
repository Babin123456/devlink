from enum import Enum


class WebhookDeliveryStatus(str, Enum):
    DELIVERED = "delivered"
    EXHAUSTED = "exhausted"
    FAILED = "failed"
    PENDING = "pending"
    REPLAYED = "replayed"

    def __str__(self) -> str:
        return str(self.value)
