import pandas as pd
import re

#This reads the dataset into the pandas DataFrame
df = pd.read_csv("data/IMDB_Dataset.csv")
df.head()

#Creates a column called "review_length"
df["review_length"] = df["review"].str.split().str.len()

#These are the most common words that are filler
stop_words = {
    "the", "and", "that", "this", "with", "from", "would", "there",
    "their", "about", "which", "could", "should", "these", "those",
    "have", "has", "were", "been", "when", "where", "while", "your",
    "very", "just", "into", "over", "than", "then", "them", "they", 
    "movies", "movie", "because", "really"
}

#This is the main menu
while True:
    print('Welcome to the Movie Review Central!')
    print('Please choose from the options below(1-8):')

    print('1. Show on average how many characters are in positive versus negative reviews')
    print('2. Show the top 10 words used in positive reviews.')
    print('3. Show the top 10 words used in negative reviews.')
    print('4. Find a the reviews containing a certain word.') #This will be my filter
    print('5. Sort showing the longest reviews first.')#This will be my sort
    print('6. Sort showing the shortest reviews first. ')#This will also be sort
    print('7. Analyze and find out if positive or negative reviews are more emotional')#Aggregation - collecting and summarizing how emotional the reviews are
    print('0. Quit')

    choice = int(input(''))

#   This finds out how many characters on average are in postive versus negative reviews.
    if choice == 1:
        #This shows if positive or negative reviews are longer
        print('\nThis shows how many characters are in both positive and negative reviews on average:')
        print(df.groupby("sentiment")["review_length"].mean())

    #This finds the most common words used in positive reviews.
    elif choice == 2:
        # Break all reviews into words
        words = (
        df["review"]
        .str.lower()
        .str.replace(r"[^a-z\s]", "", regex=True)
            .str.split()
        .explode()
        )

        filtered_words = words[
            (words.str.len() > 4) & 
            (~words.isin(stop_words))   
        ]

        filtered_words.value_counts().head(10)

        positive_words = (
        df[df["sentiment"] == "positive"]["review"]
        .str.lower()
        .str.replace(r"[^a-z\s]", "", regex=True)
        .str.split()
        .explode()
        )
        print('These are the top words used in positive reviews:')
        print(positive_words[(positive_words.str.len() > 4) & (~positive_words.isin(stop_words))].value_counts().head(10))

    #This finds the most common words used in negative reviews.
    elif choice == 3:
        # Break all reviews into words
        words = (
        df["review"]
        .str.lower()
        .str.replace(r"[^a-z\s]", "", regex=True)
        .str.split()
        .explode()
        )

        filtered_words = words[
            (words.str.len() > 4) & 
            (~words.isin(stop_words))
        ]

        filtered_words.value_counts().head(10)

        negative_words = (
            df[df["sentiment"] == "negative"]["review"]
            .str.lower()
            .str.replace(r"[^a-z\s]", "", regex=True)
            .str.split()
            .explode()
        )
        print('These are the top words used in negative reviews:')
        print(negative_words[(negative_words.str.len() > 4) & (~negative_words.isin(stop_words))].value_counts().head(10))

    #Stop the program
    elif choice == 0:
        print("Goodbye")
        break

    #Find all the reviews containing a certain word
    elif choice == 4:
        print('This is where we will find all the reviews that contain the word you give us.')
        word = input("Give me a word: ")

        pattern = r"\b" + re.escape(word) + r"\b"

        matching_reviews = df[df["review"].str.lower().str.contains(pattern, regex=True, na=False)]

        print(f"\nFound {len(matching_reviews)} reviews containing '{word}': \n")
        print(matching_reviews[["review", "sentiment"]])

    #Find the longest reviews
    elif choice == 5:
        longest = df.sort_values("review_length", ascending=False)

        print(longest[["review_length", "sentiment", "review"]])

    #Find the shortest reviews
    elif choice == 6:
        shortest = df.sort_values("review_length", ascending=True)

        print(shortest[["review_length", "sentiment", "review"]])

    #Shows how emotional the negative versus positive reviews were
    elif choice == 7:
        emotion_words = {"love", "hate", "amazing", "terrible", "great", "awful"}

        df["contains_emotion"] = df["review"].str.lower().apply(lambda x: any(word in x for word in emotion_words))

        print(df.groupby("sentiment")["contains_emotion"].mean() * 100)
