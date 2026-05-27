"""Helpers for validating numeric sidebar inputs."""

from __future__ import annotations

import re
from typing import Literal

NumericFieldKind = Literal["float", "int"]

_FLOAT_PARTIAL_RE = re.compile(r"^-?(?:\d+)?(?:\.\d*)?$")
_FLOAT_FINAL_RE = re.compile(r"^-?(?:\d+(?:\.\d*)?|\.\d+)$")
_INT_PARTIAL_RE = re.compile(r"^\d*$")
_INT_FINAL_RE = re.compile(r"^\d+$")


def normalize_numeric_text(value: str) -> str:
    """Strip surrounding whitespace from numeric text."""
    return value.strip()


def is_numeric_text_valid(value: str, kind: NumericFieldKind, *, final: bool = False) -> bool:
    """
    Validate a numeric text fragment or final value.

    Args:
        value: Raw text from the sidebar field.
        kind: ``"float"`` for X0 / X1, ``"int"`` for MAX ITER.
        final: When ``True``, require a fully-formed number. When ``False``,
            allow partial in-progress states such as ``-`` or ``1.``.
    """
    text = value

    if kind == "float":
        pattern = _FLOAT_FINAL_RE if final else _FLOAT_PARTIAL_RE
    elif kind == "int":
        pattern = _INT_FINAL_RE if final else _INT_PARTIAL_RE
    else:
        raise ValueError(f"Unknown numeric field kind: {kind}")

    return bool(pattern.fullmatch(text))
