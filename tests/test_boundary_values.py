"""Técnica 2 - Análise de Valor Limite (BVA) / domain testing.

Segue a estratégia simplificada de Jeng & Weyuker (1994): para cada fronteira
escolhem-se um ponto ON (sobre a fronteira) e um ponto OFF (imediatamente do
outro lado). Aqui há dois tipos de fronteira:

1. Fronteiras do domínio:  n >= 1  e  n <= 3999.
2. Fronteiras internas, onde a regra de escrita do numeral muda (ex.: 3->4,
   4->5, 9->10, 39->40, 399->400, 999->1000). Trata-se de uma adaptação da
   técnica: o "domínio" de cada regra de escrita é um intervalo de inteiros.

Cada ``id`` BV-xx corresponde a uma linha em ``tests.md``.
"""
import sys

import pytest

from roman_numerals import MAX_VALUE, MIN_VALUE, to_roman


def test_domain_constants_match_kata_specification():
    assert (MIN_VALUE, MAX_VALUE) == (1, 3999)


# --- Fronteiras do domínio -------------------------------------------------

@pytest.mark.parametrize(
    "n, expected",
    [
        pytest.param(1, "I", id="BV-01 ON inferior (1)"),
        pytest.param(2, "II", id="BV-02 IN logo acima do limite inferior (2)"),
        pytest.param(3998, "MMMCMXCVIII", id="BV-03 IN logo abaixo do limite superior (3998)"),
        pytest.param(3999, "MMMCMXCIX", id="BV-04 ON superior (3999)"),
    ],
)
def test_domain_boundaries_valid(n, expected):
    assert to_roman(n) == expected


@pytest.mark.parametrize(
    "n",
    [
        pytest.param(0, id="BV-05 OFF inferior (0)"),
        pytest.param(-1, id="BV-06 OFF inferior (-1)"),
        pytest.param(4000, id="BV-07 OFF superior (4000)"),
        pytest.param(-sys.maxsize - 1, id="BV-08 extremo negativo"),
        pytest.param(sys.maxsize, id="BV-09 extremo positivo"),
    ],
)
def test_domain_boundaries_invalid(n):
    with pytest.raises(ValueError):
        to_roman(n)


# --- Fronteiras internas (mudança de regra de escrita) ---------------------

# (último valor da classe anterior, primeiro valor da próxima classe)
INTERNAL_BOUNDARIES = [
    # unidades
    pytest.param(3, "III", id="BV-10 3 (fim do aditivo)"),
    pytest.param(4, "IV", id="BV-11 4 (início do subtrativo)"),
    pytest.param(5, "V", id="BV-12 5 (V puro)"),
    pytest.param(6, "VI", id="BV-13 6 (início V + aditivo)"),
    pytest.param(8, "VIII", id="BV-14 8 (fim V + aditivo)"),
    pytest.param(9, "IX", id="BV-15 9 (subtrativo)"),
    pytest.param(10, "X", id="BV-16 10 (vira dezena)"),
    pytest.param(11, "XI", id="BV-17 11"),
    # dezenas
    pytest.param(39, "XXXIX", id="BV-18 39"),
    pytest.param(40, "XL", id="BV-19 40"),
    pytest.param(49, "XLIX", id="BV-20 49"),
    pytest.param(50, "L", id="BV-21 50"),
    pytest.param(89, "LXXXIX", id="BV-22 89"),
    pytest.param(90, "XC", id="BV-23 90"),
    pytest.param(99, "XCIX", id="BV-24 99"),
    pytest.param(100, "C", id="BV-25 100 (vira centena)"),
    # centenas
    pytest.param(399, "CCCXCIX", id="BV-26 399"),
    pytest.param(400, "CD", id="BV-27 400"),
    pytest.param(499, "CDXCIX", id="BV-28 499"),
    pytest.param(500, "D", id="BV-29 500"),
    pytest.param(899, "DCCCXCIX", id="BV-30 899"),
    pytest.param(900, "CM", id="BV-31 900"),
    pytest.param(999, "CMXCIX", id="BV-32 999"),
    # milhares
    pytest.param(1000, "M", id="BV-33 1000 (vira milhar)"),
    pytest.param(1001, "MI", id="BV-34 1001"),
    pytest.param(3000, "MMM", id="BV-35 3000 (3 milhares)"),
    pytest.param(3001, "MMMI", id="BV-36 3001"),
]


@pytest.mark.parametrize("n, expected", INTERNAL_BOUNDARIES)
def test_internal_rule_boundaries(n, expected):
    assert to_roman(n) == expected
