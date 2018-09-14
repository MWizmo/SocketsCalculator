import socket

class Calculator:
    def __init__(self):
        self.error=''
        self.expression=''

    def priority(self,symbol):
        if (symbol.isdigit()):
            return 0
        elif (symbol =='('):
            return 1
        elif (symbol in ['+','-']):
            return 2
        elif (symbol in ['*','/']):
            return 3
        elif (symbol!=')'):
            return 4

    def TralslateToPolish(self,expression):
        stack = []
        string = ""
        output_string = []
        for i in range(0, len(expression)):
            symb = expression[i]
            if(self.priority(symb))==4:
                self.error='Некорректные символы во входной строке'
                continue
            if((symb=='-' and i==0)or(symb=='-' and expression[i-1]=='(')):
                string+=symb
            elif (symb == ' '): continue
            elif (self.priority(symb) == 0):
                string += symb
            else:
                if (string != ""):
                    output_string.append(string)
                    string = ""
                if (self.priority(symb) == 1):
                    stack.append(symb)
                else:
                    if (symb == ')'):
                        while (stack[-1] != '('):
                            output_string.append(stack.pop())
                        stack.pop()

                    elif (len(stack) == 0 or self.priority(stack[-1]) < self.priority(symb)):
                        stack.append(symb)
                    elif (self.priority(stack[-1]) >= self.priority(symb)):
                        while (self.priority(stack[-1]) >= self.priority(symb)):
                            output_string.append(stack.pop())
                            if(len(stack)==0):
                                stack.append(symb)
                                break
        if (string != ""):
            output_string.append(string)
        while(len(stack)>0):
            output_string.append(stack.pop())
        return output_string

    def Count(self,first,second,sign):
        if(sign=='+'):
            return float(first) + float(second)
        elif(sign=='-'):
            return float(first) - float(second)
        elif (sign == '*'):
            return float(first) * float(second)
        elif (sign == '/'):
            if(float(second)==0.0):
                return 'e'
            else:
                return float(first) / float(second)

    def Calculate(self,input_list):
        stack=[]
        if (self.error != ''):
            answer = 'There was some error while working calculator(' + self.error + '). Please, check your input data.'
            self.error = ''
            return answer
        for i in range(0,len(input_list)):
            element=input_list[i]
            if(element.isdigit() or(element[0]=='-' and len(element)>1)):
                stack.append(element)
            else:
                second_num=stack.pop()
                first_num=stack.pop()
                res=self.Count(first_num,second_num,element)
                if res=='e':
                    self.error='Divide by 0'
                    break
                else:
                    stack.append(res)
        if(self.error==''):
            return self.expression + ' = ' + str(stack[0])
        else:
            answer='There was some error while working calculator('+self.error+'). Please, check your input data.'
            self.error = ''
            return answer

sock = socket.socket()
sock.bind(('', 9000))
sock.listen(1)
calc=Calculator()
conn, addr = sock.accept()
print('connected:', addr)

while True:
    data = conn.recv(1024).decode('utf-8')
    if not data:
        continue
    calc.expression=data
    answer=calc.Calculate(calc.TralslateToPolish(data))
    conn.send(answer.encode('utf-8'))
