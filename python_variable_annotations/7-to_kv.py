#!/usr/bin/env python3
"""Write a type-annotated function to_kv.
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """return a new tuple"""
    return (k, v * v)
    