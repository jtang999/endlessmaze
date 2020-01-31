from random import randint, getrandbits, choice


class Monster:
    ''' MONSTER
       - class variables:
         - word banks of adjectives and descriptors for instances of the class
           to draw upon.
       - instance variables:
         - health/hp
         - aggressive: true/false. if aggressive, will attack when disturbed.
         - randomly generated descriptors drawn from the class's word bank.
         - monster's location
       - init: makes a monster with a random amount of hp, description, and
         aggressiveness.
       - encounter(self): user initiates contact with monster. monster will
         ignore user if nonaggressive, otherwise will attack.
       - battle(self): a helper function to simulate battle with the monster.
       - attack(self): monster attacks user and inflicts random damage. returns
         the amount of damage done.
       - deal_damage(self, amount): subtracts [amount] from monster's HP. if HP
         falls below 0, removes monster from current location.
       - appease(self, threshold=50): generates a random number in range(100).
         if it is above threshold, then the monster becomes non-aggressive.'''

    adj = ["brittle", "dripping", "gleaming", "glittering", "heaving",
           "sharp and cruel", "light", "whimsical", "curious", "sinuous",
           "chitinous", "innumerable", "scaly", "feathered", "long"]
    phrase = ["dark and empty as void", "cracked open like the dry earth",
              "incandescent as the fiery heart of stars",
              "pale as bone", "hazier than mist and mirage",
              "haunting as the skeletal trees of a petrified forest",
              "uncertain in shape as clouds in wind",
              "non-newtonian in movement and nature",
              "liquidlike in its endless dripping"]
    body1 = ["antlers", "horns", "teeth", "claws", "limbs", "tentacles",
             "eyes", "wings", "ears", "scales", "masks", "faces", "bodies",
             "jutting bones"]
    body2 = ["muzzle", "jaw", "back", "tail", "tongue", "shell", "exoskeleton",
             "breath", "body", "fur"]
    disposition = ["indifferent", "apathetic", "cold", "old",
                   "ancient", "inhuman", "soulless", "mirthful",
                   "angry", "hateful"]
    noise = ["rattles", "hisses", "screams", "growls", "gurgles", "howls",
             "cries", "laughs", "whispers", "scratches", "cackles"]

    def __init__(self, loc, user):
        self.hp = randint(20, 500)
        self.aggressive = bool(getrandbits(1))
        self.location = loc
        self.a = choice(Monster.adj)
        self.ph = choice(Monster.phrase)
        self.b1 = choice(Monster.body1)
        self.b2 = choice(Monster.body2)
        self.aura = choice(Monster.disposition)
        self.user = user

    def encounter(self):
        '''Simulates an encounter with the monster.
        User can observe, attack, or withdraw.
        If the monster is aggressive, entering an encounter with it will
        immediately cause battle to commence.'''
        in_encounter = True
        while in_encounter:
            if self.aggressive:
                in_encounter = self.battle()
                continue
            if self.user.hp <= 0:
                return
            print("\nYou look at the creature before you. What will you do?")
            print("1 - Observe    2 - Attack")
            print("3 - Tame       4 - Withdraw")
            action = input()
            try:
                action = int(action)
            except:
                pass

            if action == 1:
                # describes the monster.
                print(self.describe())
            elif action == 2:
                # attack the monster and enter a battle with it.
                print("Moved by some dark thought in your mind, you attack.")
                self.aggressive = True
                in_encounter = self.battle()
            elif action == 3:
                # Just to set the mood. :)
                self.tame()
            elif action == 4:
                # End encounter with the monster.
                print("Your curiosity satisfied, you turn your attention \
back to your surroundings.")
                in_encounter = False
            else:
                # invalid input.
                print("You feel a strong sense of dizziness. You can't make \
sense of the thoughts and sensations that just drifted through your mind.")
            action = ""

    def battle(self):
        '''Helper function. simulates a battle with the monster.
        Return value: represents whether the user is still in an encounter
            with the beast at the end of battle.
        Returns True if beast is alive & is no longer aggressive (i.e, it has
            been appeased, or successfully fed an item.)
        Returns False if you or the beast is killed in battle.'''

        print("You have disturbed the beast. Now you will die.")
        while self.aggressive:
            if self.user.hp <= 0:
                # checks if you died in the previous loop. if so, ends
                # the encounter.
                print("The beast strikes the final blow. Your consciousness \
separates from your body.\nWhat is happening to you...?")
                return
            print(self.describe())
            if self.hp <= 0:
                # checks if monster died in the previous loop. if so, ends
                # the encounter.
                print("The monster screams its hatred but it is not enough \
to save it.")
                print("You have slaughtered your prey.")
                self.location.remove_object(self)
                self.location = None
                return False

            print("\nWhat will you do?")
            print("1 - Fight    2 - Use inventory")
            print("3 - Appease  4 - Flee")
            action = input()
            try:
                action = int(action)
            except:
                pass

            if action == 1:
                # user and monster exchange blows.
                dmg = randint(20, 80)
                print("You attack the monster with all your might.")
                print("You have dealt {0} damage.".format(dmg))
                self.deal_damage(dmg)
                if self.hp > 0:
                    print("However, did you escape unscathed?")
                    self.attack()
                    print("Current hp:", self.user.hp)
            elif action == 2:
                # use plants in inventory.
                plant = self.user.check_inventory()
                if plant:
                    next_action = input("What would you like to do with this?\n\
1 - Eat      2 - Feed the beast\n")
                    try:
                        next_action = int(next_action)
                    except:
                        pass

                    if next_action == 1:
                        # eat the plant. good luck!
                        print("Hastily, you swallow the plant.")
                        if plant.poisonous:
                            print("You feel sick. Have you misjudged?")
                        else:
                            print("You feel some energy returning to you.")
                        plant.consume()
                    elif next_action == 2:
                        # feed the plant to the monster. good luck!
                        print("You wave the plant in front of the beast. \
Perhaps the scent or flavor will calm the beast down?")
                        self.appease(threshold=plant.feed())
                    else:
                        # whatever happens, the plant will no longer be
                        # useable. better not mess up on your input.
                        print("A moment of incoherence overtakes you. When you\
 come back to yourself, you find that your surroundings bear more signs of \
 the beast's attacks, and it seems angrier than ever. The plant that was once \
 in your hands is lying in shreds on the ground, stomped to uselessness \
 underfoot.\n\nYou should be more careful about yourself. Who knows what would\
  happen next time.")
            elif action == 3:
                # try and calm the monster down so it's no longer appease.
                self.appease()
            elif action == 4:
                # try to run away. 50/50 chance of success.
                if bool(getrandbits(1)):
                    print("You manage to get away by the skin of your teeth.")
                    return False
                else:
                    print("You run, but the beast blocks your way.")
            else:
                # invalid input.
                print("No, that isn't right. That isn't right. That isn't \
right.")

        return True

    def attack(self):
        '''Returns how much damage the monster will deal to the user.
        Damage is proportional to the monster's health.'''
        self.user.change_hp(-1 * (self.hp // 10))

    def deal_damage(self, damage):
        '''Deals damage to the monster. Returns nothing.'''
        self.hp -= damage
        print("Remaining health: {0}".format(self.hp))
        # remove from location

    def appease(self, threshold=50):
        '''If you are battling the monster, try and calm it down.
           It has a random chance of working.
           Modifies the monster's aggressive stat accordingly.
        '''

        if not self.aggressive:
            print("It does not seem interested in attacking you.")
        elif randint(1, 100) > threshold:
            self.aggressive = False
            print("The creature's attack ceases.")
        else:
            print("The creature's ire fails to abate. It {0} its {1} \
thoughts to the sky.".format(choice(Monster.noise), self.aura))

    def tame(self):
        '''Just a bit of a joke function to set the mood. :)'''
        print("As if a monster could ever be tamed.")

    def describe(self):
        '''Returns one of two random descriptions of the monster.'''

        if bool(getrandbits(1)):
            return "You stare at its {0} {1}.".format(self.a, self.b2)
        return "Its {0} are {1}.".format(self.b1, self.ph)

    def __repr__(self):
        return "A monster. " + self.describe()
