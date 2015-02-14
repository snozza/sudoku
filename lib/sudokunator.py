from itertools import product

class Sudoku:

    def solver(self, size, grid):

        Row, Col = size
        Total = Row * Col
        ProbSet = ([("row-col", row_col) for row_col in product(range(Total), range(Total))] +
                    [("row-num", row_num) for row_num in product(range(Total), range(1, Total + 1))] +
                    [("col-num", col_num) for col_num in product(range(Total), range(1, Total + 1))] +
                    [("box-num", box_num) for box_num in product(range(Total), range(1, Total + 1))])
        Collection = dict()

        for row, col, num in product(range(Total), range(Total), range(1, Total + 1)):
            box = (row // Row) * Row + (col // Col)
            Collection[(row, col, num)] = [
                ("row-col", (row, col)),
                ("row-num", (row, num)),
                ("col-num", (col, num)),
                ("box-num", (box, num))]

        ProbSet, Collection = self.cover(ProbSet, Collection)
        for i, row in enumerate(grid):
            for j, num in enumerate(row):
                if num:
                    self.select(ProbSet, Collection, (i, j, num))

        for solution in self.solve(ProbSet, Collection, []):
            for (row, col, num) in solution:
                grid[row][col] = num
            yield grid

    def cover(self, ProbSet, Collection):
        ProbSet = {j: set() for j in ProbSet}
        for i, row in Collection.items():
            for j in row:
                print(ProbSet[j])
                ProbSet[j].add(i)
        return ProbSet, Collection

    def solve(self, ProbSet, Collection, solution):
        if not ProbSet:
            yield list(solution)
        else:
            c = min(ProbSet, key=lambda c: len(ProbSet[c]))
            for r in list(ProbSet[c]):
                solution.append(r)
                cols = self.select(ProbSet, Collection, r)
                for s in self.solve(ProbSet, Collection, solution):
                    yield s
                self.deselect(ProbSet, Collection, r, cols)
                solution.pop()

    def select(self, ProbSet, Collection, r):
        cols = []
        for j in Collection[r]:
            for i in ProbSet[j]:
                for k in Collection[i]:
                    if k != j:
                        ProbSet[k].remove(i)
            cols.append(ProbSet.pop(j))
        return cols

    def deselect(self, ProbSet, Collection, r, cols):
        for j in reversed(Collection[r]):
            ProbSet[j] = cols.pop()
            for i in ProbSet[j]:
                for k in Collection[i]:
                    if k != j:
                        ProbSet[k].add(i)

if __name__ == "__main__":
    sud = Sudoku()
    grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    
    for i in sud.solver((3, 3), grid):
        print(*i, sep='\n')
