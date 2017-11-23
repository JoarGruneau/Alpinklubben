create table if not exists users (
id integer primary key autoincrement,
first_name text not null,
last_name text not null,
username text not null,
email text not null,
hashed_password text not null
);
create table if not exists cart (
id integer primary key autoincrement,
username text not null,
description text not null,
price integer not null
);
