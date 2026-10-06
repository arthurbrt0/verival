# Casos de teste — Roman Numerals Encoder

**SUT:** `to_roman(n)` / `solution(n)` em [`src/roman_numerals.py`](src/roman_numerals.py)
(kata [51b62bf6a9c58071c600001b](https://www.codewars.com/kata/51b62bf6a9c58071c600001b), Python 3.11).

**Especificação adotada**

| Item | Regra |
|---|---|
| Domínio válido | inteiros `n` com `1 <= n <= 3999` |
| Saída | string do numeral romano na forma canônica (subtrativa: `IV`, `IX`, `XL`, `XC`, `CD`, `CM`) |
| `n` inteiro fora do domínio | `ValueError` *(decisão da equipe — o kata não especifica)* |
| `n` não é `int` (inclui `bool`, `float`, `str`, `None`) | `TypeError` *(decisão da equipe)* |

**Técnicas aplicadas:** (1) Particionamento em classes de equivalência, (2) Análise de valor limite
(domain testing), (3) Teste baseado em propriedades. A análise de mutação (seção 5) é usada para
*avaliar* as suítes, não como técnica de geração de casos.

Os IDs abaixo (`EP-xx`, `BV-xx`, `PB-xx`) aparecem literalmente nos `id=` dos testes parametrizados
(ou na docstring, no caso dos `PB`), o que dá rastreabilidade técnica → caso → código.

---

## 1. Rastreabilidade

| Técnica | Arquivo de teste | IDs | Qtde |
|---|---|---|---|
| Classes de equivalência | `tests/test_equivalence_partitioning.py` | EP-01 … EP-34 | 34 |
| Valores-limite | `tests/test_boundary_values.py` | BV-01 … BV-36 (+ 1 teste de constantes) | 37 |
| Propriedades | `tests/test_properties.py` | PB-01 … PB-07 (500 exemplos cada) | 7 |

---

## 2. Classes de equivalência (EP)

**Partição do domínio válido.** O numeral é construído dígito a dígito (unidades, dezenas, centenas,
milhares). Cada dígito decimal pertence a uma de seis classes com regra de escrita distinta:

| Dígito | Regra | Exemplo (unidades) |
|---|---|---|
| 0 | nada é escrito | — |
| 1–3 | repetição do símbolo | `I`, `II`, `III` |
| 4 | subtrativo | `IV` |
| 5 | símbolo médio | `V` |
| 6–8 | símbolo médio + repetição | `VI`, `VII`, `VIII` |
| 9 | subtrativo | `IX` |

Para milhares só existem as classes 0 e 1–3 (limite do domínio). Escolhe-se um representante por
classe e por posição: 6 × 3 + 2 = 20 casos, mais combinações.

**Partição do domínio inválido:** inteiro negativo, inteiro > 3999, tipos não inteiros.

| ID | Classe | Entrada | Saída esperada |
|---|---|---|---|
| EP-01 | unidades = 0 | 10 | `X` |
| EP-02 | unidades 1–3 | 2 | `II` |
| EP-03 | unidades = 4 | 4 | `IV` |
| EP-04 | unidades = 5 | 5 | `V` |
| EP-05 | unidades 6–8 | 7 | `VII` |
| EP-06 | unidades = 9 | 9 | `IX` |
| EP-07 | dezenas = 0 | 101 | `CI` |
| EP-08 | dezenas 1–3 | 20 | `XX` |
| EP-09 | dezenas = 4 | 40 | `XL` |
| EP-10 | dezenas = 5 | 50 | `L` |
| EP-11 | dezenas 6–8 | 70 | `LXX` |
| EP-12 | dezenas = 9 | 90 | `XC` |
| EP-13 | centenas = 0 | 14 | `XIV` |
| EP-14 | centenas 1–3 | 200 | `CC` |
| EP-15 | centenas = 4 | 400 | `CD` |
| EP-16 | centenas = 5 | 500 | `D` |
| EP-17 | centenas 6–8 | 700 | `DCC` |
| EP-18 | centenas = 9 | 900 | `CM` |
| EP-19 | milhares = 0 | 999 | `CMXCIX` |
| EP-20 | milhares 1–3 | 2000 | `MM` |
| EP-21 | exemplo do kata | 1990 | `MCMXC` |
| EP-22 | exemplo do kata | 2008 | `MMVIII` |
| EP-23 | subtrativos em 3 posições | 1994 | `MCMXCIV` |
| EP-24 | subtrativos repetidos | 444 | `CDXLIV` |
| EP-25 | numeral mais longo (15 símbolos) | 3888 | `MMMDCCCLXXXVIII` |
| EP-26 | inteiro negativo | -5 | `ValueError` |
| EP-27 | inteiro acima do domínio | 5000 | `ValueError` |
| EP-28 | float fracionário | 3.5 | `TypeError` |
| EP-29 | float com valor inteiro | 5.0 | `TypeError` |
| EP-30 | string numérica | `"10"` | `TypeError` |
| EP-31 | `None` | `None` | `TypeError` |
| EP-32 | `bool` (subclasse de `int`) | `True` | `TypeError` |
| EP-33 | lista | `[5]` | `TypeError` |
| EP-34 | contrato do kata | `solution is to_roman`; `solution(1000)` | `M` |

---

## 3. Valores-limite (BV)

Segue Jeng & Weyuker (1994): para cada fronteira, um ponto **ON** (sobre a fronteira) e um **OFF**
(do outro lado), mais pontos internos adjacentes. Dois tipos de fronteira:

1. **Domínio:** `n >= 1` e `n <= 3999`.
2. **Internas** (adaptação nossa): pontos em que a regra de escrita muda (3→4, 4→5, 5→6, 8→9, 9→10,
   39→40, …, 999→1000).

| ID | Fronteira | Entrada | Saída esperada |
|---|---|---|---|
| BV-01 | ON inferior | 1 | `I` |
| BV-02 | IN (limite inferior + 1) | 2 | `II` |
| BV-03 | IN (limite superior − 1) | 3998 | `MMMCMXCVIII` |
| BV-04 | ON superior | 3999 | `MMMCMXCIX` |
| BV-05 | OFF inferior | 0 | `ValueError` |
| BV-06 | OFF inferior | -1 | `ValueError` |
| BV-07 | OFF superior | 4000 | `ValueError` |
| BV-08 | extremo negativo | `-sys.maxsize-1` | `ValueError` |
| BV-09 | extremo positivo | `sys.maxsize` | `ValueError` |
| BV-10 | fim do aditivo | 3 | `III` |
| BV-11 | início do subtrativo | 4 | `IV` |
| BV-12 | V puro | 5 | `V` |
| BV-13 | início V + aditivo | 6 | `VI` |
| BV-14 | fim V + aditivo | 8 | `VIII` |
| BV-15 | subtrativo | 9 | `IX` |
| BV-16 | vira dezena | 10 | `X` |
| BV-17 | | 11 | `XI` |
| BV-18 | | 39 | `XXXIX` |
| BV-19 | | 40 | `XL` |
| BV-20 | | 49 | `XLIX` |
| BV-21 | | 50 | `L` |
| BV-22 | | 89 | `LXXXIX` |
| BV-23 | | 90 | `XC` |
| BV-24 | | 99 | `XCIX` |
| BV-25 | vira centena | 100 | `C` |
| BV-26 | | 399 | `CCCXCIX` |
| BV-27 | | 400 | `CD` |
| BV-28 | | 499 | `CDXCIX` |
| BV-29 | | 500 | `D` |
| BV-30 | | 899 | `DCCCXCIX` |
| BV-31 | | 900 | `CM` |
| BV-32 | | 999 | `CMXCIX` |
| BV-33 | vira milhar | 1000 | `M` |
| BV-34 | | 1001 | `MI` |
| BV-35 | 3 milhares | 3000 | `MMM` |
| BV-36 | | 3001 | `MMMI` |
| —     | constantes do domínio | `(MIN_VALUE, MAX_VALUE)` | `(1, 3999)` |

---

## 4. Propriedades (PB)

Gerador: `st.integers(1, 3999)` para entradas válidas; geradores específicos para inválidas.
Os oráculos (`from_roman`, `CANONICAL_RE`) estão em `tests/oracle.py` e **não importam o SUT**.

| ID | Propriedade | Gerador |
|---|---|---|
| PB-01 | Round-trip: `from_roman(to_roman(n)) == n` | inteiros 1..3999 |
| PB-02 | Saída é `str` não vazia e casa com a gramática canônica `^M{0,3}(CM\|CD\|D?C{0,3})(XC\|XL\|L?X{0,3})(IX\|IV\|V?I{0,3})$` | inteiros 1..3999 |
| PB-03 | Decomposição decimal: `to_roman(n) == to_roman(n - n%b) + to_roman(n%b)` para `b ∈ {10,100,1000}` | inteiros 1..3999 × base |
| PB-04 | Injetividade: `a != b ⇒ to_roman(a) != to_roman(b)` | pares de inteiros |
| PB-05 | Determinismo e tamanho ≤ 15 símbolos | inteiros 1..3999 |
| PB-06 | Todo inteiro fora de [1, 3999] ⇒ `ValueError` | inteiros ≤ 0 ou ≥ 4000 |
| PB-07 | Todo não-`int` ⇒ `TypeError` | floats, texto, `None`, bool, bytes, listas |

---

## 5. Avaliação das suítes por análise de mutação

Ferramenta: `tools/mutation_test.py` (53 mutantes de primeira ordem: troca de operadores de
comparação/aritméticos, constantes ±1, strings invertidas, remoção de `raise`/`not`, condição → `False`).
Relatório completo com a matriz mutante × suíte em [`docs/mutation_report.md`](docs/mutation_report.md).

| Suíte | Mortos / 53 | Escore |
|---|---|---|
| EP | 47 | 88,7% |
| BVA | 50 | 94,3% |
| PBT | 52 | 98,1% |
| Todas | 53 | 100% |

**Leitura dos resultados**

* A suíte EP sozinha deixa 6 mutantes vivos, todos de fronteira do domínio (`n < 1` → `n <= 1`,
  `n > 3999` → `n >= 3999` e as constantes `MIN_VALUE`/`MAX_VALUE` ±1), pois escolhe representantes
  "do meio" das classes.
* A suíte BVA sozinha deixa 3 mutantes vivos, todos na validação de tipo (linhas 38–39 do SUT:
  `or` → `and`, condição → `False`, remoção do `raise TypeError`), porque só usa inteiros como
  entrada. EP (EP-28…33) e PBT (PB-07) matam esses mutantes.
* A suíte PBT quase mata tudo, mas **deixou sobreviver `MAX_VALUE: 3999 → 3998`**: com 500 exemplos
  aleatórios em 3999 valores, a chance de sortear exatamente 3999 é baixa. Só o teste de valor-limite
  (BV-04) o detecta — evidência concreta da complementaridade entre as técnicas.
* Nenhum mutante equivalente foi identificado; todos os sobreviventes de suítes individuais são
  mortos pela suíte completa.
