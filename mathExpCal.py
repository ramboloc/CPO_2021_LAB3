from math import *

# Operation level
operators = ['+', '-', '*', '/', '(', ')', ',']
op_levels = {'+': 1, '-': 1, '*': 8, '/': 8, '(': 0}


def negative_test(f):
    def test(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError:
            print('Wrong Expression! Please check the expression!')

    return test


class MathExpression(object):
    def __init__(self, formula='0'):
        self.formula = formula  # origin formula
        self.conv_form = []  # Different versions of formulas
        self.values = dict()

    def RPN(self):
        """ convert origin formula to RPN"""
        # clean the blank
        ori_form = self.formula.replace(' ', '')

        # operator stack
        op_stack = list()
        flag_long_num = 0

        long_str = ''
        flag_long_str = 0

        for index, i in enumerate(ori_form):
            # 1. int float   2.str include operators  3.seperator:, ()

            # 1 pop the intergers and float into stack
            if ((i >= '0') and (i <= '9')) or i == '.':
                if flag_long_num == 0:
                    self.conv_form.append(i)
                    flag_long_num = 1
                else:
                    self.conv_form[-1] = self.conv_form[-1] + i
                continue

            flag_long_num = 0

            # 2. pop the str into stack
            # if pre is a str
            if flag_long_str == 1:
                if i not in operators:
                    long_str += i
                    continue
                # deal the operators between two elements
                # '+', '-', '*', '/'
                else:
                    if len(long_str) == 1:
                        self.conv_form.append(long_str)
                    else:
                        op_stack.append(long_str)
                    flag_long_str = 0

            if (i >= 'a') and (i <= 'z'):
                long_str = i
                flag_long_str = 1
                continue

            # 3. (,)     
            if i == ',':
                continue

            if len(op_stack) == 0:
                op_stack.append(i)
                continue

            if i == '(':
                op_stack.append(i)
                continue

            if i == ')':
                # The expressions in brackets operate first, and the () is not needed in the conv_form
                while op_stack[-1] != '(':
                    self.conv_form.append(op_stack.pop(-1))
                op_stack.pop(-1)
                # pop special operators like sin cos func
                if (len(op_stack) != 0) and (op_stack[-1] not in operators):
                    self.conv_form.append(op_stack.pop(-1))
                continue

            # continue the str operation, the '+', '-', '*', '/', Identified, but not yet used
            while len(op_stack) != 0 and op_levels[op_stack[-1]] >= op_levels[i]:
                self.conv_form.append(op_stack.pop(-1))
            op_stack.append(i)

        if flag_long_str == 1:
            self.conv_form.append(long_str)

        while len(op_stack) != 0:
            self.conv_form.append(op_stack.pop(-1))

    @negative_test
    def calc(self, **kwargs):
        stack = list()
        self.values = kwargs
        # e.g.:（3+4）*5-6 -> 34+5*6-
        for i in self.conv_form:
            if i == 'sin':
                stack.append(sin(stack.pop(-1)))
            elif i == 'cos':
                stack.append(cos(stack.pop(-1)))
            elif i == 'tan':
                stack.append(tan(stack.pop(-1)))
            elif i == '+':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left + right)
            elif i == '-':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left - right)
            elif i == '*':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left * right)
            elif i == '/':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left / right)
            elif i == 'log':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(log(left, right))
            elif i == 'pow':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(pow(left, right))

            elif i not in self.values.keys():
                stack.append(float(i))
            elif len(i) == 1:
                stack.append(self.values[i])
            else:
                # the values before operate push into the stack
                f = self.values[i]
                args_nums = f.__code__.co_argcount

                dic = dict()
                for j in range(args_nums):
                    dic[j] = stack.pop(-1)
                v = f(*dic.values())
                stack.append(v)

        return stack.pop(-1)

    # the dot will output to a file
    @negative_test
    def visualize(self, num):
        res = list()
        res.append('digraph G {')
        res.append(' rankdir=BT;')

        for i, n in enumerate(self.conv_form):
            res.append(' n_{}[label="{}"];'.format(i, n))

        index = len(self.conv_form)

        stack = list()
        for i, n in enumerate(self.conv_form):
            if n in ['sin', 'cos', 'tan']:
                cur = stack.pop(-1)
                res.append('{} -> n_{};'.format(cur, i))
                stack.append('n_{}'.format(i))
            elif n in operators or i in ['log', 'pow']:
                cur1 = stack.pop(-1)
                cur2 = stack.pop(-1)
                res.append('{} -> n_{};'.format(cur1, i))
                res.append('{} -> n_{};'.format(cur2, i))
                stack.append('n_{}'.format(i))
            elif n not in self.values.keys():
                stack.append('n_{}'.format(i))
            elif len(n) == 1:
                res.append(' n_{}[label="{}"];'.format(index, self.values[n]))
                res.append('n_{} -> n_{};'.format(index, i))
                index += 1
                stack.append('n_{}'.format(i))
            else:
                f = self.values[n]
                args_nums = f.__code__.co_argcount
                for j in range(args_nums):
                    cur = stack.pop(-1)
                    res.append('{} -> n_{};'.format(cur, i))
                stack.append('n_{}'.format(i))
        res.append('}')
        file = open('pic%d.dot' % num, 'w')
        file.write("\n".join(res))
