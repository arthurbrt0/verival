"""Técnica 3 - Teste baseado em propriedades (property-based testing).

Inspirado em QuickCheck (Claessen & Hughes, 2000), via biblioteca Hypothesis.
Em vez de listar pares (entrada, saída), enunciamos invariantes que valem para
todo o domínio e deixamos o gerador explorar entradas. Os oráculos usados
(``from_roman`` e ``CANONICAL_RE``) são independentes do SUT (ver ``oracle.py``).

Cada ``PB-xx`` corresponde a uma linha em ``tests.md``.
"""
from hypothesis import given, strategies as st

import pytest

from oracle import CANONICAL_RE, from_roman
from roman_numerals import to_roman

# Limites do kata escritos como literais, NÃO importados do SUT: se o gerador
# dependesse das constantes do SUT, um defeito nelas "moveria" também o domínio
# testado e passaria despercebido (descoberto pela análise de mutação).
MIN_VALUE = 1
MAX_VALUE = 3999

valid_numbers = st.integers(min_value=MIN_VALUE, max_value=MAX_VALUE)


@given(valid_numbers)
def test_pb01_round_trip(n):
    """PB-01: decodificar o resultado devolve o número original."""
    assert from_roman(to_roman(n)) == n


@given(valid_numbers)
def test_pb02_output_is_canonical_roman(n):
    """PB-02: saída é str não vazia que obedece à gramática canônica (sem 4 repetições, etc.)."""
    result = to_roman(n)
    assert isinstance(result, str)
    assert result != ""
    assert CANONICAL_RE.fullmatch(result)


@given(valid_numbers, st.sampled_from([10, 100, 1000]))
def test_pb03_decimal_decomposition(n, base):
    """PB-03: o numeral é a concatenação dos numerais de cada ordem decimal."""
    low = n % base
    high = n - low
    if low == 0 or high == 0:
        return  # nada a decompor
    assert to_roman(n) == to_roman(high) + to_roman(low)


@given(valid_numbers, valid_numbers)
def test_pb04_injective(a, b):
    """PB-04: números distintos produzem numerais distintos."""
    if a != b:
        assert to_roman(a) != to_roman(b)


@given(valid_numbers)
def test_pb05_deterministic_and_length_bound(n):
    """PB-05: função pura (mesma entrada, mesma saída) e no máx. 15 símbolos."""
    assert to_roman(n) == to_roman(n)
    assert len(to_roman(n)) <= 15


@given(st.one_of(st.integers(max_value=MIN_VALUE - 1), st.integers(min_value=MAX_VALUE + 1)))
def test_pb06_out_of_domain_integers_raise_value_error(n):
    """PB-06: todo inteiro fora de [1, 3999] levanta ValueError."""
    with pytest.raises(ValueError):
        to_roman(n)


@given(
    st.one_of(
        st.floats(),
        st.text(),
        st.none(),
        st.booleans(),
        st.binary(),
        st.lists(st.integers()),
    )
)
def test_pb07_non_integers_raise_type_error(value):
    """PB-07: qualquer valor não-int levanta TypeError."""
    with pytest.raises(TypeError):
        to_roman(value)
