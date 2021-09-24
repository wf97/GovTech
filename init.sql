create database section2;

use section2;

CREATE TABLE customer (
    id INT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    phone INTEGER NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE salesperson (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE car (
    serialNumber VARCHAR(20) PRIMARY KEY,
    modelName VARCHAR(30) NOT NULL,
    manufacturer VARCHAR(30) NOT NULL,
    price FLOAT NOT NULL,
    weight FLOAT NOT NULL
);

CREATE TABLE transactions (
    txn_id INT PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL,
    customerID INT,
    salespersonID INT,
    serialNumber VARCHAR(20)
);

ALTER TABLE transactions ADD FOREIGN KEY (customerID) REFERENCES customer(id);
ALTER TABLE transactions ADD FOREIGN KEY (salespersonID) REFERENCES salesperson(id);
ALTER TABLE transactions ADD FOREIGN KEY (serialNumber) REFERENCES car(serialNumber);

/* Query 1 */
SELECT
    cu.name, SUM(ca.price) AS spending
FROM
    transactions t
        LEFT JOIN
    car ca ON t.serialNumber = ca.serialNumber
        LEFT JOIN
    customer cu ON t.customerID = cu.id
GROUP BY cu.name;

/* Query 2 */
SELECT
    ca.manufacturer, COUNT(ca.serialNumber) AS sales_quantity
FROM
    transactions t
        LEFT JOIN
    car ca ON t.serialNumber = ca.serialNumber
WHERE
    MONTH(t.date) = MONTH(CURDATE())
        AND ca.manufacturer IN
        (SELECT temp.manufacturer FROM
			(SELECT
				ca.manufacturer,
				ROW_NUMBER() OVER (ORDER BY COUNT(ca.serialNumber) DESC) as row_num
			FROM
				transactions t
					LEFT JOIN
				car ca ON t.serialNumber = ca.serialNumber
			GROUP BY ca.manufacturer
			) temp
            WHERE temp.row_num <= 3)
GROUP BY ca.manufacturer;