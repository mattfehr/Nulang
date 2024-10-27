import copy
import json
import sys

DEF_NULL = '404'
DEF_TRUE = '1'
DEF_FALSE = '0'
DEF_TOKENIZER = '.'
DEF_COMMENT = '*'

class UserFunction:
    def __init__(self, parsed_lines, name, partial_params, lines):
        self.parsed_lines = parsed_lines
        self.return_val = DEF_NULL
        self.params = []
        self.params_ref = {}
        self.name = name
        self.lines = lines

        is_reference = False
        for partial_param in partial_params:
            if partial_param == '7':
                is_reference = True
            else:
                if is_reference:
                    self.params.append(partial_param)
                    self.params_ref[partial_param] = True
                else:
                    self.params.append(partial_param)
                    self.params_ref[partial_param] = False
                is_reference = False
        self.params_len = len(self.params)
        self.current_function = False

def eval_tokens_amount(user_functions, variables, tokens, available_functions, amount):
    values = []

    use_tokens = tokens

    while amount > 0:
        v1, unused_tokens = eval_tokens(user_functions, variables, use_tokens, available_functions)
        use_tokens = unused_tokens
        values.append(v1)
        amount -= 1

    return values, use_tokens

def bool_changer(v, r = False):
    if r:
        if v == DEF_TRUE:
            return True
        return False
    else:
        if v:
            return DEF_TRUE
        return DEF_FALSE

def assignment(user_functions, variables, tokens, available_functions):
    # -.var.eval

    if len(tokens) < 2:
        fatal_error('No value to assign.')

    # TODO verify valid variable name
    v, ut = eval_tokens_amount(user_functions, variables, tokens[1:], available_functions, 1)
    variables[tokens[0]] = v[0]
    return None, ut

def if_statement(user_functions, variables, tokens, available_functions):
    # 11.evalB

    return eval_tokens(user_functions, variables, tokens, available_functions)

def elif_statement(user_functions, variables, tokens, available_functions):
    # 12.evalB

    return eval_tokens(user_functions, variables, tokens, available_functions)

def print_func(user_functions, variables, tokens, available_functions):
    # 947.item

    r, ut = eval_tokens(user_functions, variables, tokens, available_functions)
    if len(ut) != 0:
        fatal_error(f'Unused code after print: {".".join(ut)}')

    if isinstance(r, list):
        print('/*', end='')
        for rv in r:
            print(rv, end='.')
        print('*/')
    else:
        print(r)

def length_func(_user_functions, variables, tokens, _available_functions):
    # 138.var

    var_val = tokens[0]
    return len(variables[var_val]), tokens[1:]

def index_at(user_functions, variables, tokens, available_functions):
    # 148.item

    var_val = tokens[0]
    idx, ut = eval_tokens(user_functions, variables, tokens[1:], available_functions)
    return variables[var_val][int(idx)], ut

def uf_return(user_functions, variables, tokens, available_functions):
    # 148.item

    for uf_name in user_functions:
        actual_obj = user_functions[uf_name]
        if actual_obj.current_function:
            val, ut = eval_tokens(user_functions, variables, tokens, available_functions)
            actual_obj.return_val = val

def index_set(user_functions, variables, tokens, available_functions):
    # 148.item

    var_val = tokens[0]
    vals, ut = eval_tokens_amount(user_functions, variables, tokens[1:], available_functions, 2)
    variables[var_val][int(vals[0])] = vals[1]
    return None, ut

def gt(user_functions, variables, tokens, available_functions):
    # ++/.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return bool_changer(int(vals[0]) > int(vals[1])), ut

def gte(user_functions, variables, tokens, available_functions):
    # +//.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return bool_changer(int(vals[0]) >= int(vals[1])), ut

def lt(user_functions, variables, tokens, available_functions):
    # --/.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return bool_changer(int(vals[0]) < int(vals[1])), ut

def lte(user_functions, variables, tokens, available_functions):
    # -//.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return bool_changer(int(vals[0]) <= int(vals[1])), ut

def equality(user_functions, variables, tokens, available_functions):
    # ///.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return bool_changer(int(vals[0]) == int(vals[1])), ut

def not_equals(user_functions, variables, tokens, available_functions):
    # /-/.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return bool_changer(int(vals[0]) != int(vals[1])), ut

def and_comp(user_functions, variables, tokens, available_functions):
    # 888.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return bool_changer(bool_changer(vals[0], r=True) and bool_changer(vals[1], r=True)), ut

def or_comp(user_functions, variables, tokens, available_functions):
    # 111.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return bool_changer(bool_changer(vals[0], r=True) or bool_changer(vals[1], r=True)), ut

def add(user_functions, variables, tokens, available_functions):
    # ++.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return str(int(vals[0]) + int(vals[1])), ut

def sub(user_functions, variables, tokens, available_functions):
    # --.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return str(int(vals[0]) - int(vals[1])), ut

def division(user_functions, variables, tokens, available_functions):
    # //.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return str(int(vals[0]) // int(vals[1])), ut

def multiply(user_functions, variables, tokens, available_functions):
    # **.eval.eval

    vals, ut = eval_tokens_amount(user_functions, variables, tokens, available_functions, 2)
    return str(int(vals[0]) * int(vals[1])), ut

indentation = {
    '00': lambda x: x,
    '88': lambda x: x,
    '11': if_statement,
    '12': elif_statement,
    '22': lambda x: x,
    '72': lambda x: x,
}

reserved_functions = {
    # special
    '-': assignment,
    '947': print_func,
    '138': length_func,
    '148': index_at,
    '158': index_set,
    '888': and_comp,
    '111': or_comp,
    '27': uf_return,

    # comparison
    '++/': gt,
    '+//': gte,
    '--/': lt,
    '-//': lte,
    '///': equality,
    '/-/': not_equals,

    # something  operators
    '++': add,
    '--': sub,
    '//': division,
    '**': multiply,
}

data_types = {
    '/': '/',  # literal number
    '/-': '-/',  # ascii string
    '/*': '*/',  # list
}

def eval_data_type(tokens):
    end = tokens[1:].index(data_types[tokens[0]])
    v = tokens[1:end + 1]
    unused_tokens = tokens[end + 2:]

    if tokens[0] == '/-':
        vn = ''
        v = v[0]
        for ci in range(len(v) // 3):
            vn += chr(int(v[ci * 3:ci * 3 + 3]))
        v = vn
    elif tokens[0] == '/*':

        avs = []

        list_tokens = v
        while list_tokens:
            av, no_ut = eval_data_type(list_tokens)
            list_tokens = no_ut
            avs.append(av)
        v = avs
    else:
        v = v[0]

    return v, unused_tokens

def eval_tokens(user_functions, variables, tokens, available_functions):

    v = None
    unused_tokens = tokens[1:]

    # functions
    if tokens[0] in available_functions:
        v, unused_tokens = available_functions[tokens[0]](user_functions, variables, tokens[1:], available_functions)

    # variables
    elif tokens[0] in variables:
        v = variables[tokens[0]]

    elif tokens[0] in data_types:
        v, unused_tokens = eval_data_type(tokens)

    elif tokens[0] == DEF_COMMENT:
        unused_tokens = []

    elif tokens[0] in user_functions:

        uf_obj = user_functions[tokens[0]]
        uf_obj.current_function = True
        uf_vars = {DEF_NULL: 'null'}
        vals, ut = eval_tokens_amount(user_functions, variables, tokens[1:], available_functions, uf_obj.params_len)
        for k, val in enumerate(vals):
            if uf_obj.params_ref[uf_obj.params[k]]:
                uf_vars[uf_obj.params[k]] = val
            else:
                uf_vars[uf_obj.params[k]] = copy.deepcopy(val)
        eval_lines(user_functions, uf_vars, uf_obj.lines, uf_obj.parsed_lines)
        v = uf_obj.return_val
        uf_obj.current_function = False

    else:
        fatal_error(f'Syntax Error:\n{".".join(tokens)}')

    return v, unused_tokens

def eval_lines(user_functions, variables, all_lines, parsed_lines):
    check_elif_else = False
    if_happened = False
    for line_num in parsed_lines:
        t = count_starting_chars(all_lines[line_num])
        tokenized = all_lines[line_num][t:].split(DEF_TOKENIZER)
        if parsed_lines[line_num] == {}:

            if DEF_COMMENT in tokenized:
                idx = tokenized.index(DEF_COMMENT)
                tokenized = tokenized[:idx]

            if tokenized[0] in reserved_functions:
                reserved_functions[tokenized[0]](user_functions, variables, tokenized[1:], reserved_functions)

                if tokenized[0] == '27':
                    return '27'

            elif tokenized[0] in user_functions:

                uf_obj = user_functions[tokenized[0]]
                uf_obj.current_function = True
                uf_vars = {DEF_NULL: 'null'}
                vals, ut = eval_tokens_amount(user_functions, variables, tokenized[1:], reserved_functions, uf_obj.params_len)
                for k, val in enumerate(vals):
                    if uf_obj.params_ref[uf_obj.params[k]]:
                        uf_vars[uf_obj.params[k]] = val
                    else:
                        uf_vars[uf_obj.params[k]] = copy.deepcopy(val)
                eval_lines(user_functions, uf_vars, uf_obj.lines, uf_obj.parsed_lines)
                uf_obj.current_function = False

            else:
                fatal_error(f'Failed to interpret line: {".".join(tokenized)}')

        else:
            if tokenized[0] == '11':
                if_eval, ut = indentation[tokenized[0]](user_functions, variables, tokenized[1:], reserved_functions)
                if if_eval == DEF_TRUE:
                    pc = eval_lines(user_functions, variables, all_lines, parsed_lines[line_num])
                    if pc == '27':
                        return '27'
                else:
                    check_elif_else = True
                if_happened = True

            elif tokenized[0] == '12':
                if check_elif_else:
                    if_eval, ut = indentation[tokenized[0]](user_functions, variables, tokenized[1:], reserved_functions)
                    if if_eval == DEF_TRUE:
                        pc = eval_lines(user_functions, variables, all_lines, parsed_lines[line_num])
                        if pc == '27':
                            return '27'
                        check_elif_else = False
                elif not if_happened:
                    fatal_error('Incorrect elif')

            elif tokenized[0] == '22':
                if check_elif_else:
                    pc = eval_lines(user_functions, variables, all_lines, parsed_lines[line_num])
                    if pc == '27':
                        return '27'
                elif not if_happened:
                    fatal_error('Incorrect else')

            elif tokenized[0] == '88':

                if_eval, ut = eval_tokens(user_functions, variables, tokenized[1:], reserved_functions)

                while if_eval == DEF_TRUE:
                    pc = eval_lines(user_functions, variables, all_lines, parsed_lines[line_num])
                    if pc == '27':
                        return '27'
                    if_eval, ut = eval_tokens(user_functions, variables, tokenized[1:], reserved_functions)

            elif tokenized[0] == '00':
                _, ut = eval_tokens(user_functions, variables, tokenized[1:], reserved_functions)

                condition, func_call_tokens = eval_tokens(user_functions, variables, ut, reserved_functions)

                while condition == DEF_TRUE:
                    pc = eval_lines(user_functions, variables, all_lines, parsed_lines[line_num])
                    if pc == '27':
                        return '27'
                    eval_tokens(user_functions, variables, func_call_tokens, reserved_functions)
                    condition, _ = eval_tokens(user_functions, variables, ut, reserved_functions)
            elif tokenized[0] == '72':
                # uf_tup:
                # 0 - params
                # 1 - parsed lines
                # 2 - all lines
                # 3 - return val
                uf_obj = UserFunction(parsed_lines[line_num], tokenized[1], tokenized[2:], all_lines)
                user_functions[tokenized[1]] = uf_obj
                # user_functions[tokenized[1]] = (tokenized[2:], parsed_lines[line_num], all_lines, DEF_NULL)

def fatal_error(output):
    print(output)
    exit(0)

def count_starting_chars(loc):
    count = 0
    for c in loc:
        if c == DEF_TOKENIZER:
            count += 1
        else:
            break
    return count

def apply_nested(pl, nests, ln):
    if len(nests) > 0:
        apply_nested(pl[nests[0]], nests[1:], ln)
    else:
        pl[ln] = {}

def main():
    if len(sys.argv) != 2:
        fatal_error(f'The only valid argument is the file you want to open, you provided {len(sys.argv)}.')

    try:
        entire_raw_code = open(sys.argv[1]).read()
        lines = entire_raw_code.split('\n')

        variables = {DEF_NULL: 'null'}
        user_functions = {}
        parsed_lines = {}

        nested = []

        for i, line in enumerate(lines):

            if line == '':
                continue
            if line.startswith(DEF_COMMENT):
                continue

            token_count = count_starting_chars(line)

            if token_count > len(nested):
                fatal_error('Bad indent.')

            elif token_count < len(nested):
                for _ in range(len(nested) - token_count):
                    nested.pop()

            line = line[token_count:]
            apply_nested(parsed_lines, nested, i)
            simple_tokens = line.split(DEF_TOKENIZER)
            if simple_tokens[0] in indentation:
                nested.append(i)

        eval_lines(user_functions, variables, lines, parsed_lines)

    except FileNotFoundError:
        fatal_error(f'Could not open the file {sys.argv[1]}.')
    except Exception as e:
        print('An error occurred.')

if __name__ == '__main__':
    main()
