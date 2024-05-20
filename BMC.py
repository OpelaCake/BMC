import aiger
from pysat.solvers import Minisat22
from aiger_cnf import aig2cnf

from Aiger2Model import aiger_to_cnf
def load_aiger_and_check(file_path):
    # 载入 AIGER 文件
    aig = aiger.load(file_path)
    print(aig)
    # 使用 py-aiger 提供的接口转换为CNF
    cnf = aig2cnf(aig)

    # 初始化 SAT 求解器
    solver = Minisat22()

    # 添加 CNF 公式到 SAT 求解器
    for clause in cnf.clauses:
        solver.add_clause(clause)

    # AIGER文件中最后的输出变量通常是我们关注的属性，检查是否可满足
    output_var = cnf.outputs[0][1]  # 获取输出变量对应的CNF变量编号

    # 检查该输出是否可能为 True
    # 我们添加该变量为正的假设，看看是否有解
    result = solver.solve(assumptions=[output_var])

    # 清理并关闭求解器
    solver.delete()

    return result

if __name__ == "__main__":
    # 测试我们的函数
    file_path = './aiger-safety-properties/traffic-light/traffic-light-cycle-prescale-bits-0.aag'  # 替换为你的 AIGER 文件路径
    unsafe_possible = load_aiger_and_check(file_path)

    if unsafe_possible:
        print("系统可能进入不安全状态！")
    else:
        print("系统不会进入不安全状态。")

