# SA Spade A * lab 2 * variant 2

## Laboratory work description

* Input language is a sting like a + 2 * sin(*0.3)*(b * c).
* Should support user*specific functions by passing something like {"foo": lambda x:x*42 } or by named arguments.
* Run*time error should be processed correctly.
* You should use the default Python logging module to make the interpreter work trans*parent.
* Visualization as a dataflow graph (see Fig. 5.3) and as a dataflow graph with trace annotation (see listing 1). A specific graph representation depends on your sub*variant.

## Project structure

* `math_expression_tree.py` ** includes class `MathExpression`
* `math_expression_tree_test.py` ** unit and PBT tests for classes and functions in `math_expression_tree.py`.

## Features

* `negative_test(expression)`:Judge whether the input formula is legal.
* `dot_to_png(num)`: Convert dot to png.
* `to_Postfix(self)`: Convert infix expression to suffix expression.
* `calculate(self, **kwargs)`: Evaluate the result of an expression.
* `visualize(self, num)`: Visualize expressions.

### Contribution summary for each group member: 

* Wu Bin
  * GitHub repository created
  * write `math_expression_tree.py`
  * solve bugs
* Li Jingwen -- writing README.md
  * write `math_expression_tree_test.py`
  * write `README.md`

## Changelog

* 12.6.2022 12:55 *3
  * Wu Bin commits codes.
* 18.5.2022 19:40 *2
  * Li Jingwen commits `README.md`.
* 18.5.2022 19:13 *1
  * Build the project framework.

## Design notes

* Input type: string
