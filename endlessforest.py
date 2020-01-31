from labyrinthmaker import location, user


# start simulation of the labyrinth.
print("Welcome to the labyrinth.")
print("To interact, select the number of the corresponding prompt.")
print("Good luck, dreamer.\n\n\n")
print("You have descended into the labyrinth. You open your eyes to...")
my_user = user.User()
current_location = location.Location(my_user)
in_labyrinth = True
while current_location:
    current_location = current_location.encounter()
print("Goodbye, dreamer. Perhaps we will see you again soon...")
