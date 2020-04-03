class FileManager(object):

    def __init__(self, filename):
        self.__inputFile = filename
        file_data = filename.split('.')
        self.__outputFile = file_data[0] + '_solution.' + file_data[1]
        try:
            open(self.__outputFile, 'w')
        except FileNotFoundError:
            print('File not found')

    def get_data(self):
        if self.__inputFile == 'Files\\hardF.txt':
            return self.get_hard_data()
        try:
            with open(self.__inputFile) as file:
                graph = []
                file_lines = file.readlines()
                first_line_data = file_lines[0].split()
                V = int(first_line_data[0])
                for i in range(V):
                    line_data = file_lines[i + 1].split(',')
                    graph.append([])
                    for j in range(V):
                        graph[i].append(int(line_data[j].strip()))
                return V, graph
        except FileNotFoundError:
            print("File " + self.__inputFile + "not found.")

    def write_data(self, road, cost):
        try:
            with open(self.__outputFile, 'a') as file:
                file.write(str(len(road)) + '\n')
                for i in range(len(road)):
                    if i < len(road) - 1:
                        file.write(str(road[i]) + ',')
                    else:
                        file.write(str(road[i]) + '\n')
                file.write(str(cost) + '\n')
        except FileNotFoundError:
            print("File " + self.__outputFile + "not found.")

    def get_hard_data(self):
        try:
            with open(self.__inputFile) as file:
                graph = []
                V = 0
                file_lines = file.readlines()
                for line in file_lines:
                    line_data = line.split(' ')
                    for elem in line_data[:-1]:
                        elem = int(elem)
                        if elem > V:
                            V = elem
                for i in range(V):
                    graph.append([0 for i in range(V)])
                for line in file_lines:
                    line_data = line.split(' ')
                    x = int(line_data[0]) - 1
                    y = int(line_data[1]) - 1
                    cost = int(line_data[2])
                    graph[x][y] = cost
                    graph[y][x] = cost
                return V, graph
        except FileNotFoundError:
            print("File " + self.__inputFile + "not found.")
