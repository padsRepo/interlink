CREATE DATABASE IF NOT EXISTS repository;
USE repository;

CREATE TABLE IF NOT EXISTS gitRepo(
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  snid int(7) NOT NULL AUTO_INCREMENT, 
  pkgName varchar(25) NOT NULL,
  version varchar(75) NOT NULL,
  link varchar(255) not null,
  creationDate datetime,
  docsName varchar(25) NOT NULL,
  docsLink varchar(75) NOT NULL,
  description varchar(150) NOT NULL,
  PRIMARY KEY(snid)
);

CREATE VIEW IF NOT EXISTS qgitRepo1 AS
  SELECT
    CAST(timestamp AS DATE) AS updated,
    snid AS entry,
    CONCAT(pkgname, "_v", version) AS prettyName,
    link AS Link,
    CAST(creationDate AS DATE) AS created,
    docsName AS docsName,
    docsLink AS docsLink,
    description AS description
  FROM gitRepo
;

CREATE TABLE IF NOT EXISTS repository(
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  snid int(7) NOT NULL AUTO_INCREMENT, 
  pkgName varchar(25) NOT NULL,
  version varchar(75) NOT NULL,
  extension ENUM(".tar.gz", ".tar", ".zip"),
  creationDate datetime,
  docsName varchar(25) NOT NULL,
  docsLink varchar(75) NOT NULL,
  description varchar(150) NOT NULL,
  PRIMARY KEY(snid)
);

CREATE VIEW IF NOT EXISTS qrepo1 AS
  SELECT
    CAST(timestamp AS DATE) AS updated,
    snid AS entry,
    CONCAT(pkgname, "_v", version, extension) AS link,
    CAST(creationDate AS DATE) AS created,
    docsName AS docsName,
    docsLink AS docsLink,
    description AS description
  FROM repository
;

