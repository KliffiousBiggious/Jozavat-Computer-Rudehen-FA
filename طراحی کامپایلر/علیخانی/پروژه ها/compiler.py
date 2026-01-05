# ==================================================
# Educational C++ Compiler (Pointer Subset)
# Course: Compiler Design
# Author: Amir Mahdi Mehrabian
# ==================================================

import re

# ---------- Token Definitions ----------
TOKEN_REGEX = [
    ("KEYWORD", r"\b(int|cout|endl)\b"),
    ("IDENTIFIER", r"[A-Za-z_]\w*"),
    ("NUMBER", r"\d+"),
    ("STRING", r"\".*?\""),
    ("OPERATOR", r"<<|=|\*|&"),
    ("SEMICOLON", r";"),
]

IGNORE_LINES = [
    r"#include.*",
    r"using\s+namespace\s+std;",
    r"int\s+main\s*\(\s*\)\s*\{",
    r"\}",
    r"\{"
]

GRAMMAR = {
    "decl": r"int\s+[A-Za-z_]\w*\s*=\s*\d+\s*;",
    "ptrdecl": r"int\s*\*\s*[A-Za-z_]\w*\s*=\s*&\s*[A-Za-z_]\w*\s*;",
    "assign": r"\*\s*[A-Za-z_]\w*\s*=\s*\d+\s*;",
    "print": r'cout\s*<<\s*".*?"\s*<<\s*\*?[A-Za-z_]\w*\s*<<\s*endl\s*;'
}

declared_vars = set()
pointers = set()
tokens = []


# ---------- Lexical Analysis ----------
def lexical_analysis(code):
    tokens.clear()
    for ln, line in enumerate(code.splitlines(), start=1):
        if any(re.fullmatch(p, line.strip()) for p in IGNORE_LINES):
            continue

        pos = 0
        while pos < len(line):
            if line[pos].isspace():
                pos += 1
                continue

            matched = False
            for name, pattern in TOKEN_REGEX:
                m = re.compile(pattern).match(line, pos)
                if m:
                    tokens.append((name, m.group()))
                    pos = m.end()
                    matched = True
                    break

            if not matched:
                return ("Lexical Error", f"line {ln}: invalid symbol '{line[pos]}'")

    return None


# ---------- Syntax + Semantic Analysis ----------
def compile_cpp(code):
    declared_vars.clear()
    pointers.clear()
    parse_tree = []

    lex = lexical_analysis(code)
    if lex:
        return lex

    for ln, line in enumerate(code.splitlines(), start=1):
        line = line.strip()
        if not line or any(re.fullmatch(p, line) for p in IGNORE_LINES):
            continue

        if re.fullmatch(GRAMMAR["decl"], line):
            var = re.findall(r"[A-Za-z_]\w*", line)[1]
            declared_vars.add(var)
            parse_tree.append("Declaration")
            continue

        if re.fullmatch(GRAMMAR["ptrdecl"], line):
            vars_ = re.findall(r"[A-Za-z_]\w*", line)
            if vars_[2] not in declared_vars:
                return ("Semantic Error", f"line {ln}: variable '{vars_[2]}' not declared")
            pointers.add(vars_[1])
            parse_tree.append("Pointer Declaration")
            continue

        if re.fullmatch(GRAMMAR["assign"], line):
            ptr = re.findall(r"[A-Za-z_]\w*", line)[0]
            if ptr not in pointers:
                return ("Semantic Error", f"line {ln}: '{ptr}' is not a pointer")
            parse_tree.append("Pointer Assignment")
            continue

        if re.fullmatch(GRAMMAR["print"], line):
            parse_tree.append("Print Statement")
            continue

        return ("Syntax Error", f"line {ln}: invalid structure")

    return ("OK", {"tokens": tokens, "parse_tree": parse_tree})
