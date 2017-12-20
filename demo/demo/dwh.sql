/*
 * dwh.sql
 * Copyright (C) 2017 weihao <weihao@weihao-PC>
 *
 * Distributed under terms of the MIT license.
 */


CREATE DATABASE Zhihu;
USE Zhihu
CREATE TABLE Person (
    id varchar(30),
    name varchar(30),
    place varchar(100),
    bussiness varchar(30),
    job_exp varchar(1000),
    edu_exp varchar(1000),
    introduce varchar(1000),
    answer_num integer,
    question_num integer,
    article_num integer,
    column_num integer,
    following_num integer,
    follower_num integer,
    PRIMARY KEY(id)
);

CREATE TABLE Following (
    person_id VARCHAR(30),
    following_id VARCHAR(30)
);

CREATE TABLE Followers (
    person_id VARCHAR(30),
    followers_id VARCHAR(30)
);

create table Answers (
    author_id VARCHAR(30),
    question_text VARCHAR(1000),
    question_link VARCHAR(1000),
    answer_content TEXT,
    answer_time VARCHAR(30),
    upvote_num VARCHAR(30),
    comment_num VARCHAR(30)
);

CREATE TABLE Articles (
    article_id VARCHAR(30),
    person_id VARCHAR(30),
    article_title VARCHAR(1000),
    article_link VARCHAR(1000),
    article_content TEXT,
    upvote_num VARCHAR(30),
    comment_num VARCHAR(30),
    PRIMARY KEY(article_id)
);

CREATE TABLE Article_comment (
    article_id VARCHAR(30),
    comment_person_name VARCHAR(30),
    comment_content VARCHAR(1000),
    comment_time VARCHAR(30),
    upvote_num VARCHAR(30)
);
-- vim:et
