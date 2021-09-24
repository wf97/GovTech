create database section2;



CREATE TABLE customer (
    id int PRIMARY KEY,
    name varchar(30) NOT NULL,
    phone INTEGER NOT NULL,
    address varchar(255)  NOT NULL

);

select * from customer;

CREATE TABLE salesperson (
    id int PRIMARY KEY,
    name varchar(255) NOT NULL
);

CREATE TABLE car (
    serialNumber varchar(20) PRIMARY KEY,
    modelName varchar(30) NOT NULL,
    manufacturer varchar(30) NOT NULL,
    price FLOAT NOT NULL,
    weight FLOAT NOT NULL
);

CREATE TABLE transactions (
    txn_id int PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL,
	customerID int FOREIGN KEY REFERENCES customer(id),
	salespersonID int FOREIGN KEY REFERENCES salesperson(id),
	serialNumber varchar(20) FOREIGN KEY REFERENCES car(serialNumber),
);



/* Query 1 */
Select cu.name, SUM(ca.price) as spending
FROM 
transactions t
left join 
car ca
ON
t.serialNumber = ca.serialNumber
left join
customer cu
on
t.customerID = cu.id
GROUP BY cu.name;

/* Query 2 */
select ca.manufacturer, COUNT(ca.serialNumber) as sales_quantity from
transactions t 
left join
car ca
on t.serialNumber = ca.serialNumber
WHERE MONTH(t.date) = MONTH(CURDATE())
AND
ca.manufacturer in 
(select ca.manufacturer sales from
	transactions t
	left join
	car ca
	on t.serialNumber = ca.serialNumber
	group by ca.manufacturer
	order by COUNT(ca.serialNumber) desc
	LIMIT 3)
GROUP BY ca.manufacturer;
