# Architecture diagram patterns

Mermaid diagrams for project READMEs. GitHub renders these natively, so they live
in version control as editable text — no design file to lose, and a reviewer can
see them without leaving the page.

Copy the fenced block you need into your README and edit the labels. Keep each
diagram to one idea; two clear diagrams beat one that shows everything.

---

## 1. System context

Draw this for every non-trivial project. It answers "what talks to what" in about
five seconds.

```mermaid
graph LR
    User[Staff user] --> Web[React frontend]
    Mobile[Flutter app] --> API
    Web --> API[Laravel REST API]
    API --> DB[(Oracle)]
    API --> Cache[(Redis)]
    API --> Queue[Queue worker]
    Queue --> Mail[Email provider]
    API --> Payment[Payment gateway]
```

---

## 2. Request flow

A sequence diagram for the one genuinely interesting path. For integration and
payment work this is the diagram that carries the most weight, because it shows
you have thought about ordering and confirmation rather than just wiring calls.

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database
    participant G as Payment gateway

    C->>A: POST /api/v1/payments
    A->>A: Validate request
    A->>D: Create payment (status: pending)
    A->>G: Initiate charge (idempotency key)
    G-->>A: Accepted, reference
    A->>D: Store gateway reference
    A-->>C: 202 Accepted

    G->>A: Webhook: charge settled
    A->>A: Verify signature
    A->>D: Mark payment settled
    A-->>G: 200 OK
```

Note what this communicates without a word of prose: idempotency, a pending state
before confirmation, signature verification on the inbound webhook, and
acknowledgement so the provider stops retrying.

---

## 3. Failure and retry path

Worth drawing separately when reliability is the point of the system. Most READMEs
only ever document the happy path.

```mermaid
flowchart TD
    Start[Job picked up] --> Call{Call external service}
    Call -->|2xx| Done[Mark complete]
    Call -->|4xx| Fail[Mark failed, no retry]
    Call -->|5xx or timeout| Retry{Attempts exhausted?}
    Retry -->|No| Backoff[Wait, exponential backoff] --> Call
    Retry -->|Yes| Dead[Move to failed queue, alert]
    Fail --> Log[Record reason for review]
```

---

## 4. Data model

An entity-relationship diagram of the core tables. Show the central five to ten,
never all sixty — the point is to convey the shape of the domain.

```mermaid
erDiagram
    CUSTOMER ||--o{ INVOICE : has
    INVOICE  ||--|{ INVOICE_ITEM : contains
    INVOICE  ||--o{ PAYMENT : receives
    PAYMENT  }o--|| PAYMENT_METHOD : uses

    CUSTOMER {
        int id PK
        string name
        string email
    }
    INVOICE {
        int id PK
        int customer_id FK
        string status
        decimal total
        date issued_at
    }
    PAYMENT {
        int id PK
        int invoice_id FK
        decimal amount
        string gateway_reference
        string status
    }
```

---

## 5. Deployment

Where your Linux, Nginx, and server administration experience becomes visible
rather than merely asserted.

```mermaid
graph TD
    Internet((Internet)) --> Nginx[Nginx: TLS termination, static files]
    Nginx --> FPM[PHP-FPM: Laravel]
    FPM --> Oracle[(Oracle database)]
    FPM --> Redis[(Redis: cache, queue)]
    Redis --> Worker[Queue worker: supervisor-managed]
    Worker --> Oracle
    Cron[Cron: artisan schedule:run] --> FPM
```

---

## Notes

- Keep node labels short. Long labels wrap badly and make the diagram unreadable
  on a phone.
- Mermaid dislikes unquoted parentheses and colons in labels. Wrap awkward text in
  double quotes: `A["Auth service (v2)"]`.
- Check rendering in both GitHub light and dark themes before committing.
- A Mermaid diagram is not accessible to a screen reader, so make sure the
  paragraph beside it conveys the same information in words.
- Never put real hostnames, internal IP addresses, or client names in a diagram
  you publish.
