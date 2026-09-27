# Quant Harness Core

A small, data-agnostic Python package for managing iterative experiments. It
provides a candidate archive, a basic UCB1 selector, run-budget accounting,
JSONL event logging, and atomic JSON writes.

The repository is intentionally limited to general-purpose infrastructure.
It does not include strategy definitions, data-provider integrations, model
configuration, research results, or run artifacts.

## Quick start

Requires Python 3.10 or newer. The package uses only the Python standard
library.

```python
from quant_harness import Candidate, CandidateArchive

archive = CandidateArchive(capacity=100)
candidate = Candidate(source="x = 0.5", score=0.8, generation=0)
archive.insert(candidate)

print(archive.top_k(1)[0].source)
```

Run the small numeric example with:

```bash
python examples/minimal_run.py
```

## Components

- `CandidateArchive` deduplicates candidates by source fingerprint, keeps a
  bounded set of high-scoring candidates, and offers a simple parent sampler.
- `UCB1Selector` allocates trials across named options using caller-supplied
  rewards.
- `RunBudget` tracks elapsed time and caller-reported work units.
- `EventLog` appends JSON events to a newline-delimited file.
- `atomic_write_json` replaces a JSON file atomically.

These components do not load or execute candidate code. Applications provide
their own candidate generation, evaluation, and data handling.

## Scope and licensing

Keep credentials, private datasets, proprietary research, and generated run
outputs outside this repository. Runtime event logs and candidate metadata can
contain caller-provided content, so applications should decide what is safe to
persist.

No license is included. Public visibility alone does not grant permission to
reuse or redistribute the code; select a license before inviting reuse.
