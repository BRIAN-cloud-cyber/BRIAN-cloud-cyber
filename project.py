
import requests  # importing the request library

VALID_API_KEY="brian123"   #setting up an Api Key
user_api_key=None #stores what the user types when asked for their key

saved_words=[]  # where saved words will be stored

# checking for correct entries
def verify_api_key():
    global user_api_key
    if user_api_key !=VALID_API_KEY:
        print("INVALID CREDENTIAL")
        return False
    return True

def search_word(word):
    url=" https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response=requests.get(url)
    
    if response.status_code==200:
        data=response.json()
        meanings=data[0]("meanings")
        definitions=meanings[0] ["definitions"]
        return definitions[0] ["definitions"]

    elif response.status_code==404:
        return "No definition found"
    else:
        return "Error while fetching the defition "

def add_word(word,word_id):
    if not verify_api_key():
        return
    definition=search_word(word)
    entry={"id":word_id,   "word":word,"definitions":definition}
    

    saved_words.append(entry)
    print(f"'{word}'saved successfully" )


def view_words():
    if not verify_api_key():
        return
    if not saved_words():
        print("No saved words.")
        return
    for entry in saved_words:
        print(f"\n ID:{entry['id']}\n word:{entry['word']}\n definition:{definition}")



def update_word(word_id,new_word):
    if not verify_api_key():
        return
    for entry in saved_words():
        if entry["id"]==word_id:
            entry["word"]=new_word
            entry["definition"]=search_word(new_word)
            print(f"Word ID {word_id} updated")
            return
    print("Word ID not found ")


def delete_word(word_id):
    if not verify_api_key():
        return
    global saved_words
    saved_words=[entry for entry in saved_words if entry["id"] !=word_id]
    print(f"Word ID {word_id} deleted successfully")

def clear_words():
    if not verify_api_key():
        return
    saved_words.clear()
    print("All words cleared.")


def main():
    global user_api_key
    print("welcome to Smart Dictionary Api Tool")

    user_api_key=input("Enter Your Api Key: ")

    while True:
        print("1. Search and save a word")
        print("2. View Saved words ")
        print("3.Update a word")
        print("4.Delete a Word")
        print("Clear All words ")
        print("6.Exit")

        choice=input("Choose an option 1-6: ")
        if choice=="1":
            word=input("Enter the word: ")
            word_id=int(input("Enter A unique ID: "))
            add_word(word,word_id)
        elif choice=="2":
            view_words()

        elif choice=="3":
            word_id=int(input("Enter ID to update"))
            update_word(word_id,new_word)

        elif choice=="4":
            word_id=int(input(" Enter ID to delete:  "))
            delete_word(word_id)
        
        elif choice=="5":
            clear_words()

        elif choice=="6":
            print("Exiting Smart Dictionary Tool.")
            break
        else:
            print("Invalid option.Try again.")

if __name__=="__main__":
    main()




    
    



