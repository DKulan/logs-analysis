import psycopg2


DB = "news"


def generate_views():
    """ This function generates three views in the database """
    # Connect to database
    db = psycopg2.connect(database=DB)
    c = db.cursor()

    # Generate view to list the top articles
    c.execute("CREATE VIEW top_articles AS "
              "SELECT title, count(title) AS views "
              "FROM articles, log "
              "WHERE log.path LIKE CONCAT('%', articles.slug)"
              "GROUP BY title "
              "ORDER BY views DESC "
              "LIMIT 3; ")

    # Generate view to list the top authors
    c.execute("CREATE VIEW top_authors AS "
              "SELECT name, count(title) AS views "
              "FROM articles, authors, log "
              "WHERE authors.id = articles.author "
              "AND log.path LIKE CONCAT('%', articles.slug) "
              "GROUP BY name "
              "ORDER BY views DESC; ")

    # Generate view to list total requests for single day
    c.execute("CREATE VIEW requests AS "
              "SELECT count(*) as req, date(time) AS date "
              "FROM log "
              "GROUP BY date "
              "ORDER BY req DESC;")

    # Generate view to display requests that are not OK
    c.execute("CREATE VIEW err_requests AS "
              "SELECT count(*) as req, date(time) AS date "
              "FROM log "
              "WHERE status != '200 OK' "
              "GROUP BY date "
              "ORDER BY req DESC;")

    # Generate view to display percentage of errors for a given day
    c.execute("CREATE VIEW err_percent AS "
              "SELECT requests.date, "
              "round((100.0*err_requests.req)/requests.req,2) AS perc "
              "FROM requests, err_requests "
              "WHERE err_requests.date = requests.date "
              "GROUP BY requests.date, err_requests.req, requests.req; ")

    # Generate view to display the day with the most errors
    c.execute("CREATE VIEW most_errors AS "
              "SELECT requests.date, err_percent.perc "
              "FROM requests, err_percent, err_requests "
              "WHERE err_percent.perc > 1 "
              "LIMIT 1; ")

    # Commit and close database
    db.commit()
    db.close()


if __name__ == "__main__":
    generate_views()
