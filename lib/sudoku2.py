class Head:
    def __init__(self, col):
        self.col = col

    def insert(self):
        self.right.left = self.left.right = self

    def remove(self):
        self.left.right = self.right
        self.right.left = self.left

class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col

    def insert(self):
        self.down.up = self.up.down = self

    def remove(self):
        self.up.down = self.down
        self.down.up = self.up

class IterateNode:

    def __init__(self, node):
        self.curr = self.start = node

    def __iter__(self):
        return self

    def next(self):
        _next = self.move(self.curr)
        if _next == self.start:
            raise StopIteration
        else:
            self.curr = _next
            return _next

    def move(self):
        raise NotImplementedError

class IterateLeft (IterateNode):
    def move(self, node):
        return node.left

class IterateRight (IterateNode):
    def move(self, node):
        return node.right

class IterateDown (IterateNode):
    def move(self, node):
        return node.right

class IterateUp (IterateNode):
    def move(self, node):
        return node.down

class Matrix:

    def makeLeftRightLinks(self, srows):
        for srow in srows:
            n = len(srow)
            for j in range(n):
                srow[j].right = srow[(j + 1) % n]
                srow[j].left = srow[(j - 1 + n) % n]

    def makeUpDownLinks(self, scols):
        for scol in scols:
            n = len(scol)
            for i in range(n):
                scol[i].down = scol[(i + 1) % n]
                scol[i].up = scol[(i - 1 + n) % n]
                scol[i].head = scol[0]

    def __init__(self, mat):

        nrows = len(mat)
        ncols = len(mat[0])

        srow = [[ ] for _ in range(nrows)]
        heads = [Head(j) for j in range(ncols)]
        scol = [[head] for head in heads]

        self.head = Head(-1)
        heads = [self.head] + heads

        self.makeLeftRightLinks([heads])

        for i in range(nrows):
            for j in range(ncols):
                if mat[i][j] == 1:
                    node = Node(i, j)
                    scol[j].append(node)
                    srow[i].append(node)

        self.makeLeftRightLinks(srow)
        self.makeUpDownLinks(scol)

class Solver:

    def __init__(self, mat):
        self.solution = []
        self.smat = Matrix(mat)

    def cover(self, col):
        col.remove()
        for row in IterateDown(col):
            for cell in IterateRight(row):
                cell.remove()

    def uncover(self, col):
        for row in IterateUp(col):
            for cell in IterateLeft(row):
                cell.insert()
        col.attach()

    def solve(self):
        if (self.backtrack()):
            return self.solution
        return []

    def backtrack(self):
        col = self.smat.head.right

        print(col)

        if col == self.smat.head:
            return True

        if col.down == col:
            return False

        self.cover(col)
        print(self.smat)

        for row in IterateDown(col):

            for cell in IterateRight(row):
                self.cover(cell.head)

            print(self.smat)

            if self.backtrack():
                self.solution.append(row)
                return True

            for cell in IterateLeft(row):
                self.uncover(cell.head)

        self.uncover(col)

        return False

if __name__ == '__main__':
    grid = [[5,1,7,6,0,0,0,3,4],[2,8,9,0,0,4,0,0,0],[3,4,6,2,0,5,0,9,0],[6,0,2,0,0,0,0,1,0],[0,3,8,0,0,6,0,4,7],[0,0,0,0,0,0,0,0,0],[0,9,0,0,0,0,0,7,8],[7,0,3,4,0,0,5,6,0],[0,0,0,0,0,0,0,0,0]]
    sud = Solver(grid)
    print(sud.solve())
