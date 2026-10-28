# Bivia Python SDK

[![CI](https://github.com/articul8/bivia-python/actions/workflows/ci.yml/badge.svg)](https://github.com/articul8/bivia-python/actions/workflows/ci.yml)

Python client for [Bivia](https://articul8.ai/bivia) by [Articul8 AI](https://articul8.ai). See [bivia](https://github.com/articul8/bivia) for full documentation and examples. -- a calibrated decision engine that returns typed, structured answers with confidence scores and evidence.

## Installation

```bash
pip install bivia
```

## Authentication

Set your API key as an environment variable:

```bash
export A8_API_KEY="your-api-key"
```

Or pass it directly:

```python
from bivia import Bivia

client = Bivia(api_key="your-api-key")
```

## Quick start

```python
from bivia import Bivia

client = Bivia()  # reads A8_API_KEY from env

# Yes/no decision
result = client.decisions.boolean(
    question="Is this urgent?",
    state="Customer threatened to cancel.",
)
print(result.value, result.probability)
# "yes"  0.92
```

## Decision types

### Boolean -- yes or no

```python
result = client.decisions.boolean(
    question="Does this contract contain an auto-renewal clause?",
    documents=[{"url": "https://example.com/contract.pdf"}],
)
print(result.value)        # "yes" or "no"
print(result.probability)  # P(value)
print(result.distribution) # {"yes": 0.94, "no": 0.06}
```

### Choice -- pick one from a list

```python
result = client.decisions.choice(
    question="Which team handles this?",
    choices=["billing", "refunds", "technical"],
    state="I need a copy of my invoice.",
)
print(result.value)        # "billing"
print(result.distribution) # {"billing": 0.93, "refunds": 0.04, "technical": 0.03}
```

### Auto-detect -- let the model choose the decision type

```python
result = client.decisions.create(
    question="Most likely diagnosis?",
    state="Patient has fever, cough, and a right lower lobe infiltrate.",
    outcomes=["common cold", "pneumonia", "healthy"],
)
print(result.type, result.value)  # "decide"  "pneumonia"
```

### Score -- numeric value on a scale

```python
result = client.decisions.score(
    question="How urgent is this (0=none, 1=critical)?",
    state="Customer threatened to cancel today.",
    range=[0, 1],
    buckets=11,
)
print(result.value)   # 0.7
print(result.levels)  # {"0": 0.02, "0.1": 0.03, ..., "1": 0.1}
```

### Multi-select -- zero or more options

```python
result = client.decisions.multi_select(
    question="Which actions apply?",
    options=["cancel", "refund", "status"],
    state="Order arrived damaged and the customer wants money back.",
)
print(result.value)          # ["cancel", "refund"]
print(result.probabilities)  # {"cancel": 0.93, "refund": 0.87, "status": 0.11}
```

### Span -- locate text in the input

```python
result = client.decisions.span(
    question="Where is the auto-renewal clause?",
    state="This agreement renews automatically for one year unless either party cancels.",
)
for span in result.value:
    print(f"[{span.start}:{span.end}] {span.text}")
```

## Visual grounding

### Image -- locate objects in images

```python
result = client.grounding.image(
    question="the invoice total",
    images=[{"url": "https://example.com/invoice.png"}],
)
for region in result.value:
    print(region.label, region.box, region.score)
```

### Video -- locate objects or events in video

```python
result = client.grounding.video(
    video={"url": "https://example.com/clip.mp4"},
    query="the red car",
    kind="object",
)
for hit in result.hits:
    print(f"{hit.start}s - {hit.end}s (confidence: {hit.confidence})")
```

## Data science -- decisions from raw signals

```python
result = client.data.decide(
    question="Which analysis method fits this signal?",
    signals=[{
        "name": "temperature",
        "data": [[72.1, 73.5, 89.2, 91.0, 88.5, 72.0]],
        "fs": 1,
    }],
    kind="choice",
    options=["spectral analysis (FFT)", "linear regression"],
)
print(result.value)
```

## Batch -- multiple questions in one request

```python
result = client.batch.create(
    state="I was double-charged and support never replied.",
    questions={
        "team": {
            "type": "choice",
            "instructions": "Which team?",
            "criteria": {
                "billing": "Billing disputes and invoices",
                "tech": "Product defects",
                "sales": "New purchases",
            },
        },
        "urgent": {
            "type": "boolean",
            "instructions": "Is this urgent?",
        },
        "risk": {
            "type": "score",
            "instructions": "Churn risk from 0 to 1",
            "buckets": 5,
        },
    },
)
print(result.answers["team"])
print(result.answers["urgent"])
print(result.usage.billable_tokens)
```

## Model discovery

```python
# List available models
models = client.models.list()
for m in models.models:
    print(m.name, m.description)

# Check capabilities
caps = client.models.capabilities()
print(caps.decision_types)  # ["decide", "boolean", "choice", ...]
print(caps.abstention)      # True
```

## Modes

- **`fast`** (default) -- single-pass inference, lowest latency.
- **`deep`** -- adds a verification step for higher confidence.

```python
result = client.decisions.boolean(
    question="Is this a fraudulent transaction?",
    state="...",
    mode="deep",
)
print(result.verification.performed)  # True
print(result.verification.result)     # "passed"
```

## Abstention

When the model is unsure, it abstains instead of guessing:

```python
result = client.decisions.boolean(
    question="Is this genuine?",
    state="Ambiguous context...",
)
if result.status == "abstained":
    print(f"Model abstained: {result.abstain_reason}")
else:
    print(f"Answer: {result.value} (p={result.probability})")
```

Disable abstention to force a best-effort answer:

```python
result = client.decisions.boolean(
    question="Is this genuine?",
    state="Ambiguous context...",
    allow_abstain=False,
)
```

## Error handling

```python
from bivia import Bivia, AuthenticationError, RateLimitError, APIError

client = Bivia()
try:
    result = client.decisions.boolean(question="Test?")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limited -- retries exhausted")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

## Context manager

```python
with Bivia() as client:
    result = client.decisions.boolean(question="Is this valid?", state="...")
    print(result.value)
```

## Configuration

| Parameter | Env var | Default |
|---|---|---|
| `api_key` | `A8_API_KEY` | -- (required) |
| `base_url` | -- | `https://api.articul8.ai/bivia` |
| `timeout` | -- | `60.0` seconds |
| `max_retries` | -- | `2` |
