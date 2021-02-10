USE heroku_4c9d2a4e8dd9512;

CREATE TABLE user(
    id integer primary key auto_increment,
    username varchar(30) not null,
    password varchar(150) not null,
    name varchar(50) not null,
    workload time,
    admin tinyint(1),
    active tinyint(1),
    created_at datetime,
    updated_at datetime,
    week_days_off varchar(50)
);

CREATE TABLE register(
    id Integer primary key auto_increment,
    user_id integer not null,
    entry time,
    finish time,
    date date,
    workload time,
    created_at datetime,
    updated_at datetime

);

CREATE TABLE pauses(
    id integer primary key auto_increment,
    register_id integer,
    pause_id integer,
    entry time,
    finish time,
    time time,
    created_at datetime,
    updated_at datetime
);

CREATE TABLE pause_infos(
    id integer primary key auto_increment,
    init_label varchar(50) not null,
    end_label varchar(50) not null,
    time integer not null
);

CREATE TABLE days_off(
    id integer primary key auto_increment,
    user_id integer(50) not null,
    date date not null
);


ALTER TABLE user ADD CONSTRAINT unique_username UNIQUE (username);
