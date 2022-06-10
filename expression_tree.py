import logging

from graphviz import Digraph  # type: ignore


def arg_type(argType):
    def trace(func):
        def traced(*args, **kwargs):
            length = len(args)
            for k, v in argType.items():
                if k < length:
                    p = args[k]
                    if not isinstance(p, v):
                        logging.error("The arg %s should be %s,"
                                      "but it's %s now!"
                                      % (str(p), type(v()), type(p)))
                else:
                    if isinstance(kwargs, v):
                        pass
            try:
                res = func(*args, **kwargs)
            finally:
                logging.info("{} FINISH".format(func.__name__))
            return res
        return traced
    return trace


class Node:
    def __init__(self, name, pos, neg_mark=False, function=None):
        self.sign = -1 if neg_mark else 1
        self.pos = pos
        self.label = name
        if neg_mark and function is None:
            self.label = '-' + self.label
        self.name = name
        self.function = function
        self.arg_num = function.__code__.co_argcount if function else None
        self.value = None
        try:
            self.value = float(self.name)
        except ValueError:
            pass
        self.next = []

    def get_priority(self):
        if self.name in ['+', '-']:
            return 1
        elif self.name in ['*', '/']:
            return 2
        else:
            return 3


class ExpressTree(object):

    @arg_type({1: str, 2: dict})
    def __init__(self, input_string, **user_fun):
        self.__operators = {'+': lambda a, b: a + b, '-': lambda a, b: a - b,
                            '*': lambda a, b: a * b, '/': lambda a, b: a / b}

        self.__operators.update(user_fun)

        self.__input_string = input_string.strip().replace(' ', '')
        self.__node_list = self.__preprocess()

        self.__root = None

        if len(self.__node_list) > 0:
            self.__build_express_tree()

    def __preprocess(self):
        inp_str = self.__input_string
        ops = self.__operators
        res = []
        lng = len(inp_str)
        pos = 0
        mark_negative = False
        while pos < lng:
            if inp_str[pos].isalpha():
                start_pos = pos
                item_name = inp_str[pos]
                while pos + 1 < lng and inp_str[pos + 1].isalpha():
                    item_name += inp_str[pos + 1]
                    pos += 1
                fun = ops[item_name] if item_name in ops else None
                neg_mark = False
                if mark_negative:
                    neg_mark = True
                    mark_negative = False
                res.append(Node(item_name,
                                start_pos,
                                neg_mark=neg_mark,
                                function=fun))
            elif inp_str[pos].isdigit():
                start_pos = pos
                item_name = inp_str[pos]
                while pos + 1 < lng and \
                        (inp_str[pos + 1].isdigit() or
                         inp_str[pos + 1] == '.'):
                    item_name += inp_str[pos + 1]
                    pos += 1
                if len(item_name.split('.')) > 2:
                    logging.error(' Too many . symbols in '
                                  'numbers at position {0}'.format(start_pos))
                    return []
                neg_mark = False
                if mark_negative:
                    neg_mark = True
                    mark_negative = False
                res.append(Node(item_name, start_pos, neg_mark=neg_mark))
            elif inp_str[pos] == '-':
                if len(res) == 0 or res[-1].name \
                        in ['+', '-', '*', '/', '(', ',']:
                    if pos + 1 < lng and \
                            (inp_str[pos + 1].isalpha()
                             or inp_str[pos + 1].isdigit()):
                        mark_negative = True
                    else:
                        logging.error(' Negative sign does'
                                      ' not match at position{0}'.format(pos))
                        return []
                else:
                    fun = ops[inp_str[pos]] if inp_str[pos] in ops else None
                    res.append(Node(inp_str[pos], pos, function=fun))
            elif inp_str[pos] in ['(', ')', ',', '+', '*', '/']:
                fun = ops[inp_str[pos]] if inp_str[pos] in ops else None
                res.append(Node(inp_str[pos], pos, function=fun))
            else:
                logging.error(' Unrecognized character {0} at '
                              'position {1} '.format(inp_str[pos], pos))
                return []
            pos += 1
        return res

    def __build_express_tree(self):
        ops = self.__operators
        node_list = self.__node_list
        length = len(node_list)
        stack_node = []
        stack_op = []
        p = 0
        while p < length:
            token = node_list[p]
            if token.name == '(':
                stack_op.append(token)
            elif token.name in ops:
                while len(stack_op) > 0 and \
                        stack_op[-1].name in ops and \
                        token.get_priority() <= stack_op[-1].get_priority():
                    top_op = stack_op[-1]
                    if len(stack_node) < top_op.arg_num:
                        logging.error(
                            ' Insufficient number of parameters for'
                            ' function {0} at position {1}'.format(
                                top_op, top_op.pos))
                        return
                    for i in range(top_op.arg_num):
                        top_op.next.append(stack_node[-1])
                        stack_node.pop()
                    top_op.next = top_op.next[::-1]
                    stack_node.append(top_op)
                    stack_op.pop()
                stack_op.append(token)
            elif token.name == ',':
                while len(stack_op) > 0 and stack_op[-1].name != '(':
                    top_op = stack_op[-1]
                    if len(stack_node) < top_op.arg_num:
                        logging.error(
                            ' Insufficient number of parameters'
                            ' for function {0} at position {1}'.format(
                                top_op, top_op.pos))
                        return
                    for i in range(top_op.arg_num):
                        top_op.next.append(stack_node[-1])
                        stack_node.pop()
                    top_op.next = top_op.next[::-1]
                    stack_node.append(top_op)
                    stack_op.pop()
                if len(stack_op) == 0:
                    logging.error(' , in the'
                                  ' wrong place {0}'.format(token.pos))
                    return
            elif token.name == ')':
                while len(stack_op) > 0 and stack_op[-1].name != '(':
                    top_op = stack_op[-1]
                    if len(stack_node) < top_op.arg_num:
                        logging.error(
                            ' Insufficient number of parameters for'
                            ' function {0} at position {1}'.format(
                                top_op, top_op.pos))
                        return
                    for i in range(top_op.arg_num):
                        top_op.next.append(stack_node[-1])
                        stack_node.pop()
                    top_op.next = top_op.next[::-1]
                    stack_node.append(top_op)
                    stack_op.pop()
                if len(stack_op) == 0:
                    logging.error(' ) in the wrong'
                                  ' place {0}'.format(token.pos))
                    return
                stack_op.pop()
            else:
                stack_node.append(token)
            p += 1

        while len(stack_op) > 0:
            top_op = stack_op[-1]
            if len(stack_node) < top_op.arg_num:
                logging.error(
                    ' Insufficient number of parameters for'
                    ' function {0} at position {1}'.format(
                        top_op, top_op.pos))
                return
            for i in range(top_op.arg_num):
                top_op.next.append(stack_node[-1])
                stack_node.pop()
            top_op.next = top_op.next[::-1]
            stack_node.append(top_op)
            stack_op.pop()

        if len(stack_node) == 1:
            self.__root = stack_node[0]

    @arg_type({1: dict})
    def __call__(self, **kwargs):
        for v in kwargs.values():
            if type(v) is not float and type(v) is not int:
                logging.error(' parameter {0} is not a number'.format(v))
                return None

        self.__update_value(self.__root, arg=kwargs)
        if self.__root is None:
            return None
        return self.__root.value * self.__root.sign

    @arg_type({1: Node, 2: dict})
    def __update_value(self, node, arg):
        if node.function is None:
            if node.value is not None:
                return node.value * node.sign
            if node.name in arg:
                node.value = arg[node.name]
                return node.value * node.sign
            logging.error(' parameter {0} is not in input'.format(node.name))
            return None
        fun_arg = []
        for k in node.next:
            res = self.__update_value(k, arg)
            if res is None:
                return None
            fun_arg.append(res)
        node.value = node.function(*fun_arg)
        return node.value * node.sign

    def visualization(self):
        if self.__root is None:
            logging.warning(' Expression tree is not initialized.')
            return
        g = Digraph('express_tree', filename='express_tree.gv')

        idx = 0
        queue = [[self.__root, idx]]
        g.node(str(idx), label=self.__root.label)
        while len(queue) > 0:
            node, i = queue[0]
            del queue[0]
            for k in node.next:
                idx += 1
                g.node(str(idx), label=k.label)
                g.edge(str(i), str(idx))
                queue.append([k, idx])
        g.view()
