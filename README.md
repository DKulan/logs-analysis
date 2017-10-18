*LOGS ANALYSIS* - UDACITY PROJECT

 Description:  This project showcases the ability to use PostgreSQL queries in python. 
              The program generates VIEWS that can be used to display statistical information
              for a news database.

 To Install:   simply execute the python file in CML by using "python news_log.py", the views
              should now be created in the "news" database and can be accessed by using the command:
              
              select * from top_articles; // for the top articles view
              select * from top_authors;  // for the top authors view
              select * from requests;     // for the requests view
              select * from err_requests; // for total error requests view
              select * from err_percent;  // for total error requests in percentage view
              select * from most_errors;  // for the day with the most errors view


 Queries used: 
          

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
              FROM log "
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
              SELECT requests.date, err_percent.perc
              FROM requests, err_percent, err_request
              WHERE err_percent.perc > 1
              LIMIT 1;
