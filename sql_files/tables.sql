
CREATE table admin(
    username VARCHAR(50) NOT NULL PRIMARY KEY,
    pass VARCHAR(50) NOT NULL
);


CREATE TABLE student
(
    roll VARCHAR(9) NOT NULL,
    fest_id NUMERIC(5) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    dept VARCHAR(50) NOT NULL,
    pass VARCHAR(50) NOT NULL
);

CREATE TABLE event
(
    event_id NUMERIC(5) NOT NULL PRIMARY KEY,
    event_name VARCHAR(50) NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    event_venue VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_description VARCHAR(200),
    event_winner NUMERIC(5)
);

CREATE TABLE accomodation
(
    acc_id NUMERIC(5) NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE ext_participant
(
    fest_id NUMERIC(5) NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    college VARCHAR(50) NOT NULL,
    acc_id NUMERIC(5) NOT NULL ,
    FOREIGN KEY (acc_id) REFERENCES accomodation(acc_id) ON DELETE CASCADE ON UPDATE CASCADE,
    pass VARCHAR(50) NOT NULL
);

-- relationships 
CREATE TABLE organising
(
    fest_id NUMERIC(5) NOT NULL,
    event_id NUMERIC(5) NOT NULL ,
    FOREIGN KEY (fest_id) REFERENCES student(fest_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY(fest_id,event_id)
);

CREATE TABLE volunteering
(
    fest_id NUMERIC(5) NOT NULL,
    event_id NUMERIC(5) NOT NULL ,
    FOREIGN KEY (fest_id) REFERENCES student(fest_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY(fest_id,event_id)
);

CREATE TABLE participating_ext
(
    fest_id NUMERIC(5) NOT NULL,
    event_id NUMERIC(5) NOT NULL ,
    FOREIGN KEY (fest_id) REFERENCES ext_participant(fest_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY(fest_id,event_id)
);

CREATE TABLE participating_int
(
    fest_id NUMERIC(5) NOT NULL,
    event_id NUMERIC(5) NOT NULL ,
    FOREIGN KEY (fest_id) REFERENCES student(fest_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY(fest_id,event_id)
);