class User:

    def __init__(self):
        '''Initializes User. creates inventory and sets hp.'''
        self.inventory = []
        self.hp = 100

    def add_inventory(self, item):
        '''Adds item to the user's inventory.'''
        self.inventory.append(item)

    def remove_inventory(self, item):
        '''removes item from the user's inventory.'''
        self.inventory.remove(item)

    def print_inventory(self):
        '''prints the contents of the user's inventory.'''
        print("You check the contents of your bag.")
        if len(self.inventory) == 0:
            print("You have nothing, and no one.")
            return
        for i in range(len(self.inventory)):
            print(str(i + 1), "-", self.inventory[i])

    def check_inventory(self):
        '''checks the user's inventory.
           returns the item that the user would like to use;
           if the user decides to cancel the interaction, then it returns none.
        '''

        self.print_inventory()
        while True:
            print("\nWhat will you do?")
            print("1 - Use item     2 - Cancel")
            useraction = input()
            try:
                useraction = int(useraction)
            except:
                pass

            if useraction == 1:
                # use an item.
                item = input("What item would you like to use?: ")
                try:
                    item = int(item)
                    item = self.inventory[item - 1]
                    self.remove_inventory(item)
                    return item
                except:
                    print("Are you sure you have that item?")
                    print("Maybe it was just a dream...")
                    pass
            elif useraction == 2:
                print("You close your bag and turn your attention back to your \
surroundings.")
                return
            else:  # invalid input
                print("You have a feeling that this isn't something you can \
do.")

    def change_hp(self, change):
        '''adds [change] to the user's hp. returns nothing.'''
        self.hp += change
