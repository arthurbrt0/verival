"""Análise de mutação mínima (AST) para o SUT.

Gera mutantes de ``src/roman_numerals.py`` (um operador por vez), roda cada
suíte de testes contra cada mutante e relata quais mutantes foram "mortos"
(algum teste falhou) ou "sobreviveram". Inspirado nos conceitos de Jia & Harman
(2011): hipótese do programador competente (mutantes = pequenas alterações
sintáticas) e escore de mutação = mortos / (gerados - equivalentes).

Uso:
    python tools/mutation_test.py                # imprime relatório
    python tools/mutation_test.py --write docs/mutation_report.md
"""
from __future__ import annotations

import argparse
import ast
import copy
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_FILE = ROOT / "src" / "roman_numerals.py"

SUITES = {
    "EP (partições)": "tests/test_equivalence_partitioning.py",
    "BVA (valores-limite)": "tests/test_boundary_values.py",
    "PBT (propriedades)": "tests/test_properties.py",
    "Todas": "tests",
}

# Mutantes que, por análise manual, são semanticamente equivalentes ao original
# (nenhum teste pode matá-los). Chave: descrição do mutante.
EQUIVALENT_MUTANTS: dict[str, str] = {}

_CMP_SWAP = {
    ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Is: ast.IsNot, ast.IsNot: ast.Is,
}
_BIN_SWAP = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.FloorDiv,
             ast.FloorDiv: ast.Mult, ast.Mod: ast.FloorDiv}


@dataclass
class Mutant:
    description: str
    source: str


def _is_docstring(node, parents):
    return (isinstance(parents.get(node), ast.Expr)
            and isinstance(node.value, str))


def _inside_raise(node, parents):
    """Constantes em mensagens de erro não fazem parte do comportamento testado."""
    while node in parents:
        node = parents[node]
        if isinstance(node, ast.Raise):
            return True
    return False


def generate_mutants(source: str) -> list[Mutant]:
    """Enumera mutantes de primeira ordem para o código-fonte dado."""
    tree = ast.parse(source)
    parents = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
    nodes = list(ast.walk(tree))
    mutants: list[Mutant] = []

    def emit(index: int, mutate, description: str):
        clone = copy.deepcopy(tree)
        target = list(ast.walk(clone))[index]
        result = mutate(target)
        if result is not None:  # mutate pode devolver um novo nó para substituir
            parent = next(p for p in ast.walk(clone) if target in ast.iter_child_nodes(p))
            for field, value in ast.iter_fields(parent):
                if value is target:
                    setattr(parent, field, result)
                elif isinstance(value, list) and target in value:
                    value[value.index(target)] = result
        ast.fix_missing_locations(clone)
        mutants.append(Mutant(f"L{getattr(nodes[index], 'lineno', '?')}: {description}",
                              ast.unparse(clone)))

    for i, node in enumerate(nodes):
        if isinstance(node, ast.Compare):
            for k, op in enumerate(node.ops):
                if type(op) in _CMP_SWAP:
                    new = _CMP_SWAP[type(op)]
                    emit(i, lambda t, k=k, new=new: t.ops.__setitem__(k, new()),
                         f"{type(op).__name__} -> {new.__name__}")
        elif isinstance(node, ast.BinOp) and type(node.op) in _BIN_SWAP:
            new = _BIN_SWAP[type(node.op)]
            emit(i, lambda t, new=new: setattr(t, "op", new()),
                 f"{type(node.op).__name__} -> {new.__name__}")
        elif isinstance(node, ast.BoolOp):
            new = ast.And if isinstance(node.op, ast.Or) else ast.Or
            emit(i, lambda t, new=new: setattr(t, "op", new()),
                 f"{type(node.op).__name__} -> {new.__name__}")
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            emit(i, lambda t: t.operand, "remove 'not'")
        elif (isinstance(node, ast.Constant) and not _is_docstring(node, parents)
              and not _inside_raise(node, parents)):
            v = node.value
            if isinstance(v, bool) or v is None:
                continue
            if isinstance(v, int):
                for delta in (1, -1):
                    emit(i, lambda t, d=delta: setattr(t, "value", t.value + d),
                         f"constante {v} -> {v + delta}")
            elif isinstance(v, str) and v:
                new = v[::-1] if len(v) > 1 else v + v
                if new != v:
                    emit(i, lambda t, n=new: setattr(t, "value", n),
                         f"string {v!r} -> {new!r}")
        elif isinstance(node, ast.Raise):
            emit(i, lambda t: ast.Pass(), "remove 'raise'")
        elif isinstance(node, ast.If):
            emit(i, lambda t: setattr(t, "test", ast.Constant(False)),
                 "condição do 'if' -> False")
    # remove duplicatas preservando ordem
    seen, unique = set(), []
    for m in mutants:
        if m.source not in seen and m.source != ast.unparse(tree):
            seen.add(m.source)
            unique.append(m)
    return unique


def run_suite(mutant_src_dir: Path, target: str) -> bool:
    """Retorna True se a suíte FALHOU (isto é, o mutante foi morto)."""
    env = dict(os.environ, ROMAN_SRC_DIR=str(mutant_src_dir),
               HYPOTHESIS_PROFILE="deterministic", PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", target, "-x", "-q", "-p", "no:cacheprovider",
         "--no-header", "-o", "addopts="],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=300,
    )
    return proc.returncode != 0


def evaluate(index_mutant: tuple[int, Mutant]) -> tuple[int, dict[str, bool]]:
    index, mutant = index_mutant
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "roman_numerals.py").write_text(mutant.source, encoding="utf-8")
        return index, {name: run_suite(Path(tmp), target) for name, target in SUITES.items()}


def build_report(mutants: list[Mutant], results: dict[int, dict[str, bool]]) -> str:
    names = list(SUITES)
    lines = ["# Relatório de análise de mutação", "",
             f"Mutantes gerados: **{len(mutants)}** "
             f"(equivalentes descartados manualmente: {len(EQUIVALENT_MUTANTS)}).", "",
             "| Suíte | Mortos | Sobreviventes | Escore de mutação |", "|---|---|---|---|"]
    valid = [i for i, m in enumerate(mutants) if m.description not in EQUIVALENT_MUTANTS]
    for name in names:
        killed = sum(results[i][name] for i in valid)
        lines.append(f"| {name} | {killed} | {len(valid) - killed} | "
                     f"{100 * killed / len(valid):.1f}% |")
    lines += ["", "## Matriz mutante x suíte (X = morto)", "",
              "| # | Mutante | " + " | ".join(names) + " |",
              "|---|---|" + "---|" * len(names)]
    for i, m in enumerate(mutants):
        marks = " | ".join("X" if results[i][n] else "." for n in names)
        eq = " (equivalente)" if m.description in EQUIVALENT_MUTANTS else ""
        lines.append(f"| {i + 1} | `{m.description}`{eq} | {marks} |")
    survivors = [m for i, m in enumerate(mutants)
                 if not results[i]["Todas"] and m.description not in EQUIVALENT_MUTANTS]
    lines += ["", "## Sobreviventes da suíte completa", ""]
    lines += [f"- `{m.description}`" for m in survivors] or ["Nenhum."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", type=Path, help="grava o relatório em Markdown")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    mutants = generate_mutants(SRC_FILE.read_text(encoding="utf-8"))
    print(f"{len(mutants)} mutantes gerados; executando {len(SUITES)} suítes cada...",
          flush=True)
    results: dict[int, dict[str, bool]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for done, (index, outcome) in enumerate(pool.map(evaluate, enumerate(mutants)), 1):
            results[index] = outcome
            print(f"  [{done}/{len(mutants)}] {mutants[index].description}", flush=True)
    report = build_report(mutants, results)
    print(report)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
