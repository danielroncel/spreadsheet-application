import Mean, Min, Max, Sum

class PostfixEvaluator:
    def __init__(self, a):
        self.a = a
        self.priorities = {
            "(":0,
            ")":3,
            "+":1,
            "-":1,
            "*":2,
            "/":2,
            "SUM":2,
            "MIN":2,
            "MAX":2,
            "MEAN":2
        }

    def reorder_tokens(self, tokens): 
        pass
    
    def generate_postfix_expression(self, tokens): 
        stack = []
        for els in tokens:
            pass
            
    
    def evaluate_postfix_expression(self, postfix): 
        stack = []
        for el in postfix:
            if type(el) == str:
                val = eval(str(stack.pop())+el+str(stack.pop()))
                stack.append(val)
            else: stack.append(el)
        return stack.pop()

formula = [3,4,'*']
tokenizer = PostfixEvaluator('a')
tokens = tokenizer.evaluate_postfix_expression(formula)
print(tokens)