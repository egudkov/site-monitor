drop table if exists websites;
create table websites (
  id integer primary key autoincrement,
  url text not null,
  status text default 'Pending...'
);
