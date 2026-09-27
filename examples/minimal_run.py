"""A tiny numeric example with no external data or model calls."""

from random import Random

from quant_harness import Candidate, CandidateArchive


def main() -> None:
    rng = Random(7)
    archive = CandidateArchive(capacity=20, rng=rng)

    for generation in range(100):
        value = rng.uniform(-1.0, 1.0)
        score = -((value - 0.37) ** 2)
        archive.insert(
            Candidate(
                source=f"x = {value:.6f}",
                score=score,
                generation=generation,
            )
        )

    for candidate in archive.top_k(3):
        print(f"score={candidate.score:.6f} source={candidate.source}")


if __name__ == "__main__":
    main()
