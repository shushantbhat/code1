import heapq
import copy

N = 4

class Node:
    def __init__(self, x, y, assigned, parent):
        self.parent = parent
        self.pathCost = 0
        self.cost = 0
        self.workerID = x
        self.jobID = y
        self.assigned = copy.deepcopy(assigned)
        if y != -1:
            self.assigned[y] = True

class CustomHeap:
    def __init__(self):
        self.heap = []

    def push(self, node):
        heapq.heappush(self.heap, (node.cost, node))

    def pop(self):
        return heapq.heappop(self.heap)[1] if self.heap else None

def new_node(x, y, assigned, parent):
    return Node(x, y, assigned, parent)

def calculate_cost(cost_matrix, x, assigned):
    cost = 0
    available = [True] * N

    for i in range(x + 1, N):
        min_val, min_index = float('inf'), -1
        for j in range(N):
            if not assigned[j] and available[j] and cost_matrix[i][j] < min_val:
                min_index, min_val = j, cost_matrix[i][j]
        cost += min_val
        available[min_index] = False

    return cost

def print_assignments(min_node):
    if min_node.parent is None:
        return
    print_assignments(min_node.parent)
    print(f"Assign Worker {chr(min_node.workerID + ord('A'))} to Job {min_node.jobID}")

def find_min_cost(cost_matrix):
    pq = CustomHeap()
    root = new_node(-1, -1, [False] * N, None)
    pq.push(root)

    while True:
        min_node = pq.pop()
        i = min_node.workerID + 1

        if i == N:
            print_assignments(min_node)
            return min_node.cost

        for j in range(N):
            if not min_node.assigned[j]:
                child = new_node(i, j, min_node.assigned, min_node)
                child.pathCost = min_node.pathCost + cost_matrix[i][j]
                child.cost = child.pathCost + calculate_cost(cost_matrix, i, child.assigned)
                pq.push(child)

if __name__ == "__main__":
    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]
    optimal_cost = find_min_cost(cost_matrix)
    print(f"\nOptimal Cost is {optimal_cost}" if optimal_cost is not None else "\nNo optimal solution found.")
