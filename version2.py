import requests  # importing the request library

VALID_API_KEY = "brian123"  # setting up an Api Key
user_api_key = None  # stores what the user types when asked for their key

saved_words = []  # where saved words will be stored

# checking for correct entries
def verify_api_key():
    global user_api_key
    if user_api_key != VALID_API_KEY:
        print("INVALID CREDENTIAL")
        return False
    return True

def search_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}" # Use f-string for URL
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            # Check if 'meanings' key exists and is a list
            if 'meanings' in data[0] and isinstance(data[0]['meanings'], list) and len(data[0]['meanings']) > 0:
                meanings = data[0]['meanings'] # Correctly access 'meanings' key
                if 'definitions' in meanings[0] and isinstance(meanings[0]['definitions'], list) and len(meanings[0]['definitions']) > 0:
                    definitions = meanings[0]['definitions'] # Correctly access 'definitions'
                    # Take the first definition's 'definition' text
                    return definitions[0]['definition']
        return "No definition found (structure mismatch)." # Fallback if structure is unexpected
    elif response.status_code == 404:
        return "No definition found."
    else:
        return "Error while fetching the definition."

def add_word(word, word_id): # should enter the such word and the word_id
    if not verify_api_key(): # verifys if the key is correct
        return
    definition = search_word(word)
    entry = {"id": word_id, "word": word, "definition": definition} # Changed 'definitions' to 'definition' for consistency

    saved_words.append(entry) # adds the suched word to the list
    print(f"'{word}' saved successfully with definition: {definition}") # Indicate what was saved

def view_words():
    if not verify_api_key():
        return
    if not saved_words: # Corrected: Check if list is empty
        print("No saved words.")
        return
    for entry in saved_words: # loops through
        print(f"\nID: {entry['id']}\nWord: {entry['word']}\nDefinition: {entry['definition']}") # Corrected 'definition' access

def update_word(word_id, new_word): # find a word using its id
    if not verify_api_key():
        return
    found = False # Flag to check if word was found
    for entry in saved_words: # Corrected: Iterate over the list directly
        if entry["id"] == word_id: # confirms for the word_id if present
            entry["word"] = new_word
            entry["definition"] = search_word(new_word) # Fetch new definition for the new word
            print(f"Word ID {word_id} updated to '{new_word}' with new definition: {entry['definition']}")
            found = True
            break # Exit loop once updated
    if not found:
        print("Word ID not found.")

def delete_word(word_id): # Removes an entry with a specific id using list compression
    if not verify_api_key():
        return
    global saved_words
    initial_length = len(saved_words)
    saved_words = [entry for entry in saved_words if entry["id"] != word_id] # this creates a new list that keeps every item except the one with the matching ID
    if len(saved_words) < initial_length:
        print(f"Word ID {word_id} deleted successfully.")
    else:
        print(f"Word ID {word_id} not found.")

def clear_words():
    if not verify_api_key():
        return
    saved_words.clear() # removes everything from the list
    print("All words cleared.")

def main():
    global user_api_key
    print("Welcome to Smart Dictionary API Tool")

    user_api_key = input("Enter Your API Key: ")

    while True:
        print("\n--- Menu ---")
        print("1. Search and save a word")
        print("2. View Saved words")
        print("3. Update a word")
        print("4. Delete a Word")
        print("5. Clear All words") # Corrected menu number
        print("6. Exit")

        choice = input("Choose an option 1-6: ")
        if choice == "1":
            word = input("Enter the word: ")
            # Check if word already exists by ID to avoid duplicates or prompt differently
            word_id = int(input("Enter a unique ID for this word: "))
            add_word(word, word_id)
        elif choice == "2":
            view_words()
        elif choice == "3":
            word_id = int(input("Enter ID of the word to update: "))
            new_word = input("Enter the new word: ") # Prompt for new_word
            update_word(word_id, new_word)
        elif choice == "4":
            word_id = int(input("Enter ID of the word to delete: "))
            delete_word(word_id)
        elif choice == "5":
            clear_words()
        elif choice == "6":
            print("Exiting Smart Dictionary Tool.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()