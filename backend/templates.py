import re

class SimpleTemplate:
    var_pattern = re.compile(r'{{\s*(\w+)\s*}}')
    tag_pattern = re.compile(r'{%\s*(\w+)(?:\s+(.*?))?\s*%}')

    def __init__(self, template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def render(self, context):
        output = []
        stack = []
        skip_line = False

        def eval_expr(expr):
            try:
                return eval(expr, {}, context)
            except Exception:
                return False

        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            tag_match = self.tag_pattern.search(line)

            if tag_match:
                tag = tag_match.group(1)
                expr = tag_match.group(2)

                if tag == 'if':
                    condition = eval_expr(expr)
                    stack.append(('if', condition))
                    skip_line = not condition

                elif tag == 'else':
                    if not stack or stack[-1][0] != 'if':
                        raise SyntaxError("Unexpected else without if")
                    prev_condition = stack.pop()[1]
                    stack.append(('if', not prev_condition))
                    skip_line = not stack[-1][1]

                elif tag == 'endif':
                    if not stack or stack[-1][0] != 'if':
                        raise SyntaxError("Unexpected endif without if")
                    stack.pop()
                    skip_line = False if not stack else not stack[-1][1]

                elif tag == 'for':
                    var_iter = expr.split(' in ')
                    if len(var_iter) != 2:
                        raise SyntaxError("Malformed for tag")
                    var_name = var_iter[0].strip()
                    iterable = eval_expr(var_iter[1].strip())
                    if not hasattr(iterable, '__iter__'):
                        iterable = []
                    stack.append(('for', var_name, iterable, 0))
                    skip_line = False

                elif tag == 'endfor':
                    if not stack or stack[-1][0] != 'for':
                        raise SyntaxError("Unexpected endfor without for")
                    _, var_name, iterable, idx = stack[-1]
                    idx += 1
                    if idx < len(iterable):
                        stack[-1] = ('for', var_name, iterable, idx)
                        for_back = i
                        while for_back > 0:
                            if self.tag_pattern.search(self.lines[for_back]):
                                t = self.tag_pattern.search(self.lines[for_back]).group(1)
                                if t == 'for':
                                    break
                            for_back -= 1
                        i = for_back
                        context[var_name] = iterable[idx]
                    else:
                        stack.pop()
                        skip_line = False if not stack else False
                    i += 1
                    continue
                else:
                    pass

                i += 1
                continue

            if skip_line:
                i += 1
                continue


            def replace_var(m):
                var_name = m.group(1)
                return str(context.get(var_name, ''))

            rendered_line = self.var_pattern.sub(replace_var, line)
            output.append(rendered_line)
            i += 1

        return ''.join(output)
