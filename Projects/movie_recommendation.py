bollywood_movies = {
    "action": ["Baahubali: The Beginning", "War", "KGF: Chapter 1",],
    "comedy": ["Hera Pheri", "Andaz Apna Apna", "Munnabhai MBBS"],
    "drama": ["Dangal", "Kabir Singh", "Sita Ramam"],
    "sci-fi": ["Robot", "Ra.One", "Robot 2.0"],
    "romance": ["Dilwale Dulhania Le Jayenge", "Yeh Jawaani Hai Deewani", "Arjun Reddy"],
    "thriller": ["Drishyam", "Kahaani", "Don"],
    "horror": ["Tumbbad", "Stree", "Bhaagamathie"],
    "musical": ["Rockstar", "Aashiqui 2", "Jagga Jasoos"],
    "historical": ["Jodha Akbar", "Padmaavat", "Sye Raa Narasimha Reddy"]
}
hollywood_movies={
    "action": ["Mad Max: Fury Road", "John Wick", "The Dark Knight"],
    "comedy": ["Superbad", "Step Brothers", "The Hangover"],
    "drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather"],
    "sci-fi": ["Inception", "The Matrix", "Interstellar"],
    "romance": ["Titanic", "La La Land", "Pride and Prejudice"],
    "thriller": ["Se7en", "Gone Girl", "Silence of the Lambs"],
    "horror": ["The Exorcist", "Hereditary", "A Quiet Place"],
    "musical": ["The Greatest Showman", "Moulin Rouge!", "Chicago"],
    "historical": ["Schindler's List", "Braveheart", "Gladiator"]
}

def recommend_movie(industry, genre):
    genre = genre.lower()
    industry = industry.lower()

    if industry == "bollywood":
        movies = bollywood_movies
    elif industry == "hollywood":
        movies = hollywood_movies
    else:
        return "Sorry, I don't have information on that movie industry."

    if genre in movies:
        return f"Here are some {industry.capitalize()} {genre} movies you might enjoy: {', '.join(movies[genre])}."
    else:
        return f"Sorry, I don't have any {industry.capitalize()} recommendations for that genre."
