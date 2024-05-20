import os


from Aiger2Model import parse_aiger, aiger_to_cnf, cnf_to_string, write_cnf_file



input_folder = "aiger-safety-properties"  # 存放 AIGER 文件的文件夹
output_file = "test_results.txt"  # 用于保存测试结果的文件

def solve_sat(cnf_clauses):
    from pysat.solvers import Minisat22
    
    with Minisat22() as solver:
        for clause in cnf_clauses:
            solver.add_clause(clause)
        return solver.solve()


def list_files_recursive(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path
def main():

    # 遍历文件夹中的所有文件
    with open(output_file, 'w') as f_out:
        for file_name in list_files_recursive(input_folder):
            if file_name.endswith(".aag"):
                with open(file_name,'r') as f_in:
                    lines = f_in.readlines()
                try:
                    num_inputs, num_latches, inputs, outputs, latches, and_gates = parse_aiger(lines)
                except Exception as e:
                    print(e)
                    continue

                cnf_clauses = aiger_to_cnf(num_inputs, num_latches, inputs, outputs, latches, and_gates)
                cnf_string = cnf_to_string(cnf_clauses)
                cnf_file_path = file_name.replace(".aag", ".cnf").replace("aiger-safety-properties", "cnf-files")
                write_cnf_file(cnf_string, cnf_file_path)
                print(f"Solving {cnf_file_path}...")
                
                try:
                    return_code = solve_sat(cnf_clauses)
                except Exception as e:
                    print(f"Error occurred while solving {file_name}: {e}")
                    return_code = None
                print(  f"{file_name}: {return_code}")
                print(lines[-1])
                if "UNSATISFIABLE" in lines[-1]:
                    satisfiable = False
                elif "SATISFIABLE" in lines[-1]:
                    satisfiable = True
                else:
                    satisfiable = None
                if satisfiable == return_code:
                    f_out.write(f"{file_name}: test OK\n")
                elif satisfiable is not None and return_code is not None:
                    f_out.write(f"{file_name}: test Failed\n")
                else:    
                    f_out.write(f"{file_name}: UNKNOWN\n")


if __name__ == "__main__":
    main()

