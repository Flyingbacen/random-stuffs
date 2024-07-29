from requests import get
from os import system

def jsondata() -> dict:
    """open api at https://docs.biggames.io
    always uses the most up-to-date data"""
    url = "https://biggamesapi.io/api/collection/eggs"
    response = get(url)
    data = response.json()
    return data

def search(search_term, jsoninf) -> dict:
    data = jsoninf
    results = []
    # Step 1: Collect matches
    for egg in data['data']:
        for pet in egg['configData']['pets']:
            if search_term.lower() in pet[0].lower():
                results.append(egg)

    # Step 2: Display matches to user
    if len(results) > 1:
        print("Multiple matches found. Please select an egg:")
        for i, egg in enumerate(results):
            pets = ', '.join([pet[0] for pet in egg['configData']['pets']])
            print(f"{i+1}: Egg '{egg['configName']}' containing pets: {pets}")
        
        # Step 3: User selection
        try:
            selection = int(input("Enter the number of the egg you want to use: ")) - 1
        except ValueError:
            print("Please enter a number.")
            input("Press enter to try again.")
            search(search_term, jsoninf)
        if 0 <= selection < len(results):
            selected_egg = results[selection]
        else:
            print("Invalid selection.")
            return None
    elif results:
        selected_egg = results[0]
    else:
        print("No matches found.")
        main()

    # display the selected egg with all its pets
    if selected_egg:
        pets = ', '.join([f"{pet[0]} (Chance: {pet[1]}%)" for pet in selected_egg['configData']['pets']])
        print(f"Selected Egg '{selected_egg['configName']}' contains pets: {pets}")
        return selected_egg

def finalPrint(list):
    system("cls")
    for i in list:
        print(i)

def percentage(selected_egg: dict) -> str:
    odds = []
    finalStatement1 = []
    for pet in selected_egg['configData']['pets']:
        chance_standard_notation = "{:.10f}".format(float(pet[1]))
        chance_standard_notation = chance_standard_notation.rstrip('0').rstrip('.')
        odds.append(f"Pet: '{pet[0]}': {chance_standard_notation}%")
        # print(f"Pet: '{pet[0]}' with a chance of {chance_standard_notation}%")
    largestlength = 0
    for i in odds:
        length = len(i.split(":")[1])
        largestlength = length if length > largestlength else largestlength
    for i in odds:
        i = i.split(":")
        i[1] = i[1].ljust(largestlength)
        finalStatement1.append(f"{i[0]}:{i[1]}|{i[2]}")
    finalPrint(finalStatement1)

def one_in_x(selected_egg: dict) -> str:
    odds = []
    finalStatement2 = []
    system("cls")
    for pet in selected_egg['configData']['pets']:
        try:
            odds.append(f"Pet: '{pet[0]}': 1 in {round(100 / float(pet[1]), 3) if round(100 / float(pet[1])) == 1 else round(100 / float(pet[1]))}")
        except ZeroDivisionError:
            print(f"ERROR: Pet: '{pet[0]}' with an undefined chance (0%)\nunable to continue")
            input()
            exit()
    largestlength = 0
    for i in odds:
        length = len(i.split(":")[1])
        largestlength = length if length > largestlength else largestlength
    for i in odds:
        i = i.split(":")
        i[1] = i[1].ljust(largestlength)
        if float(i[2].split("1 in ")[1]) > 999.9:
            i[2] = f" 1 in {'{:,}'.format(int(float(i[2].split('1 in ')[1])))}"
        finalStatement2.append(f"{i[0]}:{i[1]}|{i[2]}")
    finalPrint(finalStatement2)


def main():
    searchterm = input("Enter the name of the pet you want to search for: ")
    selected_egg = search(searchterm, jsondata())
    if selected_egg:
        print(f"Selected Egg: '{selected_egg['configName']}'")
        system("cls")
        first = True
        while True:
            choice = input(('\n\n' if not first else '') + "type '1' for percentage\ntype '2' for 1 in x\ntype '0' to search again\npress enter to exit: ")
            if choice == "1":
                system("cls")
                percentage(selected_egg)
                first = False
            elif choice == "2":
                system("cls")
                one_in_x(selected_egg)
                first = False
            elif choice == "0":
                system("cls")
                main()
                break
            else: exit()
    else: print("No results found or invalid selection.")

try:
    system("cls")
    main()
except KeyboardInterrupt:
    print("Exiting")
    exit()