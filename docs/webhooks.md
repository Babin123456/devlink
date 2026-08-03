# DevLink Webhook Retry & Dead Letter Queue (DLQ) System (#646)

DevLink provides a high-reliability webhook delivery system featuring automatic exponential backoff retries, delivery tracking, monitoring metrics, and a Dead Letter Queue (DLQ) for failed delivery management and manual replay.

---

## 1. Webhook Delivery Lifecycle & Status Tracking

Every outgoing webhook event is assigned a tracking ID and moves through the following lifecycle states:

- **`PENDING`**: Initial status when a webhook event is queued or awaiting delivery attempt.
- **`DELIVERED`**: HTTP POST request succeeded with a 2xx status code.
- **`FAILED`**: HTTP request failed (network error, timeout, or 4xx/5xx response). Retries scheduled automatically.
- **`EXHAUSTED`**: Delivery reached `max_retries` threshold without success. Moved automatically to the **Dead Letter Queue (DLQ)**.
- **`REPLAYED`**: Event was successfully replayed from the Dead Letter Queue.

---

## 2. Exponential Backoff Retry Strategy

When an outgoing HTTP POST request fails, DevLink schedules subsequent delivery retries using exponential backoff:

$$\text{Delay (seconds)} = \min\left(\text{initial\_delay} \times \text{multiplier}^{(\text{attempt} - 1)}, \text{max\_delay}\right)$$

Default configuration parameters:
- **Initial Delay**: 2 seconds
- **Multiplier**: 2x
- **Max Retries**: 5 attempts (configurable up to 20 per webhook)
- **Max Delay Cap**: 3600 seconds (1 hour)

| Attempt Number | Delay Before Retry |
|----------------|--------------------|
| Attempt 1      | 2 seconds          |
| Attempt 2      | 4 seconds          |
| Attempt 3      | 8 seconds          |
| Attempt 4      | 16 seconds         |
| Attempt 5      | 32 seconds         |

If attempt 5 fails, the delivery transitions to `EXHAUSTED` and is pushed to `WebhookDeadLetterQueue`.

---

## 3. Dead Letter Queue (DLQ) Management

Events that fail all retry attempts are preserved immutably in the Dead Letter Queue for inspection and manual replay.

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/webhooks/dispatch` | Dispatches a new webhook event with automatic retry policy. |
| `POST` | `/api/v1/webhooks/retry-pending` | Triggers immediate retry processing for pending/failed events. |
| `GET`  | `/api/v1/webhooks/deliveries` | Returns paginated list of webhook deliveries. |
| `GET`  | `/api/v1/webhooks/deliveries/{id}` | Retrieves details for a specific webhook delivery. |
| `GET`  | `/api/v1/webhooks/dlq` | Lists all Dead Letter Queue entries with optional filter `is_replayed`. |
| `GET`  | `/api/v1/webhooks/dlq/{id}` | Retrieves single DLQ item details. |
| `POST` | `/api/v1/webhooks/dlq/{id}/replay` | Manually replays a specific DLQ item. |
| `POST` | `/api/v1/webhooks/dlq/replay-all` | Bulk replays all active DLQ items. |
| `DELETE` | `/api/v1/webhooks/dlq/{id}` | Deletes a DLQ entry. |
| `GET`  | `/api/v1/webhooks/metrics` | Retrieves webhook delivery success rates and DLQ counts. |

---

## 4. Monitoring Metrics API

`GET /api/v1/webhooks/metrics` returns real-time operational statistics:

```json
{
  "total_deliveries": 1250,
  "successful_deliveries": 1210,
  "failed_deliveries": 25,
  "pending_deliveries": 15,
  "dlq_count": 15,
  "replayed_count": 10,
  "delivery_success_rate": 96.8
}
```
