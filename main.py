from IOManager.FileManager import FileManager
from Solve.Solver import Solver

if __name__ == '__main__':
    fileName = 'Files\\hard_02.txt'
    fileManager = FileManager(fileName)
    v, graph = fileManager.get_data()
    solver = Solver(fileName)
    solver.solve(graph)