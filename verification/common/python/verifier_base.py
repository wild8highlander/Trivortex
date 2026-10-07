"""Base verifier class for all sections."""

import time
from typing import Any, Dict, List


class BaseVerifier:
    """Base class for section verifiers."""

    def __init__(self, config):
        self.config = config
        self.results = []
        self.metrics = {}
        self._start = 0.0

    def verify(self):
        self._start = time.perf_counter()
        self.results = self.run_verification()
        self.metrics = self.compute_metrics()
        return {
            "results": self.results,
            "metrics": self.metrics,
            "elapsed": time.perf_counter() - self._start,
        }

    def run_verification(self):
        raise NotImplementedError

    def compute_metrics(self):
        raise NotImplementedError
