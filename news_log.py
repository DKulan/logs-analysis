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
        print("Unable to connect to database")
        sys.exit(1)


def generate_views():
    """ This function generates three views in the database """
    # Connect to database
    db, c = connect(DB)

    # -- Question 1 --
    c.execute("SELECT * FROM top_articles;")
    print("Most popular articles:")
    for(title, views) in c.fetchall():
        print("{}  -  {} views".format(title, views))
    print("\n\n")

    # -- Question 2 --
    c.execute("SELECT * FROM top_authors;")
    print("Most popular authors:")
    for(name, views) in c.fetchall():
        print("{}  -  {} views".format(name, views))
    print("\n\n")

    # -- Question 3 --
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
