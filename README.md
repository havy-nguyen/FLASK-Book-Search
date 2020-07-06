## FLASK - SQLAlchemy - Book review website
[Third party API: Goodreads](https://www.goodreads.com/api)

###### Registration 
```bash
Users should be able to register, providing (at minimum) a username and password.
```

###### Login 
```bash
Users, once registered, should be able to log in username and password.
```

###### Logout
```bash
Logged in users should be able to log out of the site.
```

###### Import books 
```bash
[CSV file of 5000 different books.](https://github.com/havy-nguyen/csv-to-postgresql). Each one has an ISBN number, a title, an author, and a publication year. 
```

###### Search 
```bash
Once a user has logged in, they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. > After performing the search, a list of possible matching results is displayed. Users can type in only part of a title, ISBN, or author name.
```

###### Book Page 
```bash
When clicking on a book from the results of the search page, users are taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews and rating that users have left for the book. Users are be able to submit a review as a text component for each book together with a rating scale from 1 to 5 stars. 
```

###### Goodreads Review Data 
```bash
The average rating and number of ratings from Goodreads are also displayed on each book page.
```

###### API Access 
```bash
When users make a GET request to the site as .../index/api/<isbn> route, where <isbn> is an ISBN number, a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score will be displayed.
```
