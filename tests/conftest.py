"""Configuração do pytest.

* ``ROMAN_SRC_DIR``: sobrescreve o diretório do SUT. Usado por
  ``tools/mutation_test.py`` para rodar a mesma suíte contra mutantes sem
  alterar ``src/``.
* ``HYPOTHESIS_PROFILE``: ``default`` (aleatório, 500 exemplos) ou
  ``deterministic`` (reprodutível; usado na análise de mutação).
"""
import os
import sys
from pathlib import Path

from hypothesis import HealthCheck, settings

_tests_dir = Path(__file__).resolve().parent
_default_src = _tests_dir.parent / "src"
sys.path.insert(0, os.environ.get("ROMAN_SRC_DIR", str(_default_src)))
sys.path.insert(0, str(_tests_dir))  # para importar `oracle`

settings.register_profile(
    "default", max_examples=500, deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.register_profile(
    "deterministic", max_examples=500, deadline=None, derandomize=True,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "default"))
