from avltree import AVLTree, Order

import sys

class DeliverySystem:
    def __init__(self):
        self.priority_tree = AVLTree()
        self.eta_tree = AVLTree()
        self.orders = {}  # orderId -> order object
        self.current_system_time = 0

    def calculate_priority(self, order):
        return 0.3 * order.normalized_order_value - 0.7 * order.current_system_time

    def create_order(self, order_id, current_system_time, order_value, delivery_time):
        self.current_system_time = current_system_time  # Assume system time updates with each order creation.
        order = Order(order_id, current_system_time, order_value, delivery_time)
        order.priority = self.calculate_priority(order)
        self.orders[order_id] = order
        self.priority_tree.insertOrder(order, order.priority)  # Insert based on priority.
        # Update ETAs for all orders including the new one.
        self.update_all_etas(new_order=order)
        self.eta_tree.insertOrder(order, order.eta)
        self.runOrders()

        print(f"Order {order_id} has been created - ETA: {order.eta}")

    def cancel_order(self, order_id, current_system_time):
        if order_id in self.orders:
            order = self.orders[order_id]
            if order.eta <= current_system_time:
                print(f"Cannot cancel. Order {order_id} has already been delivered")
            else:
                self.priority_tree.root = self.priority_tree.removeOrderByID(self.priority_tree.root, order.order_id)
                self.eta_tree.root = self.eta_tree.removeOrderByID(self.eta_tree.root, order.order_id)
                del self.orders[order_id]
                print(f"Order {order_id} has been canceled")
        else:
            print(f"Order {order_id} not found")

    def update_time(self, order_id, current_system_time, new_delivery_time):
        if order_id not in self.orders:
            print(f"Order {order_id} not found")
            return
        order = self.orders[order_id]
        if order.eta <= current_system_time:
            print(f"Cannot update. Order {order_id} has already been delivered")
            return

        # Update the order's delivery time.
        order.delivery_time = new_delivery_time

        # Re-calculate priorities if necessary or directly update ETAs.
        self.update_all_etas()

        print(f"Order {order_id} delivery time updated - New ETA: {order.eta}")

    def update_all_etas(self, new_order=None):
        # This method will traverse the priority tree and update ETAs.
        # If new_order is provided, it incorporates the new_order into ETA calculations.
        orders = self.priority_tree.in_order_traversal()[::-1]  # Assumes this method returns orders in priority order.
        current_eta = self.current_system_time

        for order in orders:
            if order.eta > current_eta > order.eta - order.delivery_time:  # Order is already serviced
                current_eta = order.eta
            else:  # Calculate new ETA based on current_eta and order's delivery time.
                if order == new_order and new_order:
                    # For the new order, compare its priority.
                    order.eta = max(self.current_system_time, current_eta) + order.delivery_time
                else:
                    # Update existing orders' ETAs.
                    order.eta = current_eta + order.delivery_time
            current_eta = order.eta + order.delivery_time  # Account for return time.


    def print_order(self, order_id):
        if order_id in self.orders:
            order = self.orders[order_id]
            print(f"[{order.order_id} {order.current_system_time} {order.order_value} {order.delivery_time} {order.eta}]")
        else:
            print(f"Order {order_id} not found")

    def print_orders(self, time1, time2):
        # This would involve traversing the ETA tree and finding orders within the given range
        pass  # Placeholder for demonstration purposes

    def get_rank_of_order(self, order_id):
        if order_id not in self.orders:
            print(f"Order {order_id} not found")
            return
        order = self.orders[order_id]
        # Assuming a method to calculate rank based on order priority
        rank = self.priority_tree.getRank(order.priority)
        print(f"Order {order_id} will be delivered after {rank} orders")

    def complete_Order(self, order_id):
        self.priority_tree.root = self.priority_tree.removeOrderByID(self.priority_tree.root, order_id)
        self.eta_tree.root = self.eta_tree.removeOrderByID(self.eta_tree.root, order_id)
        print(f"Order {order_id} has been delivered at time {self.orders[order_id].eta}")
        del self.orders[order_id]

    def runOrders(self):
        orders = self.eta_tree.in_order_traversal()  # Assumes this method returns orders in priority order.
        for i in orders:
            if i.eta < self.current_system_time:
                self.complete_Order(i.order_id)
            else:
                break

# Main program logic to parse commands and execute corresponding methods would go here
