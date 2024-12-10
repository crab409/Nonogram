import re
from random import sample
from typing import List, Tuple, Dict
import tkinter

solution_list: List[List[int]] = []

def valid(s: List[int], r: List[Tuple], c: List[Tuple]):
    s_all: List[int] = s.copy() + [-1]*(len(r)*len(c) - len(s))
    grid: Dict[int, List] = {}
    row: int = 0
    for i in range(0, len(s_all), len(c)):
        grid[row] = s_all[i:(i + len(c))]
        row += 1
    
    for row in grid.keys():
        row_sum_max = sum(r[row])
        row_sum_now = sum([1 if r == 1 else 0 for r in grid[row]])
        if row_sum_now > row_sum_max:
            return False
        
        sum_from_blank = sum([1 if r == -1 else 0 for r in grid[row]])
        if row_sum_now + sum_from_blank < row_sum_max:
            return False
        
        if sum_from_blank != 0:
            continue
        else:
            str_ = "".join([str(a) for a in grid[row]])
            groups = re.split('0+', str_)
            groups = [g for g in groups if g != '']
            group_sums = tuple([len(g) for g in groups])
            if group_sums != r[row]:
                return False
    
    for col in range(len(c)):
        col_values = []
        for row in grid.keys():
            col_values.append(grid[row][col])
        
        col_sum_max = sum(c[col])
        col_sum_now = sum([1 if c == 1 else 0 for c in col_values])
        if col_sum_now > col_sum_max:
            return False
        
        sum_from_blank = sum([1 if r == -1 else 0 for r in col_values])
        if col_sum_now + sum_from_blank < col_sum_max:
            return False

        if sum_from_blank != 0:
            continue
        else:
            str_ = "".join([str(a) for a in col_values])
            groups = re.split('0+', str_)
            groups = [g for g in groups if g != '']
            group_sums = tuple([len(g) for g in groups])
            if group_sums != c[col]:
                return False
    
    return True


def extend(row_args: List[Tuple], col_args: List[Tuple], partial_solution: List[int]):
    global solution_list  # 전역 변수 사용 선언
    solution_list = []  # extend 함수 호출 시마다 초기화

    def _extend(partial_solution: List[int]):
        if len(partial_solution) == len(row_args) * len(col_args):
            solution_list.append(partial_solution.copy())
            return

        for move in sample([0, 1], k=2):
            partial_solution.append(move)
            if not valid(partial_solution, row_args, col_args):
                partial_solution.pop()
                continue
            _extend(partial_solution)  # 재귀 호출
            partial_solution.pop()

    _extend(partial_solution)  # 내부 함수 호출
    return


def convert_to_2d(solution: List[int], row_args: List[Tuple], col_args: List[Tuple]) -> List[List[int]]:
    grid = []
    start_idx = 0
    for row in row_args:
        row_len = len(col_args)
        grid.append(solution[start_idx:start_idx + row_len])
        start_idx += row_len
    return grid

def load_hints(table_number) :
    file = open(f"tables/table{table_number}.txt", 'r')
    lines = file.readlines()

    rsi = lines.index('row_args:\n')
    csi = lines.index('col_args:\n')
    end = lines.index('end')

    row_arg = []
    for i in range(rsi+1, csi, 1) :
        data = tuple(map(int, lines[i].strip().split(',')))
        row_arg.append(data)

    col_arg = []
    for i in range(csi+1, end, 1) :
        data = tuple(map(int, lines[i].strip().split(',')))
        col_arg.append(data)

    return [row_arg,col_arg]

def load_answers(row_args, col_args) : 

    extend(row_args, col_args, [])

    grid = convert_to_2d(solution_list[0], row_args, col_args)

    return grid

def hints_to_str(row_args, col_args) :
    row_hints = []
    for line in row_args :
        str_line = ""
        for data in line : 
            str_line += f"{data} "
        row_hints.append(str_line.strip())
    
    col_hints = []
    for line in col_args :
        str_line = ""
        for data in line :
            str_line += f"{data}\n"
        col_hints.append(str_line.strip())
    
    return [row_hints, col_hints]

def count_solution(table) :
    print("fun.py: count_solution 매개변수 전달받음")
    for line in table :
        for data in line :
            print(data, end=' ')
        print()

    counter = 0

    for line in table :
        for data in line : 
            if(data == 1) :
                counter += 1

    return counter

def is_clear(board, solution_table) :
    newBoard = [
        [
            data for data in line
        ] for line in board
    ]
    print(newBoard)
    print(board)
    print(solution_table)


    for i in range(0, len(board), 1) : 
        for j in range(0, len(board[0]), 1) : 
            if(board[i][j] != solution_table[i][j]) : 
                return False
    return True

def load_size(table_number) : 
    file = open(f"tables/table{table_number}.txt", 'r')
    lines = file.readlines()

    rsi = lines.index("row_args:\n")
    csi = lines.index("col_args:\n")
    end = lines.index("end")

    row_count = csi - rsi - 1
    con_count = end - csi - 1 

    return (row_count, con_count)