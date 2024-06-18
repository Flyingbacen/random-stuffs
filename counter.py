import json

def usercounting():
    input("Press Enter to start counting")
    try:
        try:
            with open("counter.json", "r") as f:
                count = json.load(f)["count"]
        except FileNotFoundError:
            print("\"counter.json\" file not found in working directory. Starting from 1.")
        while True:
            choice = input()
            try: 
                if int(choice) == count:
                    count += 1
                else:
                    count = 1
                    print("\n\n\n\n\n\n\n\n\n\n") # Artificially clear the screen
                    print(f"The next number was {count} not {choice}. Restarting count.")
            except ValueError:
                print("Please enter a number.")
    except KeyboardInterrupt:
        try:
            with open("counter.json", "w") as f:
                json.dump({"count": count}, f) # saving feature
        except FileNotFoundError:
            print("Could not save count. \"counter.json\" file not found in working directory.")
        return count
if __name__ == "__main__":
    print("You counted to: ", usercounting())