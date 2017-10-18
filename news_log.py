#!/usr/bin/python3
import psycopg2
import sys
import time


DB = "news"


def connect(db_name):
    """Connect to PostgreSQL database. Return connection"""
    try:
        db = psycopg2.connect("dbname={}".format(db_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)


def generate_views():
    """ This function generates three views in the database """
    # Connect to database
    db, c = connect(DB)

    # -- Question 1 --
    # Generate view to list the top articles
    c.execute("CREATE VIEW top_articles AS "
              "SELECT title, count(title) AS views "
              "FROM articles, log "
              "WHERE log.path LIKE CONCAT('%', articles.slug)"
              "GROUP BY title "
              "ORDER BY views DESC "
              "LIMIT 3; ")
    c.execute("SELECT * FROM top_articles;")
    print("Most popular articles:")
    for(title, views) in c.fetchall():
        print("{}  -  {} views".format(title, views))
    print("\n\n")

    # -- Question 2 --
    # Generate view to list the top authors
    c.execute("CREATE VIEW top_authors AS "
              "SELECT name, count(title) AS views "
              "FROM articles, authors, log "
              "WHERE authors.id = articles.author "
              "AND log.path LIKE CONCAT('%', articles.slug) "
              "GROUP BY name "
              "ORDER BY views DESC; ")
    c.execute("SELECT * FROM top_authors;")
    print("Most popular authors:")
    for(name, views) in c.fetchall():
        print("{}  -  {} views".format(name, views))
    print("\n\n")

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

    # -- Question 3 --
    # Generate view to display the day with the most errors
    c.execute("CREATE VIEW most_errors AS "
              "SELECT * "
              "FROM err_percent "
              "WHERE err_percent.perc > 1 "
              "ORDER BY err_percent.perc DESC; ")
    c.execute("SELECT * FROM most_errors;")
    print("Days with > 1% of requests resulting in errors")
    for(date, perc) in c.fetchall():
        print("{}  -  {}% errors".format(date.strftime("%B %d, %Y"), perc))
    print("\n\n")

    # Commit and close database
    db.commit()
    db.close()


if __name__ == "__main__":
    generate_views()
