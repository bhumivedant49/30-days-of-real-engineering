# Day 2 — What happens when the database goes down?

## Hypothesis
What I expected: ...

## Baseline (before)
- Status: ...  | Time to fail: ...s | Server stayed up: yes/no
- Exception seen: ServerSelectionTimeoutError
- Screenshot: evidence/02-failure-before.png

## Changes
1. serverSelectionTimeoutMS=3000 (was 30s default)
2. Global handler: ConnectionFailure → 503 + Retry-After
3. /health endpoint that pings MongoDB

## Verification
| Check | Before | After |
...

## Trade-offs & what I'd do next
- Server-selection failure = write never sent → safe to retry
- Mid-write network timeout = outcome unknown → needs idempotency keys
- A 3s timeout may be too aggressive on a slow network
- Next: retries with backoff, idempotency keys, structured logging

## How to reproduce
Steps to stop/start MongoDB and rerun requests.