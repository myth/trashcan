CREATE TABLE Supplier (
	sno INT NOT NULL PRIMARY KEY,
	sname CHAR(5),
	status INT,
	city CHAR(6));

CREATE TABLE Part (
	pno INT NOT NULL PRIMARY KEY,
	pname CHAR(5),
	color CHAR(5),
	weight DECIMAL(3,1),
	city CHAR(6));

CREATE TABLE SuppliesPart (
	sno INT NOT NULL,
	pno INT NOT NULL,
	qty INT,
	PRIMARY KEY (sno, pno),
	FOREIGN KEY (sno) REFERENCES Supplier(sno),
	FOREIGN KEY (pno) REFERENCES Part(pno));
 
INSERT INTO Supplier VALUES
   (101,'XYZ',10,'Boston'),
   (102,'Harry',15,'Dallas'),
   (103,'ABC',20,'Denver');
 
INSERT INTO Part VALUES
   (201,'Bolt','Grey',1.0,'Boston'),
   (202,'Screw','Grey',1.1,'Boston'),
   (203,'Nail','Grey',2.0,'Boston'),
   (204,'Bolt','Grey',1.0,'Dallas'),
   (205,'Screw','Grey',1.1,'Dallas'),
   (206,'Nail','Grey',2.0,'Miami'),
   (207,'Bolt','Grey',1.0,'Denver'),
   (208,'Screw','Grey',1.1,'Denver'),
   (209,'Nail','Grey',2.0,'Denver');
 
INSERT INTO SuppliesPart VALUES
   (101,201,10),
   (101,202,11),
   (101,203,12),
   (102,204,10),
   (102,206,21),
   (103,207,1),
   (103,209,2);
