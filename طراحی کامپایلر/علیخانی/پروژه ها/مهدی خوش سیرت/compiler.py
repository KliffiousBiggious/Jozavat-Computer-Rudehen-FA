# ============================================
# Educational C++ Compiler – 3D Array Project
# Student: Mehdi Khoshseirat
# Course: Compiler Design
# ============================================

import re

TOKENS_DEF = [
    ("KEYWORD", r"\b(int|for|cout|cin|main)\b"),
    ("NUMBER", r"\b\d+\b"),
    ("STRING", r"\".*?\""),
    ("OPERATOR", r"<<|>>|\+\+|=|<"),
    ("IDENTIFIER", r"[A-Za-z_]\w*"),
    ("SYMBOL", r"[\[\]\(\)\{\};]")
]

tokens = []
parse_tree = []


# ---------- Lexical Analysis ----------
def lexical_analysis(lines):
    tokens.clear()
    for ln, line in enumerate(lines, 1):

        # remove strings temporarily
        temp = re.sub(r"\".*?\"", "", line)

        if re.search(r"[^A-Za-z0-9_\s\[\]\(\)\{\};<>=+]", temp):
            return ("Lexical Error", f"line {ln}: invalid character")

        for ttype, pattern in TOKENS_DEF:
            for m in re.finditer(pattern, line):
                tokens.append((ttype, m.group()))

    return None


# ---------- Syntax + Semantic Analysis ----------
def compile_cpp(code):
    parse_tree.clear()
    lines = code.splitlines()

    lex = lexical_analysis(lines)
    if lex:
        return lex

    joined = "\n".join(lines)

    # main
    if not re.search(r"int\s+main\s*\(\s*\)\s*\{", joined):
        return ("Syntax Error", "main function missing")
    parse_tree.append("Main Function")

    # array declaration
    arr = re.search(r"int\s+([A-Za-z_]\w*)\s*\[\d+\]\[\d+\]\[\d+\]\s*;", joined)
    if not arr:
        return ("Syntax Error", "3D array declaration missing")
    arr_name = arr.group(1)
    parse_tree.append("3D Array Declaration")

    # cout
    if not re.search(r'cout\s*<<\s*".*?"\s*;', joined):
        return ("Syntax Error", "cout statement missing")
    parse_tree.append("Cout Statement")

    # for loops
    fors = re.findall(
        r"for\s*\(\s*int\s+([A-Za-z_]\w*)\s*=\s*\d+\s*;\s*\1\s*<\s*\d+\s*;\s*\+\+\1\s*\)",
        joined
    )
    if len(fors) != 3:
        return ("Syntax Error", "exactly three nested for loops required")
    parse_tree.append("For Loop i")
    parse_tree.append("For Loop j")
    parse_tree.append("For Loop k")

    # cin
    cin = re.search(
        rf"cin\s*>>\s*{arr_name}\s*\[\s*{fors[0]}\s*\]\s*"
        rf"\[\s*{fors[1]}\s*\]\s*\[\s*{fors[2]}\s*\]\s*;",
        joined
    )
    if not cin:
        return ("Semantic Error", "cin statement does not match array or loop variables")
    parse_tree.append("Cin Statement")

    return ("OK", {"tokens": tokens, "parse_tree": parse_tree})
