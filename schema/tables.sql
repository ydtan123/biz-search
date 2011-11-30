DROP TABLE IF EXISTS email, business;
CREATE TABLE business (
       name     VARCHAR(40) NOT NULL,
       url      VARCHAR(40) NOT NULL,
       phone    VARCHAR(10),
       category ENUM('AGY', 'RLS', 'EDU', 'TCH', 'TUR') NOT NULL,
       country  VARCHAR(10) NOT NULL,
       status   ENUM('U', 'P', 'A', 'C') NOT NULL,
       owner    VARCHAR(20),
       id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
       PRIMARY KEY (id)
) ENGINE = InnoDB;

CREATE TABLE email (
       address        VARCHAR(40) NOT NULL,
       biz_id         INT UNSIGNED NOT NULL,
       last_contacted DATE,
       priority       INT UNSIGNED NOT NULL,
       id             INT UNSIGNED NOT NULL AUTO_INCREMENT,
       PRIMARY KEY(id),
       FOREIGN KEY (biz_id) REFERENCES business (id)
) ENGINE = InnoDB;

#LOAD DATA LOCAL INFILE '~/projects/biz-search/data/biz.data' INTO TABLE business;
#LOAD DATA LOCAL INFILE '~/projects/biz-search/data/email.data' INTO TABLE email;

