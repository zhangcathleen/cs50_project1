# Project 1

"""Web Programming with Python and JavaScript

Creating a website to rate and review books using the GoodRead API, PostGreSQL, Heroku, and Flask"""

Hello!

I hope yall are having a fabulous day. This is my version of Project 1 - Web Programming with Python and Javascript.

1. Index Page
   index()
   If you are not logged in:

   - Login to the Potato Book Reviews - if you don't have an account, you can register for an account (redirected to Page 2)
     **Currently, the login uses plaintext + SQL without any protection - more research is needed for a more secure login**

     - If the login and/or password is incorrect or doesn't exist:
       Error message - saying the username/password doesn't exist : stays on this page
       **I was toying with the idea of having separate messages for if the username doesn't exist, but I don't think this would be very secure**

     - Else:
       Login to a middle page where you can either logout or proceed (redirected to Main Page 3)

   * Else:
     You are redirected to the Main page 3

2. Register Page
   register()
   If the username already exists:

   - Error message - saying username already exists : stays on this page
     Else:
   - Account is registered and will give you a link to login (redirect to Page 1)

3. Main Page
   main()
   Displays buttons to go to either all books/reviews or form to review book

4. Displays Page
   a. display()
   Lists all of the Books
   b. results(vooks,search)
   Lists all the Books from the search in (a)

5. Book Information Page
   books(isbn)
   Lists all of the information for a specific book

6. Book Review Page
   form(\*args)
   Allows you to review the selected book w/ the corresponding isbn number
   If the method is a POST:

   - The form is being submited
   - Checks if this book is in the database
   - If the user has already submitted a review for this book:
     - User is redirected to Edit page (page 7) with the isbn number + previous rating + previous review filled out
       **Should the Edit page have the old or new review + ratings?**
   - If the user has not submitted a review for this book:
     - The user's review is submitted into the database
     - Taken to Submission page (Page 8), is linked to the Book Info Page (Page 5)
       **Work on submitting the reviw from book results or just a brand new form**

7. Book Edit Page
   Allows you to edit your review for a book you have already reviewed

   Check if the book has been reviewed or not:

   - If not - redirets to a form
     **Needs to be able to display the message in the form instead of the url**
     Checks if the book is in the database:

   - If not - redirects to an error page
   - Should be, because the only way to get to this page is from the form page of a book that you have already reviewed
     **Need to do something like the @login_required, so that you can only get there if you have already reviewed this books**
   - Reidrects to edit_review() - which updates the review + rating in the database

8. Submission Success Page
   Returns a success message if the submission has been successful

9. API Page
   Returns a json with information on this book:
   - title
   - author
   - year published
   - isbn
   - the number of reviews
   - the average rating
