from requests import get
from os import system

try:
    def jsondata():
        url = "https://biggamesapi.io/api/collection/eggs" # open api https://docs.biggames.io
        response = get(url)
        data = response.json()
        return data

    def search(search_term, jsoninf):
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
            selection = int(input("Enter the number of the egg you want to use: ")) - 1
            if 0 <= selection < len(results):
                selected_egg = results[selection]
            else:
                print("Invalid selection.")
                return None
        elif results:
            selected_egg = results[0]
        else:
            print("No matches found.")
            return None

        # display the selected egg with all its pets
        if selected_egg:
            pets = ', '.join([f"{pet[0]} (Chance: {pet[1]}%)" for pet in selected_egg['configData']['pets']])
            print(f"Selected Egg '{selected_egg['configName']}' contains pets: {pets}")
            return selected_egg

    def main():
        searchterm = input("Enter the name of the pet you want to search for: ")
        selected_egg = search(searchterm, jsondata())
        if selected_egg:
            print(f"Selected Egg: '{selected_egg['configName']}'")
            system("cls")
            for pet in selected_egg['configData']['pets']:
                chance_standard_notation = "{:.10f}".format(float(pet[1]))
                chance_standard_notation = chance_standard_notation.rstrip('0').rstrip('.')
                print(f"Pet: '{pet[0]}' with a chance of {chance_standard_notation}%")
            if input("\n\nPress enter to exit.\ntype 1 to search again:") == "1":
                main()
        else:
            print("No results found or invalid selection.")

    if __name__ == "__main__":
        main()
except KeyboardInterrupt: # Made this so the exe doesn't consider it an uncaught exception :> (also it looks nicer)
    print("Exiting")
    exit()