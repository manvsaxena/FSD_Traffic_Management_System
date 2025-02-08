ALTER TABLE violation
ADD CONSTRAINT fk1 FOREIGN KEY (zone_id) REFERENCES zone(zone_id)on delete set NULL on update set NULL;

ALTER TABLE violation
ADD CONSTRAINT fk2 FOREIGN KEY (vehicle_no) REFERENCES rto_vehicle(vehicle_no)on delete cascade on update cascade;

ALTER TABLE rto_vehicle
ADD CONSTRAINT fk5 FOREIGN KEY (owner_id) REFERENCES citizen(aadhaar_id);

ALTER TABLE rto_vehicle
ADD CONSTRAINT fk6 FOREIGN KEY (zone_id) REFERENCES zone(zone_id);
