create table if not exists fishes (
    name varchar(50) not null primary key, #current highest fish name length is 126
    imageURI varchar(150), #current highest fish imageURI length is 126
    location varchar(30), #current highest fish location lengthi is 22
    shadowSize tinyint, #max shadow size is 6
    startTime time,
    endTime time,
    january boolean,
    february boolean,
    march boolean,
    april boolean,
    may boolean,
    june boolean,
    july boolean,
    august boolean,
    september boolean,
    october boolean,
    november boolean,
    december boolean
)

