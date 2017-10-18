CREATE VIEW top_articles AS
SELECT title, count(title) AS views
FROM articles, log
WHERE log.path LIKE CONCAT('%', articles.slug)
GROUP BY title
ORDER BY views DESC
LIMIT 3;

CREATE VIEW top_authors AS
SELECT name, count(title) AS views
FROM articles, authors, log
WHERE authors.id = articles.author
AND log.path LIKE CONCAT('%', articles.slug)
GROUP BY name
ORDER BY views DESC;

CREATE VIEW requests AS
SELECT count(*) as req, date(time) AS date
FROM log
GROUP BY date
ORDER BY req DESC;

CREATE VIEW err_requests AS
SELECT count(*) as req, date(time) AS date
FROM log
WHERE status != '200 OK'
GROUP BY date
ORDER BY req DESC;

CREATE VIEW err_percent AS
SELECT requests.date,
round((100.0*err_requests.req)/requests.req,2) AS perc
FROM requests, err_requests
WHERE err_requests.date = requests.date
GROUP BY requests.date, err_requests.req, requests.req;

CREATE VIEW most_errors AS
SELECT *
FROM err_percent
WHERE err_percent.perc > 1
ORDER BY err_percent.perc DESC;