import sys

from deliverysystem import DeliverySystem

# ... (rest of the code remains the same)

def main():
    delivery_system = DeliverySystem()
    input_file = sys.argv[1]
    output_file = f"{input_file}_output_file.txt"

    with open(input_file, 'r') as file:
        commands = file.readlines()

    #sys.stdout = open(output_file, 'w')

    for command in commands:
        command = command.strip()
        if command.startswith("createOrder"):
            order_id, current_system_time, order_value, delivery_time = map(int, command[12:-1].split(', '))
            delivery_system.create_order(order_id, current_system_time, order_value, delivery_time)
        elif command.startswith("cancelOrder"):
            order_id, current_system_time = map(int, command[12:-1].split(', '))
            delivery_system.cancel_order(order_id, current_system_time)
        elif command.startswith("updateTime"):
            order_id, current_system_time, new_delivery_time = map(int, command[11:-1].split(', '))
            delivery_system.update_time(order_id, current_system_time, new_delivery_time)
        elif command.startswith("print("):
            if ',' in command:
                time1, time2 = map(int, command[6:-1].split(', '))
                delivery_system.print_orders(time1, time2)
            else:
                order_id = int(command[6:-1])
                delivery_system.print_order(order_id)
        elif command.startswith("getRankOfOrder"):
            order_id = int(command[15:-1])
            delivery_system.get_rank_of_order(order_id)
        elif command == "Quit()":
            break

    #sys.stdout.close()

if __name__ == "__main__":
    main()
