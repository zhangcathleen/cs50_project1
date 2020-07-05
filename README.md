# Project 1

"""Web Programming with Python and JavaScript

Creating a website to rate and review books using the GoodRead API, PostGreSQL, Heroku, and Flask"""

Hello!

I hope yall are having a fabulous day. This is my version of Project 1 - Web Programming with Python and Javascript.

1. Index Page
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
   If the username already exists:

   - Error message - saying username already exists : stays on this page
     Else:
   - Account is registered and will give you a link to login (redirect to Page 1)

3. Main Page
   Displays buttons to go to either all books/reviews or form to review book
