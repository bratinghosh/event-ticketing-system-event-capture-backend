# event-ticketing-system-event-capture-backend

### Purpose
- Log events for off-chain storage.
- Extract Analytics from logged events.

### Basic Event Format
```
Event: {
  contract_id: STRING
  wallet_id: STRING
  event: {
    type: STRING,
    data: { ... }
  }
}
```
