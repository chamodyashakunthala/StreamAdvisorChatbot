import pickle


with open("stream_selection_model.pkl", "rb") as f:
    model, feature_names = pickle.load(f)


print(" Hi! I’m your A/L Stream Advisor Chatbot.")
print("I’ll ask about your interest in subjects (1 = Low, 5 = High).")
print("At the end, I’ll also ask your overall interest area.\n")

while True:  

    
    subjects = ["Maths", "Science", "English", "Sinhala", 
                "ICT", "History", "Commerce", "Buddhism"]

    inputs = []
    for subject in subjects:
        while True:
            try:
                rating = int(input(f" How much do you like {subject}? (1–5): "))
                if 1 <= rating <= 5:
                    inputs.append(rating * 20)  
                    break
                else:
                    print(" Please enter a number between 1 and 5.")
            except ValueError:
                print(" Invalid input! Please enter a number between 1 and 5.")

    
    interest_options = ["Science", "Maths", "Commerce", "Arts", "Technology"]
    print("\n What is your overall main interest?")
    for i, opt in enumerate(interest_options, 1):
        print(f"{i}. {opt}")

    while True:
        try:
            chosen = int(input(" Enter the number (1–5): "))
            if 1 <= chosen <= 5:
                break
            else:
                print(" Please enter a number between 1 and 5.")
        except ValueError:
            print(" Invalid input! Enter a number between 1 and 5.")

    interest = interest_options[chosen-1]

    
    input_dict = {feature: 0 for feature in feature_names}

    
    for i, subject in enumerate(subjects):
        input_dict[subject] = inputs[i]

    
    interest_col = "Interest_" + interest
    if interest_col in input_dict:
        input_dict[interest_col] = 1

    
    input_data = [input_dict[f] for f in feature_names]

    
    prediction = model.predict([input_data])[0]

   
    print("\n Based on your answers, I recommend you choose:")
    print(f" **{prediction} Stream** ")
    print("\n(Remember: this is just a suggestion — the final choice is yours!) ")

    
    again = input("\nDo you want to check another student? (yes/no): ").strip().lower()
    if again != "yes":
        print("\n Thank you for using the Stream Advisor Chatbot! Goodbye!")
        break
