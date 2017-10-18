*LOGS ANALYSIS* - UDACITY PROJECT

 Description:  This project showcases the ability to use PostgreSQL queries in python. 
              The program generates VIEWS that can be used to display statistical information
              for a news database.
 
 Requirements:
 - Python 3x
 - Psycopg2
 - PostgreSQL 9.6
 - "News" database file (download: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)


 To Run:
 1. Load the data onto the database
	      psql -d news -f newsdata.sql
 
 2. Generate the views from file
       	      psql -d news -f create_views.sql
 
 3. Connect to the database 
              psql -d news

 4. Run the Python file
              python news_log.py

 5. You should now see the output of the queries!


# Queries used:
          

# Generate view to list the top articles

              CREATE VIEW top_articles AS
              SELECT title, count(title) AS views
              FROM articles, log
              WHERE log.path LIKE CONCAT('%', articles.slug)
              GROUP BY title
              ORDER BY views DESC
              LIMIT 3;


# Generate view to list the top authors

    	      CREATE VIEW top_authors AS
              SELECT name, count(title) AS views
              FROM articles, authors, log
              WHERE authors.id = articles.author
              AND log.path LIKE CONCAT('%', articles.slug)
              GROUP BY name
              ORDER BY views DESC;


# Generate view to list total requests for single day
              CREATE VIEW requests AS
              SELECT count(*) as req, date(time) AS date
              FROM log
              GROUP BY date
              ORDER BY req DESC;


# Generate view to display requests that are not OK
              CREATE VIEW err_requests AS
              SELECT count(*) as req, date(time) AS date
              FROM log
              WHERE status != '200 OK'
              GROUP BY date
              ORDER BY req DESC;


# Generate view to display percentage of errors for a given day
              CREATE VIEW err_percent AS
              SELECT requests.date,
              round((100.0*err_requests.req)/requests.req,2) AS perc
              FROM requests, err_requests
              WHERE err_requests.date = requests.date
              GROUP BY requests.date, err_requests.req, requests.req;


# Generate view to display the day with the most errors
              CREATE VIEW most_errors AS
              SELECT *
              FROM err_percent
              WHERE err_percent.perc > 1
              ORDER BY err_percent.perc DESC; 
