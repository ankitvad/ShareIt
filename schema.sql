drop table if exists pics;
create table pics ( 
  id integer primary key autoincrement,
  filename text not null,
  likes integer default 0,
  dislike integer default 1);
