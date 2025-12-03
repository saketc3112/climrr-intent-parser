import re
from typing import Tuple, List, Set

_VAR_RE = re.compile(r'\{([a-zA-Z0-9_~]+)\}')
_EXPR_RE = re.compile(r'\{\{(.+?)\}\}|\{expr:([^}]+)\}')

def separate_vars_and_exprs(text: str) -> Tuple[Set[str], List[str]]:
    """
    Given combined question+answer template text, return:
    - set of variable placeholders (like "precipann_hist", "Location", "tempmax")
    - list of expression placeholders (strings to eval) if present.
    
    This is intentionally conservative: it returns variables that look like simple placeholders.
    For expressions, we look for either double-curly {{ expr }} or {expr:...}.
    """
    vars_found = set(m.group(1) for m in _VAR_RE.finditer(text))
    exprs = []
    for m in _EXPR_RE.finditer(text):
        g1, g2 = m.group(1), m.group(2)
        if g1:
            exprs.append(g1.strip())
        elif g2:
            exprs.append(g2.strip())
    return vars_found, exprs

