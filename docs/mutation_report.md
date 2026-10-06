# Relatório de análise de mutação

Mutantes gerados: **53** (equivalentes descartados manualmente: 0).

| Suíte | Mortos | Sobreviventes | Escore de mutação |
|---|---|---|---|
| EP (partições) | 47 | 6 | 88.7% |
| BVA (valores-limite) | 50 | 3 | 94.3% |
| PBT (propriedades) | 52 | 1 | 98.1% |
| Todas | 53 | 0 | 100.0% |

## Matriz mutante x suíte (X = morto)

| # | Mutante | EP (partições) | BVA (valores-limite) | PBT (propriedades) | Todas |
|---|---|---|---|---|---|
| 1 | `L15: constante 1 -> 2` | . | X | X | X |
| 2 | `L15: constante 1 -> 0` | . | X | X | X |
| 3 | `L16: constante 3999 -> 4000` | . | X | X | X |
| 4 | `L16: constante 3999 -> 3998` | . | X | . | X |
| 5 | `L38: condição do 'if' -> False` | X | . | X | X |
| 6 | `L40: condição do 'if' -> False` | X | X | X | X |
| 7 | `L38: Or -> And` | X | . | X | X |
| 8 | `L39: remove 'raise'` | X | . | X | X |
| 9 | `L40: Or -> And` | X | X | X | X |
| 10 | `L41: remove 'raise'` | X | X | X | X |
| 11 | `L20: constante 1000 -> 1001` | X | X | X | X |
| 12 | `L20: constante 1000 -> 999` | X | X | X | X |
| 13 | `L20: string 'M' -> 'MM'` | X | X | X | X |
| 14 | `L21: constante 900 -> 901` | X | X | X | X |
| 15 | `L21: constante 900 -> 899` | X | X | X | X |
| 16 | `L21: string 'CM' -> 'MC'` | X | X | X | X |
| 17 | `L22: constante 500 -> 501` | X | X | X | X |
| 18 | `L22: constante 500 -> 499` | X | X | X | X |
| 19 | `L22: string 'D' -> 'DD'` | X | X | X | X |
| 20 | `L23: constante 400 -> 401` | X | X | X | X |
| 21 | `L23: constante 400 -> 399` | X | X | X | X |
| 22 | `L23: string 'CD' -> 'DC'` | X | X | X | X |
| 23 | `L24: constante 100 -> 101` | X | X | X | X |
| 24 | `L24: constante 100 -> 99` | X | X | X | X |
| 25 | `L24: string 'C' -> 'CC'` | X | X | X | X |
| 26 | `L25: constante 90 -> 91` | X | X | X | X |
| 27 | `L25: constante 90 -> 89` | X | X | X | X |
| 28 | `L25: string 'XC' -> 'CX'` | X | X | X | X |
| 29 | `L26: constante 50 -> 51` | X | X | X | X |
| 30 | `L26: constante 50 -> 49` | X | X | X | X |
| 31 | `L26: string 'L' -> 'LL'` | X | X | X | X |
| 32 | `L27: constante 40 -> 41` | X | X | X | X |
| 33 | `L27: constante 40 -> 39` | X | X | X | X |
| 34 | `L27: string 'XL' -> 'LX'` | X | X | X | X |
| 35 | `L28: constante 10 -> 11` | X | X | X | X |
| 36 | `L28: constante 10 -> 9` | X | X | X | X |
| 37 | `L28: string 'X' -> 'XX'` | X | X | X | X |
| 38 | `L29: constante 9 -> 10` | X | X | X | X |
| 39 | `L29: constante 9 -> 8` | X | X | X | X |
| 40 | `L29: string 'IX' -> 'XI'` | X | X | X | X |
| 41 | `L30: constante 5 -> 6` | X | X | X | X |
| 42 | `L30: constante 5 -> 4` | X | X | X | X |
| 43 | `L30: string 'V' -> 'VV'` | X | X | X | X |
| 44 | `L31: constante 4 -> 5` | X | X | X | X |
| 45 | `L31: constante 4 -> 3` | X | X | X | X |
| 46 | `L31: string 'IV' -> 'VI'` | X | X | X | X |
| 47 | `L32: constante 1 -> 2` | X | X | X | X |
| 48 | `L32: constante 1 -> 0` | X | X | X | X |
| 49 | `L32: string 'I' -> 'II'` | X | X | X | X |
| 50 | `L38: remove 'not'` | X | X | X | X |
| 51 | `L40: Lt -> LtE` | . | X | X | X |
| 52 | `L40: Gt -> GtE` | . | X | X | X |
| 53 | `L47: Mult -> FloorDiv` | X | X | X | X |

## Sobreviventes da suíte completa

Nenhum.
