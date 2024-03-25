import sys


class RideRequest:
    def __init__(self, rideIdentifier, estimatedCost, timeTaken):
        self.rideIdentifier = rideIdentifier
        self.estimatedCost = estimatedCost
        self.timeTaken = timeTaken

class MinHeapTree:
    def __init__(self):
        self.heap = []
    

    def parent_node(self, index):
        return (index - 1) // 2


    def left_child_node(self, index):
        return 2 * index + 1

    def right_child_node(self, index):
        return 2 * index + 2

    def has_left_child_node(self, index):
        return self.left_child_node(index) < len(self.heap)

    def has_right_child_node(self, index):
        return self.right_child_node(index) < len(self.heap)

    def exchange_nodes(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def up_heapify(self, index):
        while index > 0 and self.compare(self.heap[index], self.heap[self.parent_node(index)]):
            parent_node_index = self.parent_node(index)
            self.exchange_nodes(index, parent_node_index)
            index = parent_node_index

    def down_heapify(self, index):
        while self.has_left_child_node(index):
            min_child_index = self.left_child_node(index)
            if self.has_right_child_node(index) and self.compare(self.heap[self.right_child_node(index)], self.heap[self.left_child_node(index)]):
                min_child_index = self.right_child_node(index)

            if self.compare(self.heap[index], self.heap[min_child_index]):
                break

            self.exchange_nodes(index, min_child_index)
            index = min_child_index

    def insertion(self, ride):
        self.heap.append(ride)
        self.up_heapify(len(self.heap) - 1)
    
    def extract_min_node(self):
        if not self.heap:
            return None
        min_ride = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.down_heapify(0)
        return min_ride

    def compare(self, ride_1, ride_2):
        if ride_1.estimatedCost < ride_2.estimatedCost:
            return True
        elif ride_1.estimatedCost == ride_2.estimatedCost and ride_1.timeTaken < ride_2.timeTaken:
            return True
        return False

  
class Node:
    def __init__(self, ride, color='R', left=None, right=None, parent_node=None):
        self.ride = ride
        self.color = color
        self.left = left
        self.right = right
        self.parent_node = parent_node

class RedBlackTree:
    def __init__(self):
        self.nil = Node(None, 'B')
        self.root = self.nil

    def left_rotation(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent_node = x
        y.parent_node = x.parent_node
        if x.parent_node == self.nil:
            self.root = y
        elif x == x.parent_node.left:
            x.parent_node.left = y
        else:
            x.parent_node.right = y
        y.left = x
        x.parent_node = y

    def right_rotation(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent_node = x
        y.parent_node = x.parent_node
        if x.parent_node == self.nil:
            self.root = y
        elif x == x.parent_node.right:
            x.parent_node.right = y
        else:
            x.parent_node.left = y
        y.right = x
        x.parent_node = y

    def insertion(self, ride):
        z = Node(ride)
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.ride.rideIdentifier < x.ride.rideIdentifier:
                x = x.left
            else:
                x = x.right
        z.parent_node = y
        if y == self.nil:
            self.root = z
        elif z.ride.rideIdentifier < y.ride.rideIdentifier:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = 'R'
        self.insertion_fixup(z)

    def insertion_fixup(self, z):
        while z.parent_node.color == 'R':
            if z.parent_node == z.parent_node.parent_node.left:
                y = z.parent_node.parent_node.right
                if y.color == 'R':
                    z.parent_node.color = 'B'
                    y.color = 'B'
                    z.parent_node.parent_node.color = 'R'
                    z = z.parent_node.parent_node
                else:
                    if z == z.parent_node.right:
                        z = z.parent_node
                        self.left_rotation(z)
                    z.parent_node.color = 'B'
                    z.parent_node.parent_node.color = 'R'
                    self.right_rotation(z.parent_node.parent_node)
            else:
                y = z.parent_node.parent_node.left
                if y.color == 'R':
                    z.parent_node.color = 'B'
                    y.color = 'B'
                    z.parent_node.parent_node.color = 'R'
                    z = z.parent_node.parent_node
                else:
                    if z == z.parent_node.left:
                        z = z.parent_node
                        self.right_rotation(z)
                    z.parent_node.color = 'B'
                    z.parent_node.parent_node.color = 'R'
                    self.left_rotation(z.parent_node.parent_node)
        self.root.color = 'B'

    def search(self, rideIdentifier):
        x = self.root
        while x != self.nil and x.ride.rideIdentifier != rideIdentifier:
            if rideIdentifier < x.ride.rideIdentifier:
                x = x.left
            else:
                x = x.right
        return x

    def replacing(self, u, v):
        if u.parent_node == self.nil:
            self.root = v
        elif u == u.parent_node.left:
            u.parent_node.left = v
        else:
            u.parent_node.right = v
        v.parent_node = u.parent_node

    def minimum_value(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    def deletion(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.replacing(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.replacing(z, z.left)
        else:
            y = self.minimum_value(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent_node == z:
                x.parent_node = y
            else:
                self.replacing(y, y.right)
                y.right = z.right
                y.right.parent_node = y
            self.replacing(z, y)
            y.left = z.left
            y.left.parent_node = y
            y.color = z.color
        if y_original_color == 'B':
            self.deletion_fixup(x)
    
    def deletion_fixup(self, x):
        while x != self.root and x.color == 'B':
            if x == x.parent_node.left:
                w = x.parent_node.right
                if w.color == 'R':
                    w.color = 'B'
                    x.parent_node.color = 'R'
                    self.left_rotation(x.parent_node)
                    w = x.parent_node.right
                if w.left.color == 'B' and w.right.color == 'B':
                    w.color = 'R'
                    x = x.parent_node
                else:
                    if w.right.color == 'B':
                        w.left.color = 'B'
                        w.color = 'R'
                        self.right_rotation(w)
                        w = x.parent_node.right
                    w.color = x.parent_node.color
                    x.parent_node.color = 'B'
                    w.right.color = 'B'
                    self.left_rotation(x.parent_node)
                    x = self.root
            else:
                w = x.parent_node.left
                if w.color == 'R':
                    w.color = 'B'
                    x.parent_node.color = 'R'
                    self.right_rotation(x.parent_node)
                    w = x.parent_node.left
                if w.right.color == 'B' and w.left.color == 'B':
                    w.color = 'R'
                    x = x.parent_node
                else:
                    if w.left.color == 'B':
                        w.right.color = 'B'
                        w.color = 'R'
                        self.left_rotation(w)
                        w = x.parent_node.left
                    w.color = x.parent_node.color
                    x.parent_node.color = 'B'
                    w.left.color = 'B'
                    self.right_rotation(x.parent_node)
                    x = self.root
        x.color = 'B'


class GatorTaxi:
    def __init__(self):
        self.min_heap = MinHeapTree()
        self.red_black_tree = RedBlackTree()

    def insertion(self, ride):

        node = self.red_black_tree.search(ride.rideIdentifier)
        if node != self.red_black_tree.nil:
            return False
        else:
            self.min_heap.insertion(ride)
            self.red_black_tree.insertion(ride)
            return True
            
    def getNextRide(self):
        ride = self.min_heap.extract_min_node()
        if ride is None:
            return "No active ride requests"
        node = self.red_black_tree.search(ride.rideIdentifier)
        self.red_black_tree.deletion(node)
        return f"({ride.rideIdentifier},{ride.estimatedCost},{ride.timeTaken})"
        

    def cancelRide(self, rideIdentifier):
        node = self.red_black_tree.search(rideIdentifier)
        if node != self.red_black_tree.nil:
            self.red_black_tree.deletion(node)
            for i, ride in enumerate(self.min_heap.heap):
                if ride.rideIdentifier == rideIdentifier:
                    self.min_heap.heap.pop(i)
                    break
            self.min_heap.down_heapify(0)

    def updateTrip(self, rideIdentifier, new_timeTaken):
        node = self.red_black_tree.search(rideIdentifier)
        if node != self.red_black_tree.nil:
            ride = node.ride
            if new_timeTaken < ride.timeTaken:
                ride.timeTaken = new_timeTaken
                self.cancelRide(rideIdentifier)
                self.insertion(ride)
            if ride.timeTaken < new_timeTaken <= 2 * ride.timeTaken:
                ride.timeTaken = new_timeTaken
                ride.estimatedCost += 10
                self.cancelRide(rideIdentifier)
                self.insertion(ride)
            elif new_timeTaken > 2 * ride.timeTaken:
                self.cancelRide(rideIdentifier)
    
    
    range_str = ""

    def print(self, rideIdentifier_1, rideIdentifier_2=None):
        
        if rideIdentifier_2 is None:
            node = self.red_black_tree.search(rideIdentifier_1)
            if node != self.red_black_tree.nil:
                ride = node.ride
                print(f"({ride.rideIdentifier},{ride.estimatedCost},{ride.timeTaken})",end="")
            else:
                print("(0,0,0)",end="")
        else:
            global range_str
            range_str = ""
            range_out=self.printRange(self.red_black_tree.root, rideIdentifier_1, rideIdentifier_2)
            if len(range_out)==0:
                print("(0,0,0)",end="")
            else:
                print(range_out[:-1],end="")

        print("")

    def printRange(self, node, rideIdentifier_1, rideIdentifier_2):
        global range_str
        if node != self.red_black_tree.nil:
            if rideIdentifier_1 < node.ride.rideIdentifier:
                self.printRange(node.left, rideIdentifier_1, rideIdentifier_2)
            if rideIdentifier_1 <= node.ride.rideIdentifier <= rideIdentifier_2:
                ride = node.ride
                range_str=range_str+(f"({ride.rideIdentifier},{ride.estimatedCost},{ride.timeTaken})")+","
            if rideIdentifier_2 > node.ride.rideIdentifier:
                self.printRange(node.right, rideIdentifier_1, rideIdentifier_2)
        
        return range_str


gator_taxi = GatorTaxi()


def process_input_line(line, output_file):
    sections = line.strip().split()
    input_string = sections[0]
    cmd = input_string.split('(')[0]
    args_str = input_string.split('(')[1].split(')')[0]
    args = [int(arg) for arg in args_str.split(',')] if args_str else []
    output = [cmd] + args
    cmd1 = output[0]

    if cmd1 == "Insert":
        rideIdentifier = output[1]
        estimatedCost = output[2]
        timeTaken = output[3]
        insertion_output =gator_taxi.insertion(RideRequest(rideIdentifier, estimatedCost, timeTaken))
        if insertion_output==False:
            output_file.write("rideNumber already exists.")
            sys.exit()

    elif cmd1 == "GetNextRide":
        next_ride = gator_taxi.getNextRide() 
        output_file.write(next_ride+"\n")

    elif cmd1 == "CancelRide":
        rideIdentifier = int(output[1])
        gator_taxi.cancelRide(rideIdentifier)

    elif cmd1 == "UpdateTrip":
        rideIdentifier = output[1]
        new_timeTaken = output[2]
        gator_taxi.updateTrip(rideIdentifier, new_timeTaken)

    elif cmd1 == "Print":
        rideIdentifiers = list(map(int, output[1:]))
        orig_stdout = sys.stdout
        sys.stdout = output_file
        gator_taxi.print(*rideIdentifiers)
        sys.stdout = orig_stdout

with open(sys.argv[1], "r") as input_file, open("output_file.txt", "w") as output_file:
    for line in input_file:
        process_input_line(line, output_file)