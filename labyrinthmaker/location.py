from random import randint, shuffle, choice
from labyrinthmaker import flora, monster


class Location:
    '''LOCATION
       - class variables:
         - word bank of adjectives and descriptors for instances of the class
           to draw upon.
       - instance variables:
         - dict of location objects to the north, south, east, west (if known)
         - list of monsters and flora at the location
         - randomly generated descriptors drawn from the class's word bank.
       - init(self, north=None, south=None, east=None, west=None): by default
         creates a location with no known locations adjacent to it.
         can pass in location objects for the east, west, north, south of it
         generates a random number of monsters and flora.
       - connect(self, adjacent_location, direction): adds a specified location
         object to the location's dictionary of adjacent locations.
       - remove_object(self, object): removes the given object from the list of
         things that are currently at location.
       - investigate(self): prints list of things in the clearing that the user
         can interact with.
       - look_closely(self, index): user enters an encounter with the object at
         [index] of the location's list of monsters and flora.'''

    directions = ["north", "south", "east", "west"]
    oppositedir = {"north": "south", "south": "north", "east": "west",
                   "west": "east"}
    biomes = ["forest", "swamp", "clearing", "meadow", "bog", "wetland",
              "desert", "cliffside", "mountain", "river", "lake", "pond",
              "field", "plain"]
    weathers = ["searingly hot", "humid with melancholy", "raining black oil",
                "echoing with the crying wind",
                "rumbling with an oncoming storm",
                "a little bit unreal, as if you were not quite here",
                "cold as the eye of the moon",
                "twisting with madness"]
    detailsA = ["opalescent waters", "golden and dreamy trees",
                "blade-like grass", "mirrored surfaces staring out at you",
                "peaceful flowers scattered all around",
                "sinister vines creeping along the ground",
                "worn cobblestones of a long-gone city scattered about",
                "sand and dust of some unknown remains blowing in the wind",
                "flocks of what should be birds haunting the horizon",
                "strange undergrowth that is warm and fleshy to the touch",
                "plants - or are they animals? - that shrink at your approach"]
    detailsB = ["ink-dark currents swirling through the air",
                "nightmarish shapes against the horizon",
                "a distorted sky with too many eyes and too many teeth",
                "flickering ghosts that vanish when you look too close",
                "a strange, dreamy aura, as though you were entombed",
                "a sharp feeling, as if you have become far too awake",
                "the feeling that you shouldn't look too much",
                "a thick red mist that rises underfoot as you walk",
                "glowing fungi of all sizes not quite safe to touch",
                "carnivorous-looking plants turning towards you as you walk"]

    def __init__(self, user, north=None, east=None, south=None, west=None):
        '''Generates a Location object with random descriptions and randomized
        Monster and Flora objects.'''

        self.adjacent_locations = {"north": north, "east": east,
                                   "south": south, "west": west}
        self.interactables = []
        for i in range(randint(0, 5)):
            self.interactables.append(flora.Flora(self, user))
        for i in range(randint(0, 5)):
            self.interactables.append(monster.Monster(self, user))
        shuffle(self.interactables)
        self.numthings = len(self.interactables)

        self.user = user

        self.biome = choice(Location.biomes)
        self.weather = choice(Location.weathers)
        self.detail1 = choice(Location.detailsA)
        self.detail2 = choice(Location.detailsB)

    def connect(self, adjacent_location, direction):
        '''connects an adjacent location to this location.
           - [adjacent_location]: location to be connected to this location.
           - [direction]: which direction [adjacent_location] is from the
             current location, i.e. it is north of here.'''

        if direction not in self.directions:
            print("direction not real!")
        elif not adjacent_location:
            print("location being added does not exist!")
        else:
            self.adjacent_locations[direction] = adjacent_location

    def remove_object(self, ob):
        '''removes [ob] from the list of interactable objects at the
        location.'''

        self.interactables.remove(ob)
        self.numthings -= 1

    def describe(self):
        '''gives a description of the current location.'''

        return "A {0} that is {1}, with {2} and {3}.".format(self.biome,
                                                             self.weather,
                                                             self.detail1,
                                                             self.detail2)

    def investigate(self):
        '''prints a list of interactable objects in the location.'''
        if self.numthings == 0:
            print("There is nothing here left to see.")
            return
        for i in range(self.numthings):
            print(str(i + 1), "-", self.interactables[i])

    def look_closely(self, index):
        '''enters an encounter with the interactable object at
        [index] in the location's list of interactable objects.'''

        if index >= self.numthings or index < 0:
            print("The thing you are looking for does not exist.")
            print("Perhaps it was simply a trick of the eye...")
        else:
            self.interactables[index].encounter()

    def encounter(self):
        '''simulates an "encounter" with the location. user can interact with
        the location, look around for interactable objects, check status,
        check inventory, and interact with different monsters and plants in
        the location.'''

        print(self.describe())
        in_encounter = True

        while in_encounter:
            # check if user was killed in an encounter, i.e. by fighting a
            # monster or eating a poisonous plant.
            if self.user.hp <= 0:
                print("\n\n\n\nLike so many before you, you have fallen to the\
 dream.\n\nIt's time to wake up.\n")
                return False
            print("\nWhat will you do?")
            print("1 - Observe                  2 - Interact")
            print("3 - Inventory                4 - Check status")
            print("5 - Leave current location   6 - Leave the labyrinth")
            action = input()
            try:
                action = int(action)
            except:
                pass

            if action == 1:
                # investigate the area.
                print("You look around the area to see what catches your eye.")
                self.investigate()
            elif action == 2:
                # choose an object to interact with.
                idx = input("What will you investigate closer?: ")
                try:
                    idx = int(idx)
                    self.look_closely(idx - 1)
                except:
                    print("You look for...\nfor...\n...")
                    print("You feel an overwhelming sense of vertigo. Something\
 feels terribly wrong.\n\nWhat were you looking for again?\n")
                    pass
            elif action == 3:
                # check your inventory.
                plant = self.user.check_inventory()
                if plant:
                    print("You consume the chosen plant.")
                    self.user.change_hp(plant.consume())
                    if plant.poisonous:
                        print("It makes you feel sick.")
                    else:
                        print("It soothes you. You feel energy coming back.")
                    print("Current hp:", self.user.hp)
            elif action == 4:
                # check your health status.
                print("Current hp:", self.user.hp)
            elif action == 5:
                # leave the area.
                print("Which direction will you go?")
                print("1 - north      2 - east")
                print("3 - south      4 - west")
                direction = input()
                try:
                    direction = int(direction)
                except:
                    print("No, that direction doesn't seem quite right...?")
                    pass

                if direction == 1:
                    direction = "north"
                elif direction == 2:
                    direction = "east"
                elif direction == 3:
                    direction = "south"
                elif direction == 4:
                    direction = "west"

                if direction in Location.directions:
                    # head in the new direction.
                    print("You head", direction + ".")
                    # go back to preexisting location.
                    if self.adjacent_locations[direction]:
                        return self.adjacent_locations[direction]

                    # if there is no location already in that direction,
                    # create a new location and store its info.
                    new_loc = Location(self.user)
                    self.adjacent_locations[direction] = new_loc
                    opposite_dir = Location.oppositedir[direction]
                    new_loc.connect(self, opposite_dir)
                    return self.adjacent_locations[direction]
            elif action == 6:
                # exit the program.
                print("It's time to wake up from the dream.")
                return False
            else:
                # user did not give valid input.
                print("A splitting pain assaults your skull, and your vision \
goes black. When you open your eyes again, you can't remember what you were \
thinking of. How much time has passed?")
