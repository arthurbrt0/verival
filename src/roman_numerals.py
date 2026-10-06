"""Roman Numerals Encoder (CodeWars kata 51b62bf6a9c58071c600001b).

Converte um inteiro em sua representação em algarismos romanos.

Regras do kata:
    * Entrada: inteiro no intervalo fechado [1, 3999].
    * Saída: string com a forma canônica (subtrativa) do número romano.

Decisões de projeto (o kata não especifica o comportamento fora do domínio):
    * Inteiros fora de [1, 3999] -> ``ValueError``.
    * Qualquer valor que não seja ``int`` (incluindo ``bool``, ``float``,
      ``str`` e ``None``) -> ``TypeError``.
"""

MIN_VALUE = 1
MAX_VALUE = 3999

# Tabela em ordem decrescente, incluindo os pares subtrativos (CM, CD, XC, XL, IX, IV).
_NUMERALS = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)


def to_roman(n):
    """Retorna o numeral romano de ``n`` (1 <= n <= 3999)."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"esperado int, recebido {type(n).__name__}")
    if n < MIN_VALUE or n > MAX_VALUE:
        raise ValueError(f"valor fora do intervalo [{MIN_VALUE}, {MAX_VALUE}]: {n}")

    result = []
    remaining = n
    for value, symbol in _NUMERALS:
        count, remaining = divmod(remaining, value)
        result.append(symbol * count)
    return "".join(result)


# Nome exigido pela assinatura do kata no CodeWars.
solution = to_roman
