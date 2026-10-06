"""Técnica 1 - Particionamento em Classes de Equivalência (EP).

Veja ``tests.md`` (seção 2) para a justificativa das partições e a tabela de
rastreabilidade. Cada ``id`` abaixo (EP-xx) corresponde a uma linha em tests.md.

Partição do domínio válido: o numeral é construído dígito a dígito (unidades,
dezenas, centenas, milhares) e cada dígito decimal cai em uma de seis classes
com regra de escrita distinta:

    0 -> vazio | 1-3 -> aditivo | 4 -> subtrativo | 5 -> símbolo médio
    6-8 -> médio + aditivo | 9 -> subtrativo
"""
import pytest

import roman_numerals
from roman_numerals import to_roman

# --- Classes válidas -------------------------------------------------------

VALID_CLASSES = [
    # Unidades (milhares = centenas = dezenas = 0 ou fora de foco)
    pytest.param(10, "X", id="EP-01 unidades=0"),
    pytest.param(2, "II", id="EP-02 unidades 1-3 (aditivo)"),
    pytest.param(4, "IV", id="EP-03 unidades=4 (subtrativo)"),
    pytest.param(5, "V", id="EP-04 unidades=5"),
    pytest.param(7, "VII", id="EP-05 unidades 6-8 (V + aditivo)"),
    pytest.param(9, "IX", id="EP-06 unidades=9 (subtrativo)"),
    # Dezenas
    pytest.param(101, "CI", id="EP-07 dezenas=0"),
    pytest.param(20, "XX", id="EP-08 dezenas 1-3 (aditivo)"),
    pytest.param(40, "XL", id="EP-09 dezenas=4 (subtrativo)"),
    pytest.param(50, "L", id="EP-10 dezenas=5"),
    pytest.param(70, "LXX", id="EP-11 dezenas 6-8 (L + aditivo)"),
    pytest.param(90, "XC", id="EP-12 dezenas=9 (subtrativo)"),
    # Centenas
    pytest.param(14, "XIV", id="EP-13 centenas=0"),
    pytest.param(200, "CC", id="EP-14 centenas 1-3 (aditivo)"),
    pytest.param(400, "CD", id="EP-15 centenas=4 (subtrativo)"),
    pytest.param(500, "D", id="EP-16 centenas=5"),
    pytest.param(700, "DCC", id="EP-17 centenas 6-8 (D + aditivo)"),
    pytest.param(900, "CM", id="EP-18 centenas=9 (subtrativo)"),
    # Milhares
    pytest.param(999, "CMXCIX", id="EP-19 milhares=0"),
    pytest.param(2000, "MM", id="EP-20 milhares 1-3"),
    # Combinações com todas as posições preenchidas (exemplos do kata e extras)
    pytest.param(1990, "MCMXC", id="EP-21 exemplo do kata (1990)"),
    pytest.param(2008, "MMVIII", id="EP-22 exemplo do kata (2008)"),
    pytest.param(1994, "MCMXCIV", id="EP-23 subtrativos em 3 posições"),
    pytest.param(444, "CDXLIV", id="EP-24 subtrativos repetidos"),
    pytest.param(3888, "MMMDCCCLXXXVIII", id="EP-25 numeral mais longo (15 símbolos)"),
]


@pytest.mark.parametrize("n, expected", VALID_CLASSES)
def test_valid_equivalence_classes(n, expected):
    assert to_roman(n) == expected


# --- Classes inválidas: valor fora do domínio ------------------------------

@pytest.mark.parametrize(
    "n",
    [
        pytest.param(-5, id="EP-26 negativo"),
        pytest.param(5000, id="EP-27 acima de 3999"),
    ],
)
def test_integer_out_of_domain_raises_value_error(n):
    with pytest.raises(ValueError):
        to_roman(n)


# --- Classes inválidas: tipo incorreto -------------------------------------

@pytest.mark.parametrize(
    "value",
    [
        pytest.param(3.5, id="EP-28 float fracionário"),
        pytest.param(5.0, id="EP-29 float com valor inteiro"),
        pytest.param("10", id="EP-30 string numérica"),
        pytest.param(None, id="EP-31 None"),
        pytest.param(True, id="EP-32 bool (subclasse de int)"),
        pytest.param([5], id="EP-33 lista"),
    ],
)
def test_wrong_type_raises_type_error(value):
    with pytest.raises(TypeError):
        to_roman(value)


# --- Contrato da API do kata -----------------------------------------------

def test_kata_entry_point_is_alias():
    """EP-34: o CodeWars chama ``solution(n)``; deve ser equivalente a ``to_roman``."""
    assert roman_numerals.solution is to_roman
    assert roman_numerals.solution(1000) == "M"
