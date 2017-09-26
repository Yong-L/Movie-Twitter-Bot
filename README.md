# Movie Twitter

Simple bot to send back the user the closest theater of the movie you want to watch

The program first finds the tt_id from the IMDB
Then the program queries the website with zipcode and tt_id from showtime
It then picks the first theater that comes up and then goes into the theater website
which then searches for the movie once again and finally gets the showtime and returns the mention to user

## Instructions

First edit the secrets.py file with your credentials on your Twitter API
Change the @mentions in the secrets.py as well to your own twitter username
Run the bots.py on your local machine or on a python server to run the bot 
