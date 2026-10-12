# Day 2: What happens when the database goes down?

## Hypothesis
[Write what you expected BEFORE testing, e.g. "I expected a fast 500 error."]

## Baseline (Day 1 code, MongoDB stopped)
- GET /tasks → HTTP 500 after 30.25s
- POST /tasks → HTTP [ ] after [ ]s
- Exception: pymongo.errors.ServerSelectionTimeoutError (WinError 10061, connection refused)
- The API process stayed up; each request failed independently
- Screenshots: evidence/04, 05, 06

## Changes
1. database.py: serverSelectionTimeoutMS=3000 (default is 30000)
2. main.py: global handler mapping ConnectionFailure → 503 + Retry-After
3. main.py: /health endpoint that pings MongoDB

## Verification
| Check | Before | After |
|---|---|---|
| GET /tasks status | 500 | 503 |
| GET /tasks time | 30.25s | 3.12s |
| POST /tasks | 500 / [ ]s | [ ] / [ ]s |
| /health with DB down | n/a | [ ] |
| Recovered after MongoDB restart | n/a | [ ] |

## Trade-offs
- ServerSelectionTimeoutError means no server was found, so the write was not sent. Retrying is safe.
- A network failure after a write is sent leaves the outcome unknown. Retrying blindly could duplicate data, so idempotency keys are needed.
- 3s may be too aggressive on slow networks or during failovers. It's a tuning decision.
- I did not load-test this, so I make no claims about behavior under concurrency.

## Next
Retries with backoff, idempotency keys, structured logging.

## Reproduce
1. Start MongoDB and the API. 2. Stop MongoDB (`net stop MongoDB`). 3. Run the curl commands in `commands.md`. 4. Restart MongoDB and re-run.