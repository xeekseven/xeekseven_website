DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS article_content;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS article_markdown;

CREATE TABLE article (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id varchar(40) NOT NULL,
  article_id varchar(40) NOT NULL,
  article_modefiedtime DATETIME,
  article_tag varchar(100) NOT NULL,
  article_imgpath TEXT NOT NULL,
  article_title TEXT NOT NULL,
  article_subtitle TEXT NOT NULL,
  article_introduction TEXT NOT NULL,
  article_view_count INTEGER NOT NULL,
  article_scan_count INTEGER NOT NULL
);
CREATE TABLE article_content(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content_id varchar(40) NOT NULL,
  article_id varchar(40) NOT NULL,
  article_typename nvarchar(40) NOT NULL,
  article_value TEXT NOT NULL,
  article_index INTEGER NOT NULL
);
CREATE TABLE author(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id varchar(40) NOT NULL,
  author_name varchar(40) NOT NULL,
  headimg TEXT NOT NULL
);

CREATE TABLE article_markdown(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  markdown_id varchar(40) NOT NULL,
  author_id varchar(40) NOT NULL,
  title varchar(100) NOT NULL,
  content TEXT NOT NULL,
  create_time DATETIME,
  modefied_time DATETIME,
  tag varchar(40)
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);