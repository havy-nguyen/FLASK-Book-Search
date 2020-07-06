## FLASK - SQLAlchemy - Book review website
[Third party API: Goodreads](https://www.goodreads.com/api)

##### Registration 
```bash
Users should be able to register, providing (at minimum) a username and password.
```

##### Login 
```bash
Users, once registered, should be able to log in username and password.
```

##### Logout
```bash
Logged in users should be able to log out of the site.
```

##### Import books 
[CSV file of 5000 different books.](https://github.com/havy-nguyen/csv-to-postgresql).
```bash
Each one has an ISBN number, a title, an author, and a publication year. 
```

##### Search 
```bash
Once a user has logged in, they can search for a book. 
Users can type in the ISBN number of a book, the title of a book, or the author of a book.
After performing the search, a list of possible matching results is displayed. 
Users can type in only part of a title, ISBN, or author name.
```

##### Book Page 
```bash
From the results of the search page, users are taken to a book page. 
Details about the book: 
- Its title, author. 
- Publication year. 
- ISBN number. 
- Any reviews and rating that users have left. 

Users are be able to submit a review for each book together with a rating scale.
(1 to 5 stars)
```

##### Goodreads Review Data 
```bash
Average rating and number of ratings from Goodreads are displayed on each book page.
```

##### API Access 
```bash
Users can make a GET request (.../index/api/<isbn> route) for a JSON response.
A JSON response contains: 
- The book’s title.
- Author. 
- Publication year.
- ISBN number. 
- Review count.
- Average review score.
```
###### JSON format example
```bash
{
    "title": "The Dark Is Rising",
    "author": "Susan Cooper",
    "year": 1973,
    "isbn": "1416949658",
    "review_count": 28,
    "average_score": 5.0
}
```
