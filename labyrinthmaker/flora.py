from random import randint, getrandbits, choice


class Flora:
    ''' 3. FLORA
       - class variables:
         - word banks of adjectives and descriptors for instances of the class
           to draw upon.
       - instance variables:
         - poisonous: true/false
         - health value: random. if poisonous, will subtract this amount from
           user's hp. otherwise, will add health value to user's hp.
         - appeasement value: random. if fed to a monster, changes the
           threshold in monster's appease function to this value.
         - randomly generated descriptors drawn from the class's word bank.
       - init: makes a flora with randomized instance variables.
       - encounter(self): returns a description of the flower.
       - add_inventory(self): moves self to the user's inventory
       - consume(self): eat the plant. removes from user's inventory. returns
         an int(its health value)
       - feed(self): feed the plant to a monster. removes from user's inventory
         returns its appeasement value. '''

    adj1 = ["glowing", "thready", "delicate", "thorny", "frilled", "shivering",
            "hateful", "cancerous", "pendulous", "thin-leaved", "webbed",
            "spiraling", "towering", "translucent", "oozing", "crystalline",
            "drunken", "despairing", "autumn", "tempting"]
    adj2 = ["melancholy", "melodious", "fluttering", "shadow-dark", "shifting",
            "lightning-sharp", "clamoring", "fierce", "drooping", "watchful",
            "tyrannical", "withering", "shriveled", "lush", "iridescent"]
    scent = ["lightning", "rot and decay", "the sweetness of death",
             "a merry and mocking fermentation", "winter sunlight",
             "a drunken and despairing starlight", "dew",
             "the fresh growth that comes after rain",
             "something that reminds you of home",
             "something that makes you feel heartsick", "sleep"]
    action = ["sways", "rattles", "cries", "moans", "sings", "whispers",
              "laughs", "curls coyly", "beckons", "dances",
              "waves like it is almost alive", "is unnaturally still"]

    def __init__(self, loc, user):
        '''Creates a Flora with random instance variables and descriptors.'''

        self.poisonous = bool(getrandbits(1))
        self.healthvalue = randint(20, 200)
        self.appeasevalue = randint(0, 100)
        self.desc1 = choice(Flora.adj1)
        self.desc2 = choice(Flora.adj2)
        self.smell = choice(Flora.scent)
        self.move = choice(Flora.action)
        self.user = user
        self.loc = loc

    def encounter(self):
        ''' enters an interaction with the flora in question.'''

        print("You look at the strange growth before you.")
        in_encounter = True

        while in_encounter:
            print("\nWhat will you do?")
            print("1 - Observe   2 - Smell")
            print("3 - Harvest   4 - Withdraw")
            action = input()
            try:
                action = int(action)
            except:
                pass

            if action == 1:
                # describes the plant.
                print(self.describe())
            elif action == 2:
                # smell the plant.
                print(self.scentit())
            elif action == 3:
                # harvest the plant and add to user's inventory.
                # removes plant from current location as well.
                self.add_inventory()
                self.loc.remove_object(self)
                print("You carefully harvest one of its arms, ignoring the \
way it {0} as you do.".format(self.move))
                in_encounter = False
            elif action == 4:
                # end inspection and return to current location.
                print("Your curiosity satisfied, you turn your attention \
back to your surroundings.")
                in_encounter = False
            else:
                # invalid input.
                print("The world goes gray and fuzzy. You're not sure how much\
 time passes until it stabilizes again.\n\nWhat were you trying to do again?")

        return None

    def add_inventory(self):
        '''adds the Flora instance to user's inventory.'''
        self.user.add_inventory(self)

    def consume(self):
        '''simulates the user eating the Flora.
        returns what value to change the user's HP by.'''
        if self.poisonous:
            return -self.healthvalue
        return self.healthvalue

    def feed(self):
        '''simulates the user feeding the Flora to a beast.
        this changes the likelihood of the beast being appeased by the user.'''
        return self.appeasevalue

    def describe(self):
        '''returns a description of the plant's appearance.'''

        if bool(getrandbits(1)):
            return "A {0} and {1} thing.".format(self.desc1, self.desc2)
        return "It {0} in the breeze.".format(self.move)

    def scentit(self):
        '''returns a description of the plant's smell.'''

        return "It smells like {0}.".format(self.smell)

    def __repr__(self):
        return "A flora. " + self.describe()
