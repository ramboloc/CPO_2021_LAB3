# CPO-lab3
Computational Process Organization lab3
## title: Mathematical expression
## laboratory work number: 1b

### variant description: Mathematical expression
• Input language is a sting like a + 2 - sin(-0.3)*(b - c).
• Should support user-specific functions by passing something like {"foo": lambda x:x*42 } or by named arguments.
• Run-time error should be processed correctly.
• You should use the default Python logging module to make the interpreter work trans-parent.
• Visualization as a dataflow graph (see Fig. 5.3) and as a dataflow graph with trace annotation (see listing 1). A specific graph representation depends on your sub-variant.

### Synopsis:
I use the RPN(suffix expression) to transfer the formula become easy to computation.
e.g.:（3+4）*5-6 -> 34+5*6-
RPN(Reverse Polish Notation):
There are no brackets in the Reverse Polish Notation. 
In the calculation, the first number before the operator is used as the right operand, and the second number is used as the left operand. 
The value obtained will continue to be put into the RPN.

### Contribution summary for each group member: 

Work by Zhou Wu Bin :

1. design the main mathematical code 

Work by Li Jingwen:

1. test, debug

##  descriptions of  modules
#### In MathExpression from mathExpCal
 def RPN： change the origin string into RPN string
 def calc: calculate the RPN string
 def visualize: generate the dot.source
 
#### In MathExpression from mathExpCal
We test +, -, *, /, sin, cos, tan, pow, log and func(), by some formulas.
Such as:
- cos(0)+tan(0.3)*sin(0)
- 19-14.21*20.91
- cos((3-a)*b)+func(c,d)/3
- a + 2 - sin(0.3)*(b - c)
......

### Conclusion
In this lab, we completed the string conversion to RPN, and successfully calculated the value of each formula.

We have completed the functions: +, -, *, /, sin, cos, tan, pow, log and can accept input functions: func().

Finally, we visualize the process of computation.
      