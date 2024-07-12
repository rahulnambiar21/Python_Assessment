while True:
    print("1. Fruit Market Manager")
    print("2. Customer")
    print("3. Exit")
    print("*"*50)

    choice=int(input("Enter your Choice : "))

    if choice==1:
        fruits = {}

        def add_fruit_stock():
            print("\nAdd Fruit Stock:")
            fruit_name = input("Enter fruit name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per unit: "))

            if fruit_name in fruits:
                print(f"{fruit_name} already exists in stock. Updating quantity.")
                fruits[fruit_name]['quantity'] += quantity
                fruits[fruit_name]['price'] = price
            else:
                fruits[fruit_name] = {'quantity': quantity, 'price': price}
                print(f"{quantity} {fruit_name}(s) added to stock.")

        def view_stock():
            print("\nCurrent Fruit Stock:")
            for fruit, details in fruits.items():
                print(f"Fruit: {fruit}, Quantity: {details['quantity']}, Price per unit: Rs.{details['price']}")

        def update_stock():
            print("\nUpdate Fruit Stock:")
            fruit_name = input("Enter fruit name to update: ")
            if fruit_name in fruits:
                new_quantity = int(input("Enter new quantity: "))
                new_price = float(input("Enter new price per unit: "))
                fruits[fruit_name]['quantity'] = new_quantity
                fruits[fruit_name]['price'] = new_price
                print(f"{fruit_name} stock updated.")
            else:
                print(f"{fruit_name} not found in stock.")

        # Example usage
        if __name__ == "__main__":
            while True:
                print("\nManager Menu:")
                print("1. Add Fruit Stock")
                print("2. View Stock")
                print("3. Update Stock")
                print("4. Exit")

                choice = input("Enter your choice: ")

                if choice == '1':
                    add_fruit_stock()
                elif choice == '2':
                    view_stock()
                elif choice == '3':
                    update_stock()
                elif choice == '4':
                    print("Exiting manager module.")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")
    elif choice == '3':
        print("Exiting Fruit manager module.")
        break
        


