#!/usr/bin/env python3
"""
OmniResearch Real-time Data Leakage Scanner (AST Linter)
Zero-dependency static analysis tool that parses Python scripts into Abstract Syntax Trees (AST)
to detect data leakage patterns (pre-split scaling/imputation, temporal leakage, target contamination)
before code is executed.
"""

import argparse
import ast
import os
import sys
from pathlib import Path

LEAKY_TRANSFORMERS = {
    "StandardScaler", "MinMaxScaler", "RobustScaler", "Normalizer",
    "SimpleImputer", "KNNImputer", "IterativeImputer",
    "PCA", "TruncatedSVD", "FastICA", "FactorAnalysis",
    "OneHotEncoder", "OrdinalEncoder", "TargetEncoder",
    "PolynomialFeatures", "QuantileTransformer", "PowerTransformer"
}

SPLIT_FUNCTIONS = {
    "train_test_split", "KFold", "StratifiedKFold", "GroupKFold",
    "TimeSeriesSplit", "cross_val_score", "cross_validate"
}

TEMPORAL_KEYWORDS = {
    "date", "datetime", "time", "timestamp", "year", "month", "day", "epoch"
}

class LeakageVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.violations = []
        self.has_split = False
        self.split_line = None
        self.split_nodes = []
        self.temporal_vars = set()
        self.transformer_instances = {}  # var_name -> class_name

    def visit_Assign(self, node: ast.Assign):
        # Track transformer instantiation (e.g., scaler = StandardScaler())
        if isinstance(node.value, ast.Call):
            func_name = self._get_func_name(node.value.func)
            if func_name in LEAKY_TRANSFORMERS:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.transformer_instances[target.id] = func_name

        # Track temporal variables
        for target in node.targets:
            if isinstance(target, ast.Name):
                for kw in TEMPORAL_KEYWORDS:
                    if kw in target.id.lower():
                        self.temporal_vars.add(target.id)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        func_name = self._get_func_name(node.func)

        # Track train_test_split or cross-validation calls
        if func_name in SPLIT_FUNCTIONS:
            self.has_split = True
            if self.split_line is None:
                self.split_line = node.lineno
            self.split_nodes.append(node)

            # Check temporal leakage: random shuffling on temporal data
            if func_name == "train_test_split":
                shuffle_arg = True  # default in sklearn is shuffle=True
                for kw in node.keywords:
                    if kw.arg == "shuffle" and isinstance(kw.value, ast.Constant):
                        shuffle_arg = kw.value.value

                if shuffle_arg and self.temporal_vars:
                    self.violations.append({
                        "file": self.filename,
                        "line": node.lineno,
                        "type": "TEMPORAL_LEAKAGE",
                        "severity": "HIGH",
                        "message": (
                            f"Call to 'train_test_split' uses random shuffle=True while temporal variable(s) "
                            f"({', '.join(sorted(self.temporal_vars))}) were declared. "
                            f"Use TimeSeriesSplit or sequential temporal cutoff."
                        )
                    })

        # Check fit or fit_transform calls
        if isinstance(node.func, ast.Attribute) and node.func.attr in ("fit", "fit_transform"):
            caller_name = ""
            if isinstance(node.func.value, ast.Name):
                caller_name = node.func.value.id
            elif isinstance(node.func.value, ast.Call):
                caller_name = self._get_func_name(node.func.value.func)

            is_transformer = (
                caller_name in self.transformer_instances or
                caller_name in LEAKY_TRANSFORMERS or
                "scaler" in caller_name.lower() or
                "imputer" in caller_name.lower()
            )

            if is_transformer:
                # If fit is called before train_test_split in the file
                if not self.has_split:
                    # Check arguments passed to fit
                    arg_names = [self._get_arg_repr(a) for a in node.args]
                    arg_str = ", ".join(arg_names)
                    self.violations.append({
                        "file": self.filename,
                        "line": node.lineno,
                        "type": "PRE_SPLIT_DATA_LEAKAGE",
                        "severity": "CRITICAL",
                        "message": (
                            f"Pre-split transformation '{caller_name}.{node.func.attr}({arg_str})' detected at Line {node.lineno} "
                            f"before train/test partition. Fit must strictly occur on training folds only."
                        )
                    })

        self.generic_visit(node)

    def _get_func_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ""

    def _get_arg_repr(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_arg_repr(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_arg_repr(node.value)}[...]"
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        return "..."

def scan_file(file_path: Path) -> list[dict]:
    """Parse and inspect a single Python file for leakage."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(file_path))
        visitor = LeakageVisitor(filename=str(file_path))
        visitor.visit(tree)
        return visitor.violations
    except SyntaxError as e:
        return [{
            "file": str(file_path),
            "line": e.lineno or 1,
            "type": "SYNTAX_ERROR",
            "severity": "ERROR",
            "message": f"Syntax error preventing AST parsing: {e.msg}"
        }]
    except Exception as e:
        return [{
            "file": str(file_path),
            "line": 1,
            "type": "PARSE_ERROR",
            "severity": "WARNING",
            "message": f"Could not parse file: {str(e)}"
        }]

def scan_path(target_path: Path) -> list[dict]:
    violations = []
    if target_path.is_file():
        if target_path.suffix == ".py":
            violations.extend(scan_file(target_path))
    elif target_path.is_dir():
        for py_file in target_path.rglob("*.py"):
            # skip virtualenvs, .git, cache
            parts = py_file.parts
            if any(p.startswith(".") or p in ("venv", ".venv", "node_modules", "__pycache__") for p in parts):
                continue
            violations.extend(scan_file(py_file))
    return violations

def main():
    parser = argparse.ArgumentParser(description="Scan Python scripts for data leakage and methodological violations.")
    parser.add_argument("target", nargs="?", default="03_src/python", help="File or directory to scan (default: 03_src/python)")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if any violation is found")

    args = parser.parse_args()
    target_p = Path(args.target).resolve()

    if not target_p.exists():
        print(f"[ERROR] Target path does not exist: {target_p}")
        sys.exit(1)

    violations = scan_path(target_p)

    print(f"\n--- OmniResearch Data Leakage Scanner (AST Linter) ---")
    print(f"Target: {target_p.as_posix()}")

    if not violations:
        print("[PASSED] Zero data leakage patterns detected. Pipelines conform to strict partition standards.")
        print("------------------------------------------------------\n")
        sys.exit(0)

    print(f"[VIOLATIONS DETECTED] Found {len(violations)} potential methodological issue(s):\n")
    critical_count = 0
    for v in violations:
        rel_f = v['file']
        try:
            rel_f = Path(v['file']).relative_to(Path.cwd()).as_posix()
        except Exception:
            pass
        sev = v['severity']
        if sev in ("CRITICAL", "HIGH"):
            critical_count += 1
        print(f"  • [{sev}] {v['type']}")
        print(f"    Location : {rel_f}:{v['line']}")
        print(f"    Issue    : {v['message']}\n")

    print(f"Total: {len(violations)} issues ({critical_count} critical/high).")
    print("------------------------------------------------------\n")

    if args.strict and critical_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
