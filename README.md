# CPO_LW - lab 3 - variant 1

In lab 3, *Basic Model of Computational*, variant 1 aims to
parse mathematical expressions by expression trees.

## Project structure

- `expression_tree.py` -- includes class `Node` with methods `__init__` and `get_priority`,
 class `ExpressTree` with methods `__init__`, `__preprocess`, `__build_express_tree`,
 `__update_value`, `__call__`, `visualization`,
 and function `arg_type` as a decorator for checking input datas.

- `expression_tree_test.py` -- unit tests for `expression_tree.py`.

## Features

- class `Node`:
  - `__init__`: Instantiate a node of expression tree
 (non-leaf - function; leaf - constant).
  - `get_priority`: Get the priority of function.

- class `ExpressTree`:
  - `__init__`: Create an expression tree.
  - `__preprocess`: Preprocessing the input string expression.
  - `__build_express_tree`: Building an expression tree
   according to the preprocessed string expression.
  - `__update_value`: Reducing the expression tree in a result (from leaves to root).
  - `__call__`: Input constants, reduce the expression.
  - `visualization`: Visualization the expression tree.

## Contribution

- Li Liquan (212320016@hdu.edu.cn)
  - GitHub repository created
  - implement classes `Node`, `ExpressTree`

- Wang Zimeng (1372178297@qq.com)
  - implement tests and input data control: class `TestExpressTree`, decorator `arg_type`.
  - write `README.md`

## Changelog

- 23.5.2022 11:55 -3
  - Wang Zimeng commits codes and `README.md`.
- 18.5.2022 19:40 -2
  - Li Liquan commits codes.
- 18.5.2022 19:13 -1
  - Build the project framework.

## Design notes

- Input type: string.
- In expression tree, functions are parsed as non-leaf nodes and constants as leave.
- Users can customize functions as non-leaf nodes of the expression tree.