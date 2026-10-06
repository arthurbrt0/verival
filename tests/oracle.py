"""Oráculos independentes do SUT, usados pelos testes baseados em propriedades.

Nada aqui importa ``roman_numerals``: assim, um defeito no SUT não pode
"contaminar" o oráculo.
"""
import re

# Gramática canônica dos numerais romanos de 1 a 3999 (forma subtrativa).
CANONICAL_RE = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)

_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def from_roman(text):
    """Decodificador romano -> inteiro (regra: símbolo menor antes de maior subtrai)."""
    total = 0
    for current, following in zip(text, text[1:] + " "):
        value = _VALUES[current]
        if following != " " and _VALUES[following] > value:
            total -= value
        else:
            total += value
    return total
