import aiger

def aiger_to_cnf(aig):
    clauses = []
    # Handling latches
    for latch in aig.latches:
        print(latch)
        state_var = latch[0]    # Latch's current state variable
        next_expr = latch[1]    # Expression for the next state

        # Map latch logic to CNF
        # Since `py-aiger` uses expressions, you might need to manually encode this
        # This example assumes a simple direct conversion which may need more sophisticated handling
        # For now, we will assume the expression provides a direct variable for simplicity
        next_var = next_expr.inputs[0]  # This may not be correct and needs more specific handling based on actual circuit logic
        clauses.append([-state_var, next_var])  # If state_var is true, then next_var must be true
        clauses.append([state_var, -next_var])  # If state_var is false, then next_var must be false

    # Convert AND gates
    for gate in aig.gates:
        output, inputs = gate[0], gate[1]
        input1, input2 = inputs
        # AND gate to CNF
        clauses.append([-input1, -input2, output])  # If both inputs are true, output is true
        clauses.append([input1, -output])           # If output is true, input1 must be true
        clauses.append([input2, -output])           # If output is true, input2 must be true

    return clauses
if __name__ == '__main__':
    # 读取 AIGER 文件
    circuit = aiger.load('./aiger-safety-properties/traffic-light/traffic-light-cycle-prescale-bits-0.aag')
    print(circuit)
    # 定义自动机的状态和转换
    transitions = {}
    for latch in circuit.latches:
        state = latch.input  # 触发器当前状态
        next_state_expr = latch.expr  # 下一个状态的表达式
        transitions[state] = next_state_expr

    # 可以进一步转换这些表达式为更具体的转换规则


