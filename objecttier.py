
# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  #Constructor
  def __init__(self, id, title, year): 
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year
  
  
  ###Methods
  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year




##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
   #Constructor
  def __init__(self, id, title, year, reveiews, ratings): 
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year
    self._Num_Reviews = reveiews
    self._Avg_Rating = ratings
  
  
  ###Methods
  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating



##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  # Constructor
  def __init__(self, id, title, date, time, language, budget, revenue, reveiews, ratings, tagline, genres, companies): 
    self._Movie_ID = id
    self._Title = title
    self._Release_Date = date
    self._RunTime = time
    self._Original_Language = language
    self._Budget = budget
    self._Revenue = revenue
    self._Num_Reviews = reveiews
    self._Avg_Rating = ratings
    self._Tagline = tagline
    self._Production_Companies = companies
    self._Genres = genres
  
  
 ###Methods
  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._RunTime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating

  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Production_Companies(self):
    return self._Production_Companies

  @property
  def Genres(self):
    return self._Genres


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  
  sql = """Select count(*)
           From Movies;"""

  s_row = datatier.select_one_row(dbConn, sql)

  #Safety check to catch None case that could lead to an error
  if s_row is None:
    return -1;
    
  return s_row[0]



##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  sql = """Select count(*)
           From Ratings;"""

  
  s_row = datatier.select_one_row(dbConn, sql)

  #Safety check to catch None case that could lead to an error
  if s_row is None:
    return -1;

    
  return s_row[0]
  
  


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  
  sql2 = """Select Movies.Movie_ID, Title, strftime('%Y', Release_Date)
           From Movies
           where Title like ?
           Group by Movies.Movie_ID
           Order by Movies.Movie_ID asc;"""

  m_row = datatier.select_n_rows(dbConn, sql2, [pattern])
  movieslist = []
  for row in m_row:
    a = Movie(row[0], row[1], row[2]);
    movieslist.append(a)

  #Safety check to see if movieslist is empty
  if not movieslist:
    return  []

  #Return list of object data
  return movieslist
    
  

  


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
#Multiple sql commands had to be created in order to address that some commands would produce a list of data and 
#some would just be one output. Multiple sql commands also made it easier to address None case
  sql1 = """Select count(Rating), avg(Rating)
            From Ratings
            Where Movie_ID like ?;"""
  
  m_row = datatier.select_one_row(dbConn, sql1, [movie_id])

   #Safety check to catch None in total and avg rating and converting it to 0 so data can still be used
  if m_row[0] is None or m_row[0] == () or m_row[1] is None or m_row[1] == ():
     temp = list(m_row)
     temp[1] = 0
     m_row = tuple(temp)

  
  sql2 = """Select Movies.Movie_ID, Title, DATE(Release_Date), Runtime, 
            Original_Language, Budget, Revenue, Tagline 
            From Movies
            Left Join Ratings
            on Movies.Movie_ID = Ratings.Movie_ID
            Left Join Movie_Taglines
            on Movies.Movie_ID = Movie_Taglines.Movie_ID
            Where Movies.Movie_ID like ?;"""

  m_row2 = datatier.select_one_row(dbConn, sql2, [movie_id])

  if m_row2 is None or len(m_row2) < 8:
         return None;

  #Safety check to catch tagline that is None and converting it to "" so data can still be used
  if m_row2 is None or m_row2 == () or m_row2[7] is None:
     temp1 = list(m_row2)
     temp1[7] = ""
     m_row2 = tuple(temp1)

  #Sql command creates a list of genres that will be put in a list and later appended to an object  
  sql3 = """Select Genre_Name
            From Genres
            Join Movie_Genres
            on Genres.Genre_ID = Movie_Genres.Genre_ID
            Where Movie_Genres.Movie_ID = ?
            Order by Genre_Name asc;"""

  m_row3 = datatier.select_n_rows(dbConn, sql3, [movie_id])
  
  
  if m_row3 is None:
    return None

  genrelist = []
    
  for rows in m_row3:
    genrelist.append(rows[0])

  #Sql command creates a list of companies that will be put in a list and later appended to an object  
  sql4 =""" Select Company_Name
            From Companies
            Join Movie_Production_Companies
            on Companies.Company_ID = Movie_Production_Companies.Company_ID
            Where Movie_Production_Companies.Movie_ID = ?
            Order by Company_Name asc;"""

  m_row4 = datatier.select_n_rows(dbConn, sql4, [movie_id])
  
  
  if m_row4 is None:
    return None

  companylist = []
    
  for rows in m_row4:
    companylist.append(rows[0])
      
  ##Adding all the data from the prvious sql commands
  a = MovieDetails(m_row2[0], m_row2[1], m_row2[2], m_row2[3], m_row2[4], m_row2[5], 
                     m_row2[6], m_row[0], m_row[1], m_row2[7], genrelist, companylist)

    
  #Returning an Object of data  
  return a


      

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
   sql = """Select Movies.Movie_ID, Title, strftime('%Y', Release_Date), 
            count(Rating), AVG(Rating)
            From Movies
            Join Ratings
            on Movies.Movie_ID = Ratings.Movie_ID
            Group by Movies.Movie_ID
            Having count(Rating) >= ?
            Order by avg(Rating) desc
            limit ? """
  
   parameter_list = [min_num_reviews, N]

   m_row = datatier.select_n_rows(dbConn, sql, parameter_list)

  #Safety check to catch None case
   if m_row is None:
    return None
  
   movieslist = []
   for row in m_row:
    a = MovieRating(row[0], row[1], row[2], row[3], row[4]);
    movieslist.append(a)

   #Returing a list of MovieRating Object Data
   return movieslist

##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  sql = """Select Movies.Movie_ID
           From Movies
           Where Movies.Movie_ID is ?""" 

  m_row = datatier.select_one_row(dbConn, sql, [movie_id])

  # Checking if movie_id exists if not return 0
  if m_row is None or m_row == ():
    return 0

  
  sql1 = """Insert Into Ratings(Movie_ID, Rating) values(?, ?);"""

  parameter_list = [movie_id, rating]
  
  # Since movie_id does exist continue with inserting rating
  modified = datatier.perform_action(dbConn, sql1, parameter_list)
  
  #if modified is -1, none, or () then that means adding review was unsuccessful
  if modified == -1:
    return 0
  
  return modified

##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  sql = """Select Title 
           From Movies
           Where Movie_ID is ?""" 

  m_row = datatier.select_one_row(dbConn, sql, [movie_id])

  # Checking if the movie_id exists, if not it will return 0
  if len(m_row) == 0:
    return 0;

  # Checking if tagline is none
  m_row2 = datatier.select_one_row(dbConn, "Select Tagline From Movie_Taglines Where Movie_ID is ?", [movie_id])

  #Since there is no tagline, insert a new tagline
  if len(m_row2) == 0:
    sql1 = """Insert Into Movie_Taglines(Movie_ID, Tagline) values(?, ?);"""

    parameter_list = [movie_id, tagline]
    modified = datatier.perform_action(dbConn, sql1, parameter_list)
  else:
    
    sql1 = """Update Movie_Taglines
              Set Tagline = ?
              Where Movie_ID = ?"""
    parameter_list = [tagline, movie_id]
    modified = datatier.perform_action(dbConn, sql1, parameter_list)


  # if modified has a value greater than zero then setting tagline was successful
  if modified > 0:
    return 1
  else: #unsuccessful at adding tagline
    return 0 

#########################################
##End of objecttier