import sqlite3
import objecttier

##
##Program uses MovieLens.db data file data to output certain data based on user input
##Program acknowledges that some of the tables in the file have None values
##

##Function outputs movie titles, movie id, and the release date of the user's chosen movie
##Function limits output to 100
def movie_match(dbConn):
  print('\n')
  movie_input = input("Enter movie name (wildcards _ and % supported): ")

  num_movies = []
  num_movies = objecttier.get_movies(dbConn, movie_input)

  #Safety check to catch errors
  if num_movies is None:  
      print("No such movie...")
  elif num_movies == 0:
      print('\n')
      print("# of movies found: ", len(num_movies), "\n")
  elif len(num_movies) > 100: #Only want to output 100 movies
      print('\n')
      print("# of movies found: ", len(num_movies), "\n")
      print("There are too many movies to display, please narrow your search and try again...")
  else: #if no errors then output data
      print('\n')
      print("# of movies found: ", len(num_movies), "\n")
      for s in num_movies:
          print(s.Movie_ID, " : ", 
                s.Title, 
                f"({s.Release_Year})")

############################################################
##End of movie_match
#
#
#Function outputs the details of a movie based on user selection via the Movie_ID 
#Function also checks if the movie exists or not
def movie_details(dbConn):
  print('\n')
  movie_info = input("Enter movie id: ")

  movieinfodump = []
  a = objecttier.get_movie_details(dbConn, movie_info)
  movieinfodump.append(a)

  #Safety check to catch errors
  if movieinfodump[0] is None:
      print('\n')
      print("No such movie...")
  elif movieinfodump == ():
      print('\n')
      print("No such movie...")
  elif len(movieinfodump) == 0:
      print('\n')
      print("No such movie...")  
  else: #If no errors output data
      print('\n')

      for s in movieinfodump:
        print(s.Movie_ID, ":", 
              s.Title)
              
        print("  Release date: ", s.Release_Date, "\n",
              " Runtime: ", s.Runtime, "(mins)",  "\n",
              " Orig language: ", s.Original_Language,  "\n",
              " Budget: ", f"${s.Budget:,}", " (USD)",  "\n",
              " Revenue: ", f"${s.Revenue:,}", "(USD)", "\n",
              " Num reviews: ", s.Num_Reviews, "\n",
              " Avg rating:", f"{s.Avg_Rating:.2f}", "(0..10)")

      #Outputting lists of Genre and Companies inside main list movieinfodump
      print("  Genres: ", end="")
      for genre in s.Genres:
          print(genre, end=", ")

      print("\n", " Production companies: ", end="")
      for companies in s.Production_Companies:
          print(companies, end=", ")
     
      print("\n", " Tagline: ", s.Tagline)
  

########################################################
#end of movie_details
#
#
#Function outputs top movies with rating based on user selection
#For example, the user can select to pick the top 10 movies with a rating of 50
def top_movies(dbConn):
  print('\n')

  #Safety check to make sure the input is above 0 for both top_num and review_input
  top_num = input("N? ")
  if int(top_num) <= 0:
    return print("Please enter a positive value for N...")
 
  review_input = input("min number of reviews? ")
  if int(review_input) <= 0: 
    return print("Please enter a positive value for min number of reviews...")
    

    
  top_reviewdump = []
  top_reviewdump = objecttier.get_top_N_movies(dbConn, int(top_num), int(review_input))
  
  #If top_reviewdump returns none or 0 then there will be no output
  if top_reviewdump is None:  # error
     return
  elif len(top_reviewdump) == 0:
     return
  else:
      print('\n')

      for s in top_reviewdump:
        print(s.Movie_ID, ":", 
              s.Title,
              f"({s.Release_Year}), ",
              "avg rating = ", f"{s.Avg_Rating:.2f}",
              f" ({s.Num_Reviews} reviews)")
        

########################################
#end of top_movies
#
#
#Function is outputting whether or not a new rating for a movie was succeessfully inserted
#Function also lets you know whether the movie specified exists or not
def insert_rating(dbConn):
  print('\n')

  rating_input = input("Enter rating (0..10): ")

  #Safety checks to make sure rating_input is between 0-10 range
  if int(rating_input) < 0:
    return print("Invalid rating...")

  if int(rating_input) > 10:
    return print("Invalid rating...")

  movieid_input = input("Enter movie id: ")

  rating_change = objecttier.add_review(dbConn, int(movieid_input), int(rating_input))

  #Safety check to output successbased on rating_change data
  if rating_change == 0:
    print('\n')
    print("No such movie...")
  else:
    print('\n')
    print("Review successfully inserted")

########################################################################################
# end of insert_rating 
#
#
#Function outputs whether tagline for movie was successfully updated or inserted
#Function also checks if chosen movie exists or not
def modify_tagline(dbConn):
  print('\n')

  tagline_input = input("tagline?")

  movieid_input = input(" movie id?")

  print('\n')
  #set_tagline returns 1 or 0 to indicate success
  tagline_change = objecttier.set_tagline(dbConn, movieid_input, tagline_input)
  
  #Outputting data based on tagline_change data
  if int(tagline_change) == 1:
    print("Tagline successfully set")
  else:
    print("No such movie...")

####################################################
#end of modify_tagline
#
#
#Function displays general statistics of the data file
def print_stats(dbConn):
  

  print("General stats:")

  num_movies = objecttier.num_movies(dbConn)
  num_reviews =  objecttier.num_reviews(dbConn)

  
  print("  # of movies: ", f"{num_movies:,}")
  print("  # of reviews: ", f"{num_reviews:,}")

  
##################################################################
#
# main
#
print('** Welcome to the MovieLens app **\n')

dbConn = sqlite3.connect('MovieLens.db')

print_stats(dbConn)

user_input = ''

# While loop that runs until user clicks "x" to  exit. Error message displayed if user picks anything outside of the given choices
while user_input != 'x':
    print('\n')
    user_input = input("Please enter a command (1-5, x to exit):")

    if user_input == '1':
      movie_match(dbConn)
    elif user_input == '2':
      movie_details(dbConn)
    elif user_input == '3':
      top_movies(dbConn)
    elif user_input == '4':
      insert_rating(dbConn)
    elif user_input == '5':
      modify_tagline(dbConn)
    elif user_input == 'x':
        user_input == 'x'
    else:
        print(" **Error, unknown command, try again...")

dbConn.close()

#
# done
#