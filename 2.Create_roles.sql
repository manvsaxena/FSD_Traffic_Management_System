DROP USER IF EXISTS 'project'@'localhost';
CREATE USER 'project'@'localhost' identified by'project123';

GRANT SELECT,INSERT ON trafficfine.login TO 'project'@'localhost';
GRANT INSERT, SELECT, DELETE ON trafficfine.violation TO 'project'@'localhost';
GRANT INSERT,SELECT ON trafficfine.payment TO 'project'@'localhost';
GRANT SELECT ON trafficfine.citizen TO 'project'@'localhost';
GRANT SELECT ON trafficfine.rto_vehicle TO 'project'@'localhost';

DROP USER IF EXISTS 'admin'@'localhost';
CREATE USER 'admin'@'localhost' identified by 'likith';

GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;