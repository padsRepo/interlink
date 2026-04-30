CREATE DATABASE IF NOT EXISTS blog;
USE blog;

CREATE TABLE IF NOT EXISTS blog(
  snid int not null auto_increment primary key,
  created date,
  updated timestamp not null default current_timestamp,
  author varchar(50) not null,
  title varchar(50),
  content text not null
);

INSERT INTO blog(created, author, title, content) VALUES('2024-02-18', 'Joe Corso', 'My Auto Generated Post', 'You should be able to see an auto generated admin page, and form to fill in your next post, and report to see each post, and blog, which can be styled like a blog. >:{D-K http://127.0.0.1:8000/admin/blog http://127.0.0.1:8000/form/blog http://127.0.0.1:8000/report/blog http://127.0.0.1:8000/blog/blog')
