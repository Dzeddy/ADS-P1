class Order:
    def __init__(self, order_id, current_system_time, order_value, delivery_time):
        self.order_id = order_id
        self.current_system_time = current_system_time
        self.order_value = order_value
        self.delivery_time = delivery_time
        self.normalized_order_value = order_value / 50
        self.priority = 0.3 * self.normalized_order_value - 0.7 * current_system_time
        self.eta = 0


class Node:
    def __init__(self, key, order):
        self.key = key
        self.order = order
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.root = None

    def getHeight(self, node):
        if not node:
            return 0
        return node.height

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def rightRotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))

        return x

    def leftRotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def insert(self, root, key, order):
        if not root:
            return Node(key, order)

        if key < root.key:
            root.left = self.insert(root.left, key, order)
        else:
            root.right = self.insert(root.right, key, order)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)

        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def insertOrder(self, order, key):
        self.root = self.insert(self.root, key, order)

    def remove(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.remove(root.left, key)
        elif key > root.key:
            root.right = self.remove(root.right, key)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.order = temp.order
            root.right = self.remove(root.right, temp.key)
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)
        return self.rebalance(root, balance)

    def getMinValueNode(self, node):
        if node is None or node.left is None:
            return node
        return self.getMinValueNode(node.left)

    def rebalance(self, node, balance):
        # Right rotate
        if balance > 1 and self.getBalance(node.left) >= 0:
            return self.rightRotate(node)
        # Left rotate
        if balance < -1 and self.getBalance(node.right) <= 0:
            return self.leftRotate(node)
        # Left Right rotate
        if balance > 1 and self.getBalance(node.left) < 0:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        # Right Left rotate
        if balance < -1 and self.getBalance(node.right) > 0:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)
        return node

    def find(self, key):
        return self._find(self.root, key)

    def _find(self, node, key):
        if node is None:
            return None
        elif key < node.key:
            return self._find(node.left, key)
        elif key > node.key:
            return self._find(node.right, key)
        else:
            return node

    def updateKey(self, old_key, new_key):
        node = self.find(old_key)
        if node:
            order = node.order
            self.root = self.remove(self.root, old_key)
            self.root = self.insert(self.root, new_key, order)

    def find_predecessor(self, priority):
        node = self.root
        predecessor = None
        while node:
            if node.key > priority:
                predecessor = node
                node = node.right
            else:
                node = node.left
        return predecessor

    def in_order_traversal(self):
        nodes = []
        self._in_order_traversal(self.root, nodes)
        return nodes

    def _in_order_traversal(self, node, nodes):
        if node is not None:
            self._in_order_traversal(node.left, nodes)
            nodes.append(node.order)  # Assuming each node stores an 'order' object.
            self._in_order_traversal(node.right, nodes)

    def search(self, node, order_id):
        """
        Search for a node with a given order_id in the AVL Tree.

        :param node: The current node in the AVL Tree being inspected.
        :param order_id: The order_id being searched for.
        :return: The Node containing the Order with the matching order_id, or None if not found.
        """
        # Base Case: node is None or the order_id matches the node's order's order_id
        if not node or node.order.order_id == order_id:
            return node

        # If the order_id is smaller than the node's order's order_id, then it lies in the left subtree
        if order_id < node.order.order_id:
            return self.search(node.left, order_id)

        # If the order_id is greater than the node's order's order_id, then it lies in the right subtree
        return self.search(node.right, order_id)

    def removeOrderByID(self, root, order_id):
        """
        Remove a node from the AVL Tree based on order_id, starting at the given root.

        :param root: The root of the subtree to search for the order_id.
        :param order_id: The order_id of the order to be removed.
        :return: The root of the modified subtree.
        """
        if not root:
            return root

        # Perform standard BST delete
        left_deleted = self.removeOrderByID(root.left, order_id)
        right_deleted = self.removeOrderByID(root.right, order_id)

        if root.order.order_id == order_id:
            # Node with the order_id found
            # Cases with one or no child
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            # Node with two children: Get the inorder successor
            temp = self.getMinValueNode(root.right)
            root.order = temp.order
            root.key = temp.key
            root.right = self.removeOrderByID(root.right, temp.order.order_id)
        else:
            root.left = left_deleted
            root.right = right_deleted

        # If the tree had only one node then return
        if root is None:
            return root

        # Update height of the current node
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # Rebalance the node
        balance = self.getBalance(root)
        return self.rebalance(root, balance)

    def rebuildTreeBasedOnETA(self):
        orders = []
        self._collectAllOrders(self.root, orders)
        orders.sort(key=lambda order: order.eta)
        self.root = self._rebuildTreeFromSortedOrders(orders, 0, len(orders) - 1)

    def _collectAllOrders(self, node, orders):
        if node is not None:
            self._collectAllOrders(node.left, orders)
            orders.append(node.order)  # Assuming each node stores an 'Order' object
            self._collectAllOrders(node.right, orders)

    def _rebuildTreeFromSortedOrders(self, orders, start, end):
        if start > end:
            return None
        mid = (start + end) // 2
        node = Node(orders[mid].eta, orders[mid])  # Assuming ETA is the new key
        node.left = self._rebuildTreeFromSortedOrders(orders, start, mid - 1)
        node.right = self._rebuildTreeFromSortedOrders(orders, mid + 1, end)
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        return node
