import ast
import math
import operator
import sys

from optparse import OptionParser


def evaluate(node):

    op_map = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitAnd: operator.and_,
        ast.BitXor: operator.xor,
    }

    func_map = {
        "log": math.log10,
        "exp": math.exp,
        "sqrt": math.sqrt,
        "factorial": math.factorial,
        "sin": math.sin,
        "cos": math.cos,
    }

    const_map = {
        "pi": math.pi,
        "e": math.e,
    }

    if isinstance(node, (list, tuple)):
        return [evaluate(sub_node) for sub_node in node]

    elif isinstance(node, str):
        return evaluate(ast.parse(node))

    elif isinstance(node, ast.Module):
        values = []
        for body in node.body:
            values.append(evaluate(body))
        if len(values) == 1:
            values = values[0]
        return values

    elif isinstance(node, ast.Expr):
        return evaluate(node.value)

    elif isinstance(node, ast.BinOp):
        left = evaluate(node.left)
        op = node.op
        right = evaluate(node.right)

        try:
            return op_map[type(op)](left, right)
        except KeyError:
            raise ValueError(
                "Operator %s not supported" % op.__class__.__name__)

    elif isinstance(node, ast.Call):
        func_name = node.func.id
        args = [evaluate(arg) for arg in node.args]

        try:
            return func_map[func_name](*args)
        except KeyError:
            raise ValueError("Function %s not supported" % func_name)

    elif isinstance(node, ast.Num):
        return node.n

    elif isinstance(node, ast.Name):
        try:
            return const_map[node.id]
        except KeyError:
            raise ValueError("Constant %s not supported" % node.id)

    raise TypeError("Unsupported operation: %s" % node.__class__.__name__)