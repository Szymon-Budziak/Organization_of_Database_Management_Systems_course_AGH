# SQL - Funkcje okna (Window functions)

# Lab 1-2

---

**Imię i nazwisko:**

- **Szymon Budziak**
- **Piotr Ludynia**

---

Celem ćwiczenia jest zapoznanie się z działaniem funkcji okna (window functions) w SQL, analiza wydajności zapytań i
porównanie z rozwiązaniami przy wykorzystaniu "tradycyjnych" konstrukcji SQL

Swoje odpowiedzi wpisuj w miejsca oznaczone jako:

```sql
-- wyniki ...
```

Ważne/wymagane są komentarze.

Zamieść kod rozwiązania oraz zrzuty ekranu pokazujące wyniki, (dołącz kod rozwiązania w formie tekstowej/źródłowej)

Zwróć uwagę na formatowanie kodu

---

## Oprogramowanie - co jest potrzebne?

Do wykonania ćwiczenia potrzebne jest następujące oprogramowanie:

- MS SQL Server - wersja 2019, 2022
- PostgreSQL - wersja 15/16
- SQLite
- Narzędzia do komunikacji z bazą danych
  - SSMS - Microsoft SQL Managment Studio
  - DtataGrip lub DBeaver
- Przykładowa baza Northwind
  - W wersji dla każdego z wymienionych serwerów

Oprogramowanie dostępne jest na przygotowanej maszynie wirtualnej

## Dokumentacja/Literatura

- Kathi Kellenberger, Clayton Groom, Ed Pollack, Expert T-SQL Window Functions in SQL Server 2019, Apres 2019
- Itzik Ben-Gan, T-SQL Window Functions: For Data Analysis and Beyond, Microsoft 2020

- Kilka linków do materiałów które mogą być
  pomocne - https://learn.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql?view=sql-server-ver16

  - https://www.sqlservertutorial.net/sql-server-window-functions/
  - https://www.sqlshack.com/use-window-functions-sql-server/
  - https://www.postgresql.org/docs/current/tutorial-window.html
  - https://www.postgresqltutorial.com/postgresql-window-function/
  - https://www.sqlite.org/windowfunctions.html
  - https://www.sqlitetutorial.net/sqlite-window-functions/

- Ikonki używane w graficznej prezentacji planu zapytania w SSMS opisane są tutaj:
  - [https://docs.microsoft.com/en-us/sql/relational-databases/showplan-logical-and-physical-operators-reference](https://docs.microsoft.com/en-us/sql/relational-databases/showplan-logical-and-physical-operators-reference)

---

# Zadanie 1 - obserwacja

Wykonaj i porównaj wyniki następujących poleceń.

```sql
select avg(unitprice) avgprice
from products p;

select avg(unitprice) over () as avgprice
from products p;

select categoryid, avg(unitprice) avgprice
from products p
group by categoryid

select avg(unitprice) over (partition by categoryid) as avgprice
from products p;
```

Jaka są podobieństwa, jakie różnice pomiędzy grupowaniem danych a działaniem funkcji okna?

| Zapytanie | MS SQL                    | Postgres                   | SQLite                   |
| --------- | ------------------------- | -------------------------- | ------------------------ |
| 1         | ![](./img/ex1/mysql1.png) | ![](img/ex1/postgres1.png) | ![](img/ex1/sqlite1.png) |
| 2         | ![](./img/ex1/mysql2.png) | ![](img/ex1/postgres2.png) | ![](img/ex1/sqlite2.png) |
| 3         | ![](./img/ex1/mysql3.png) | ![](img/ex1/postgres3.png) | ![](img/ex1/sqlite3.png) |
| 4         | ![](./img/ex1/mysql4.png) | ![](img/ex1/postgres4.png) | ![](img/ex1/sqlite4.png) |

> Widzimy, że funkcje okna przypisują obliczoną wartość każdemu wierszowi danych.
> Grupowanie automatycznie agreguje wartości do grup.

> **Zapytanie 1** zwraca średnią cenę wszystkich produktów.

> **Zapytanie 2**, które używa funkcji okna, zwraca tę samą wartość liczbową co
> **Zapytanie 1**, ale dodaje te wartość dla każdego produktu.

> **Zapytanie 3** używające group by, oblicza średnią wartość dla każdej z grup,
> rozróżnianych przed categoryid.

> **Zapytanie 4** używające funkcji okna, różni się od **Zapytania 2** tym, że liczy średnią cenę na grupach produktów, które łączy top samo categoryid. Wartości są zwracane dla
> każðego produktu podobnie jak w **Zapytaniu 2**.

# Zadanie 2 - obserwacja

Wykonaj i porównaj wyniki następujących poleceń.

```sql
--1)

select p.productid,
       p.ProductName,
       p.unitprice,
       (select avg(unitprice) from products) as avgprice
from products p
where productid < 10

--2)
select p.productid,
       p.ProductName,
       p.unitprice,
       avg(unitprice) over () as avgprice
from products p
where productid < 10
```

Jaka jest różnica? Czego dotyczy warunek w każdym z przypadków? Napisz polecenie równoważne

1. z wykorzystaniem podzapytania
2. z wykorzystaniem funkcji okna. Napisz polecenie równoważne

---

> 1. Pierwsze zapytanie używa `podzapytania w klauzuli SELECT` do obliczenia średniej ceny wszystkich produktów. Warunek
>    productid < 10 jest używany do filtracji wyników na podstawie identyfikatora produktu mniejszego niż 10.
> 2. Drugie zapytanie wykorzystuje `funkcję okna avg(unitprice) over ()` do obliczenia średniej ceny wszystkich produktów,
>    ale bez potrzeby podzapytania. Warunek productid < 10 również jest używany do filtracji wyników na podstawie
>    identyfikatora produktu mniejszego niż 10.

| Zapytanie    | MS SQL Server              | Postgres                    | SQLite                    |
| ------------ | -------------------------- | --------------------------- | ------------------------- |
| 1 oryginalne | ![](./img/ex2/mysql11.png) | ![](img/ex2/postgres11.png) | ![](img/ex2/sqlite11.png) |
| 1 równoważne | ![](./img/ex2/mysql12.png) | ![](img/ex2/postgres12.png) | ![](img/ex2/sqlite12.png) |
| 2 oryginalne | ![](./img/ex2/mysql21.png) | ![](img/ex2/postgres21.png) | ![](img/ex2/sqlite21.png) |
| 2 równoważne | ![](./img/ex2/mysql22.png) | ![](img/ex2/postgres22.png) | ![](img/ex2/sqlite22.png) |

# Zadanie 3

Baza: Northwind, tabela: products

Napisz polecenie, które zwraca: id produktu, nazwę produktu, cenę produktu, średnią cenę wszystkich produktów.

Napisz polecenie z wykorzystaniem podzapytania, join'a oraz funkcji okna.

- Polecenie z wykorzystaniem podzapytania

```sql
SELECT p.ProductID,
       p.ProductName,
       p.UnitPrice,
       (SELECT AVG(p2.UnitPrice) FROM Products AS p2) AS AveragePrice
FROM Products AS p
```

- Polecenie z wykorzystaniem joina

```sql
SELECT p.ProductID,
       p.ProductName,
       p.UnitPrice,
       AVG(p2.UnitPrice) AS AveragePrice
FROM Products p
         CROSS JOIN Products p2
GROUP BY p.ProductID, p.ProductName, p.UnitPrice
```

- Polecenie z wykorzystaniem funkcji okna

```sql
SELECT p.ProductID,
       p.ProductName,
       p.UnitPrice,
       AVG(UnitPrice) OVER() AS AveragePrice
FROM Products AS p
```

---

Porównaj czasy oraz plany wykonania zapytań. Przetestuj działanie w różnych SZBD (MS SQL Server, PostgreSql, SQLite)

W SSMS włącz dwie opcje: Include Actual Execution Plan oraz Include Live Query Statistics

![w:700](./img/ex3/window-1.png)

W DataGrip użyj opcji Explain Plan/Explain Analyze

![w:700](./img/ex3/window-2.png)

![w:700](./img/ex3/window-3.png)

**Porównanie planów wykonania**

| Zapytanie    | MS SQL                    | Postgres                   | SQLite                   |
| ------------ | ------------------------- | -------------------------- | ------------------------ |
| Podzapytanie | ![](./img/ex3/mysql1.png) | ![](img/ex3/postgres1.png) | ![](img/ex3/sqlite1.png) |
| Join         | ![](./img/ex3/mysql2.png) | ![](img/ex3/postgres2.png) | ![](img/ex3/sqlite2.png) |
| Funkcja okna | ![](./img/ex3/mysql3.png) | ![](img/ex3/postgres3.png) | ![](img/ex3/sqlite3.png) |

**Porównanie czasów wykonania**

| Zapytanie    | MS SQL                        | Postgres                       | SQLite                       |
| ------------ | ----------------------------- | ------------------------------ | ---------------------------- |
| Podzapytanie | ![](./img/ex3/mysql1time.png) | ![](img/ex3/postgres1time.png) | ![](img/ex3/sqlite1time.png) |
| Join         | ![](./img/ex3/mysql2time.png) | ![](img/ex3/postgres2time.png) | ![](img/ex3/sqlite2time.png) |
| Funkcja okna | ![](./img/ex3/mysql3time.png) | ![](img/ex3/postgres3time.png) | ![](img/ex3/sqlite3time.png) |

> Sqlite nie daje pełnej możliwości zwizualizowania planu. Datagrip pozwala jednak na zrobienie tego z Postgresem.
> Ze względu na specyficzny sposób wyliczania kosztu dla każdego z SZBD nie ma sensu porównywać wyników ze względu na rodzaj SZBD. Natomiast porównując koszty ze względu na formę zapytania można zauważyć, że w przypadku zapytań dla MS SQL czasy wykonania są najszybsze, a dla PostgreSQL oraz SQLite są nieco gorsze, jednak nie sa one takie duże, aby wykonywały się w zauważalnie dłuższym czasie.

---

# Zadanie 4

Baza: Northwind, tabela products

Napisz polecenie, które zwraca: id produktu, nazwę produktu, cenę produktu, średnią cenę produktów w kategorii, do której należy dany produkt. Wyświetl tylko pozycje (produkty), których cena jest większa niż średnia cena.

Napisz polecenie z wykorzystaniem podzapytania, join'a oraz funkcji okna.

- Polecenie z wykorzystaniem podzapytania

```sql
SELECT p.ProductID,
       p.ProductName,
       p.UnitPrice,
       (SELECT AVG(p2.UnitPrice)
        FROM Products AS p2
        WHERE p2.CategoryID = p.CategoryID) AS AvgCategoryPrice
FROM Products p
WHERE p.UnitPrice > (SELECT AVG(p3.UnitPrice)
                     FROM Products p3
                     WHERE p3.CategoryID = p.CategoryID)
```

- Polecenie z wykorzystaniem joina

```sql
SELECT p.ProductID,
       p.ProductName,
       p.UnitPrice,
       AVG(p2.UnitPrice) AS AvgCategoryPrice
FROM Products p
         JOIN Products AS p2 ON p.CategoryID = p2.CategoryID
GROUP BY
    p.ProductID,
    p.ProductName,
    p.UnitPrice
HAVING p.UnitPrice > AvgCategoryPrice
```

- Polecenie z wykorzystaniem funkcji okna

```sql
WITH AvgPrices AS (SELECT ProductID,
                          ProductName,
                          UnitPrice,
                          AVG(UnitPrice) OVER (PARTITION BY CategoryID) AS AvgCategoryPrice
                   FROM Products)
SELECT ProductID,
       ProductName,
       UnitPrice,
       AvgCategoryPrice
FROM AvgPrices
WHERE UnitPrice > AvgCategoryPrice;
```

Porównaj zapytania. Porównaj czasy oraz plany wykonania zapytań. Przetestuj działanie w różnych SZBD (MS SQL Server, PostgreSql, SQLite)

**Wyniki**

| Zapytanie    | MS SQL                    | Postgres                   | SQLite                   |
| ------------ | ------------------------- | -------------------------- | ------------------------ |
| Podzapytanie | ![](./img/ex4/mysql1.png) | ![](img/ex4/postgres1.png) | ![](img/ex4/sqlite1.png) |
| Join         | ![](./img/ex4/mysql2.png) | ![](img/ex4/postgres2.png) | ![](img/ex4/sqlite2.png) |
| Funkcja okna | ![](./img/ex4/mysql3.png) | ![](img/ex4/postgres3.png) | ![](img/ex4/sqlite3.png) |

**Porównanie czasów wykonania**

| Zapytanie    | MS SQL                        | Postgres                       | SQLite                       |
| ------------ | ----------------------------- | ------------------------------ | ---------------------------- |
| Podzapytanie | ![](./img/ex4/mysql1time.png) | ![](img/ex4/postgres1time.png) | ![](img/ex4/sqlite1time.png) |
| Join         | ![](./img/ex4/mysql2time.png) | ![](img/ex4/postgres2time.png) | ![](img/ex4/sqlite2time.png) |
| Funkcja okna | ![](./img/ex4/mysql3time.png) | ![](img/ex4/postgres3time.png) | ![](img/ex4/sqlite3time.png) |

**Porównanie planów wykonania**

| Zapytanie    | MS SQL                        | Postgres                       | SQLite                       |
| ------------ | ----------------------------- | ------------------------------ | ---------------------------- |
| Podzapytanie | ![](./img/ex4/mysql1plan.png) | ![](img/ex4/postgres1plan.png) | ![](img/ex4/sqlite1plan.png) |
| Join         | ![](./img/ex4/mysql2plan.png) | ![](img/ex4/postgres2plan.png) | ![](img/ex4/sqlite2plan.png) |
| Funkcja okna | ![](./img/ex4/mysql3plan.png) | ![](img/ex4/postgres3plan.png) | ![](img/ex4/sqlite3plan.png) |

> Możemy zaobserwować, że operacje w przypadku PostgreSQL są liniowe oraz jest ich mniej co przekłada się na mniejszy czas wykonywania zapytań. Dla przykładu w przypadku MS SQL roaz SQLite widzimy zagnieżdżone podzapytania.

---

# Zadanie 5 - przygotowanie

Baza: Northwind

Tabela products zawiera tylko 77 wiersz. Warto zaobserwować działanie na większym zbiorze danych.

Wygeneruj tabelę zawierającą kilka milionów (kilkaset tys.) wierszy

Stwórz tabelę o następującej strukturze:

Skrypt dla SQL Srerver

```sql
create table product_history
(
    id              int identity(1,1) not null,
    productid       int,
    productname     varchar(40) not null,
    supplierid      int null,
    categoryid      int null,
    quantityperunit varchar(20) null,
    unitprice       decimal(10, 2) null,
    quantity        int,
    value           decimal(10, 2),
    date            date,
    constraint pk_product_history primary key clustered
    (id asc )
)
```

Wygeneruj przykładowe dane:

Dla 30000 iteracji, tabela będzie zawierała nieco ponad 2mln wierszy (dostostu ograniczenie do możliwości swojego
komputera)

Skrypt dla SQL Srerver

```sql
declare
@i int
set @i = 1
while @i <= 30000
begin
    insert
product_history
select productid,
       ProductName,
       SupplierID,
       CategoryID,
       QuantityPerUnit,
       round(RAND() * unitprice + 10, 2),
       cast(RAND() * productid + 10 as int),
       0,
       dateadd(day, @i, '1940-01-01')
from products set @i = @i + 1;
end;

update product_history
set value = unitprice * quantity
where 1 = 1;
```

Skrypt dla Postgresql

```sql
create table product_history
(
    id              int generated always as identity not null
        constraint pkproduct_history primary key,
    productid       int,
    productname     varchar(40)                      not null,
    supplierid      int null,
    categoryid      int null,
    quantityperunit varchar(20) null,
    unitprice       decimal(10, 2) null,
    quantity        int,
    value           decimal(10, 2),
    date            date
);
```

Wygeneruj przykładowe dane:

Skrypt dla Postgresql

```sql
do
$$
begin
for cnt in 1..30000 loop
    insert into product_history(productid, productname, supplierid,
           categoryid, quantityperunit,
           unitprice, quantity, value, date)
select productid,
       productname,
       supplierid,
       categoryid,
       quantityperunit,
       round((random() * unitprice + 10):: numeric, 2),
       cast(random() * productid + 10 as int),
       0,
       cast('1940-01-01' as date) + cnt
from products;
end loop;
end; $$;

update product_history
set value = unitprice * quantity
where 1 = 1;
```

Wykonaj polecenia: `select count(*) from product_history`, potwierdzające wykonanie zadania

| MS SQL                    | Postgres                   | SQLite                   |
| ------------------------- | -------------------------- | ------------------------ |
| ![](./img/ex5/mysql1.png) | ![](img/ex5/postgres1.png) | ![](img/ex5/sqlite1.png) |

---

# Zadanie 6

Baza: Northwind, tabela product_history

To samo co w zadaniu 3, ale dla większego zbioru danych

Napisz polecenie, które zwraca:

- id pozycji,
- id produktu,
- nazwę produktu,
- cenę produktu,
- średnią cenę produktów w kategorii do której należy dany produkt.

Wyświetl tylko pozycje (produkty) których cena jest większa niż średnia cena.

(przykłady poniżej)

Napisz polecenie z wykorzystaniem podzapytania, join'a oraz funkcji okna.

- Polecenie z wykorzystaniem podzapytania

```sql
SELECT p.ProductID,
	   p.ProductName,
       p.UnitPrice,
	   (SELECT AVG(ph.UnitPrice)
	    FROM product_history ph
	    WHERE ph.CategoryID = p.CategoryID) as avgprice
FROM product_history as p
WHERE p.UnitPrice >
      (SELECT AVG(ph.UnitPrice)
       FROM product_history ph
       WHERE ph.CategoryID = p.CategoryID)
```

- Polecenie z wykorzystaniem joina

```sql
WITH classes as
(select categoryid, avg(unitprice) avgprice
from product_history p
group by categoryid)

SELECT p.ProductID,
	   p.ProductName,
       p.UnitPrice,
	   classes.avgprice
FROM product_history as p
	   inner JOIN classes ON p.categoryid = classes.categoryid
WHERE p.unitprice > classes.avgprice
```

- Polecenie z wykorzystaniem funkcji okna

```sql
WITH data as
(SELECT p.ProductID,
       p.ProductName,
       p.UnitPrice,
       AVG(UnitPrice) OVER(PARTITION BY p.CategoryID) AS AveragePrice
FROM product_history AS p)
SELECT * from data
WHERE UnitPrice > AveragePrice
```

Porównaj zapytania. Porównaj czasy oraz plany wykonania zapytań. Przetestuj działanie w różnych SZBD (MS SQL Server, PostgreSql, SQLite)

**Wyniki**

| Zapytanie    | MS SQL                    | Postgres                   | SQLite                   |
| ------------ | ------------------------- | -------------------------- | ------------------------ |
| Podzapytanie | ![](./img/ex6/mysql1.png) | ![](img/ex6/postgres1.png) | ![](img/ex6/sqlite1.png) |
| Join         | ![](./img/ex6/mysql2.png) | ![](img/ex6/postgres2.png) | ![](img/ex6/sqlite2.png) |
| Funkcja okna | ![](./img/ex6/mysql3.png) | ![](img/ex6/postgres3.png) | ![](img/ex6/sqlite3.png) |

**Porównanie czasów wykonania**

| Zapytanie    | MS SQL                        | Postgres                       | SQLite                       |
| ------------ | ----------------------------- | ------------------------------ | ---------------------------- |
| Podzapytanie | ![](./img/ex6/mysql1time.png) | ![](img/ex6/postgres1time.png) | ![](img/ex6/sqlite1time.png) |
| Join         | ![](./img/ex6/mysql2time.png) | ![](img/ex6/postgres2time.png) | ![](img/ex6/sqlite2time.png) |
| Funkcja okna | ![](./img/ex6/mysql3time.png) | ![](img/ex6/postgres3time.png) | ![](img/ex6/sqlite3time.png) |

**Porównanie planów wykonania**

| Zapytanie    | MS SQL                        | Postgres                       | SQLite                       |
| ------------ | ----------------------------- | ------------------------------ | ---------------------------- |
| Podzapytanie | ![](./img/ex6/mysql1plan.png) | ![](img/ex6/postgres1plan.png) | ![](img/ex6/sqlite1plan.png) |
| Join         | ![](./img/ex6/mysql2plan.png) | ![](img/ex6/postgres2plan.png) | ![](img/ex6/sqlite2plan.png) |
| Funkcja okna | ![](./img/ex6/mysql3plan.png) | ![](img/ex6/postgres3plan.png) | ![](img/ex6/sqlite3plan.png) |

> Możemy zaobserwować, że zapytanie z użyciem podzapytania dla postgres nie wykonało się nawet po 5 minutach od wywołania. Dla SQLite również nie uzyskaliśmy wyniku po około 5 minutach. Jednym z pomysłow, było możliwe zawieszenie się bazy. Jednak, po testowym sprawdzeniu połączenia prostym zapytaniem, zakończyło się ono suckecem co świadczyło o poprawnym działaniu bazy, a problemem było mało efektywne działanie podzapytania w takim zapytaniu. Trochę lepiej poradziło sobie zapytanie z joinem a najlepiej z funkcją okna.

> Według analizy plany dla **joina** oraz **podzapytania** wyglądają podobnie z dwoma operacjami 'Full Index Scan' kazdy. Jednak, róznia się one miejscem agregacji gdzie jedna jest przed 'Hash Join' dla **podzapytania** a druga po w przypadku **joina**.

---

# Zadanie 7

Baza: Northwind, tabela product_history

Lekka modyfikacja poprzedniego zadania

Napisz polecenie, które zwraca:

- id pozycji
- id produktu
- nazwę produktu
- cenę produktu oraz:
  - średnią cenę produktów w kategorii do której należy dany produkt.
  - łączną wartość sprzedaży produktów danej kategorii (suma dla pola value)
  - średnią cenę danego produktu w roku którego dotyczy dana pozycja

Napisz polecenie z wykorzystaniem podzapytania, join'a oraz funkcji okna. Porównaj zapytania. W przypadku funkcji okna spróbuj użyć klauzuli WINDOW.

- Polecenie z wykorzystaniem podzapytania

_MS SQL_

```sql
SELECT ph.id,
       ph.ProductID,
       ph.ProductName,
       ph.UnitPrice,
	   (select avg(ph2.unitprice) from product_history as ph2 where ph.categoryid = ph2.categoryid) as AveragePrice,
	   (select sum(ph3.value) from product_history as ph3 where ph.categoryid = ph3.categoryid) as TotalSale,
	   (select avg(ph4.unitprice) from product_history as ph4 where ph.productid = ph4.productid and YEAR(ph.date) = YEAR(ph4.date)) as AveragePriceOverYear
FROM product_history AS ph
```

_Postgres_

```sql
SELECT ph.id,
       ph.ProductID,
       ph.ProductName,
       ph.UnitPrice,
	   (select avg(ph2.unitprice) from product_history as ph2 where ph.categoryid = ph2.categoryid) as AveragePrice,
	   (select sum(ph3.value) from product_history as ph3 where ph.categoryid = ph3.categoryid) as TotalSale,
	   (select avg(ph4.unitprice) from product_history as ph4 where ph.productid = ph4.productid and EXTRACT (YEAR FROM ph.date) = EXTRACT (YEAR FROM ph4.date)) as AveragePriceOverYear
FROM product_history AS ph
```

_SQLite_

```sql
SELECT ph.id,
       ph.ProductID,
       ph.ProductName,
       ph.UnitPrice,
	   (select avg(ph2.unitprice) from product_history as ph2 where ph.categoryid = ph2.categoryid) as AveragePrice,
	   (select sum(ph3.value) from product_history as ph3 where ph.categoryid = ph3.categoryid) as TotalSale,
	   (select avg(ph4.unitprice) from product_history as ph4 where ph.productid = ph4.productid and strftime('%Y', ph.date) = strftime('%Y', ph4.date)) as AveragePriceOverYear
FROM product_history AS ph
```

- Polecenie z wykorzystaniem joina

_MS SQL_

```sql
SELECT
    ph.id,
    ph.ProductID,
    ph.ProductName,
    ph.UnitPrice,
    AVG(ph2.unitprice) AS AveragePrice,
    SUM(ph3.value) AS TotalSale,
    AVG(ph4.unitprice) AS AveragePriceOverYear
FROM
    product_history AS ph
JOIN
    product_history AS ph2 ON ph.categoryid = ph2.categoryid
JOIN
    product_history AS ph3 ON ph.categoryid = ph3.categoryid
JOIN
    product_history AS ph4 ON ph.productid = ph4.productid AND YEAR(ph.date) = YEAR(ph4.date)
GROUP BY
    ph.id,
    ph.ProductID,
    ph.ProductName,
    ph.UnitPrice;
```

_Postgres_

```sql
SELECT
    ph.id,
    ph.ProductID,
    ph.ProductName,
    ph.UnitPrice,
    AVG(ph2.unitprice) AS AveragePrice,
    SUM(ph3.value) AS TotalSale,
    AVG(ph4.unitprice) AS AveragePriceOverYear
FROM
    product_history AS ph
JOIN
    product_history AS ph2 ON ph.categoryid = ph2.categoryid
JOIN
    product_history AS ph3 ON ph.categoryid = ph3.categoryid
JOIN
    product_history AS ph4 ON ph.productid = ph4.productid AND EXTRACT (YEAR FROM ph.date) = EXTRACT (YEAR FROM ph4.date)
GROUP BY
    ph.id,
    ph.ProductID,
    ph.ProductName,
    ph.UnitPrice;
```

_SQLite_

```sql
SELECT
    ph.id,
    ph.ProductID,
    ph.ProductName,
    ph.UnitPrice,
    AVG(ph2.unitprice) AS AveragePrice,
    SUM(ph3.value) AS TotalSale,
    AVG(ph4.unitprice) AS AveragePriceOverYear
FROM
    product_history AS ph
JOIN
    product_history AS ph2 ON ph.categoryid = ph2.categoryid
JOIN
    product_history AS ph3 ON ph.categoryid = ph3.categoryid
JOIN
    product_history AS ph4 ON ph.productid = ph4.productid AND strftime('%Y', ph.date) = strftime('%Y', ph4.date)
GROUP BY
    ph.id,
    ph.ProductID,
    ph.ProductName,
    ph.UnitPrice;
```

- Polecenie z wykorzystaniem funkcji okna

_MS SQL_

```sql
SELECT ph.id,
     ph.ProductID,
     ph.ProductName,
     ph.UnitPrice,
     avg(ph.UnitPrice) over (partition by ph.categoryid) as AveragePrice,
     sum(ph.value) over (partition by ph.categoryid) as TotalSale,
     avg(ph.UnitPrice) over (partition by ph.productid, YEAR(ph.date)) as AveragePriceOverYear
FROM product_history AS ph
WINDOW w AS (partition by ph.categoryid),
     w2 AS (partition by ph.productid, YEAR(ph.date))
```

_Postgres_

```sql
SELECT ph.id,
     ph.ProductID,
     ph.ProductName,
     ph.UnitPrice,
     avg(ph.UnitPrice) over (partition by ph.categoryid) as AveragePrice,
     sum(ph.value) over (partition by ph.categoryid) as TotalSale,
     avg(ph.UnitPrice) over (partition by ph.productid, EXTRACT (YEAR FROM ph.date)) as AveragePriceOverYear
FROM product_history AS ph
WINDOW w AS (partition by ph.categoryid),
     w2 AS (partition by ph.productid, EXTRACT (YEAR FROM ph.date))
```

_SQLite_

```sql
SELECT ph.id,
     ph.ProductID,
     ph.ProductName,
     ph.UnitPrice,
     avg(ph.UnitPrice) over (partition by ph.categoryid) as AveragePrice,
     sum(ph.value) over (partition by ph.categoryid) as TotalSale,
     avg(ph.UnitPrice) over (partition by ph.productid, strftime('%Y', ph.date)) as AveragePriceOverYear
FROM product_history AS ph
WINDOW w AS (partition by ph.categoryid),
     w2 AS (partition by ph.productid, strftime('%Y', ph.date))
```

> W powyższych zapytaniach możemy zaobserwować, jakie róznice należało uwzględnić aby móc wyciągnąc date:
>
> - MS SQL: należy użyć `YEAR(ph.date)`
> - Postgres: należy użyć `EXTRACT (YEAR FROM ph.date)`
> - SQLite: należy użyć `strftime('%Y', ph.date)`

**Wyniki**

| Zapytanie    | MS SQL                    | Postgres                   | SQLite                   |
| ------------ | ------------------------- | -------------------------- | ------------------------ |
| Podzapytanie | ![](./img/ex7/mysql1.png) | ![](img/ex7/postgres1.png) | ![](img/ex7/sqlite1.png) |
| Join         | ![](./img/ex7/mysql2.png) | ![](img/ex7/postgres2.png) | ![](img/ex7/sqlite2.png) |
| Funkcja okna | ![](./img/ex7/mysql3.png) | ![](img/ex7/postgres3.png) | ![](img/ex7/sqlite3.png) |

Porównaj czasy oraz plany wykonania zapytań. Przetestuj działanie w różnych SZBD (MS SQL Server, PostgreSql, SQLite).

**Porównanie czasów wykonania**

| Zapytanie    | MS SQL                        | Postgres                       | SQLite                       |
| ------------ | ----------------------------- | ------------------------------ | ---------------------------- |
| Podzapytanie | ![](./img/ex7/mysql1time.png) | ![](img/ex7/postgres1time.png) | ![](img/ex7/sqlite1time.png) |
| Join         | ![](./img/ex7/mysql2time.png) | ![](img/ex7/postgres2time.png) | ![](img/ex7/sqlite2time.png) |
| Funkcja okna | ![](./img/ex7/mysql3time.png) | ![](img/ex7/postgres3time.png) | ![](img/ex7/sqlite3time.png) |

**Porównanie planów wykonania**

| Zapytanie    | MS SQL                        | Postgres                         | SQLite                         |
| ------------ | ----------------------------- | -------------------------------- | ------------------------------ |
| Podzapytanie | ![](./img/ex7/mysql1plan.png) | ![](img/ex7/postgres1plan.png)   | ![](img/ex7/sqlite1plan.png)   |
| Join         | ![](./img/ex7/mysql2plan.png) | ![](./img/ex7/postgres2plan.png) | ![](./img/ex7/sqlite2plan.png) |
| Funkcja okna | ![](./img/ex7/mysql3plan.png) | ![](./img/ex7/postgres3plan.png) | ![](./img/ex7/sqlite3plan.png) |

> W przypadku MS SQL oraz PostgreSQL funkcje okna wykonują się bardziej liniowo niż ich odpowiedniki join oraz podzapytanie.

> Można też zauważyc, że czas wykonywania dla PostgreSQL był znacznie dłuższy niż w przypadku innych SZBD. Może być to spowodowane tym, że PostgreSQL wykonuje znacznie więcej full scanów. Możemy również zauważyć, że w przypadku podzapytania dla SQLite oraz MS SQL nie udało się otrzymać wyniku w czasie 5 min.

---

# Zadanie 8 - obserwacja

Funkcje rankingu, `row_number()`, `rank()`, `dense_rank()`

Wykonaj polecenie, zaobserwuj wynik. Porównaj funkcje row_number(), rank(), dense_rank()

```sql
select productid,
       productname,
       unitprice,
       categoryid,
       row_number() over(partition by categoryid order by unitprice desc)
       as rowno,
       rank() over(partition by categoryid order by unitprice desc)
       as rankprice,
       dense_rank() over(partition by categoryid order by unitprice desc)
       as denserankprice
from products;
```

| MS SQL                    |
| ------------------------- |
| ![](./img/ex8/mysql1.png) |

```sql
SELECT
    p1.productid,
    p1.productname,
    p1.unitprice,
    p1.categoryid,
    (SELECT COUNT(*) + 1 FROM products p2
     WHERE p2.categoryid = p1.categoryid
         AND p2.unitprice > p1.unitprice) AS rowno,
	(SELECT COUNT(*) + 1 FROM products p2
     WHERE p2.categoryid = p1.categoryid
         AND p2.unitprice > p1.unitprice) AS rankprice,
	(SELECT COUNT(DISTINCT p2.unitprice) + 1 FROM products p2
     WHERE p2.categoryid = p1.categoryid
         AND p2.unitprice > p1.unitprice) AS denserankprice
FROM
    products p1
ORDER BY p1.categoryid, rowno;
```

| MS SQL                    |
| ------------------------- |
| ![](./img/ex8/mysql1.png) |

> Widać zasadniczą różnicę działania dla kolumny `rowno` zwiększanie wartość musiałaby rosnąć dla zbioru produktów o tej samej cenie. Podzapytania róznią się dla takich samych wartości w kolumnie.

> `row_number` sortuje po unit price i numeruje wiersze.

> `rank` sortuje po unit price i przypisuje równe wartości dla tych samych cen.

> `dense_rank` sortuje po unit price i przypisuje równe wartości dla tych samych cen, ale nie ma przerw w numeracji.

Spróbuj uzyskać ten sam wynik bez użycia funkcji okna:

```sql
SELECT
    p1.productid,
    p1.productname,
    p1.unitprice,
    p1.categoryid,
    (SELECT COUNT(*) + 1
     FROM products p2
     WHERE p2.categoryid = p1.categoryid AND p2.unitprice > p1.unitprice) as rowno,
    (SELECT COUNT(DISTINCT p3.unitprice) + 1
     FROM products p3
     WHERE p3.categoryid = p1.categoryid AND p3.unitprice > p1.unitprice) as rankprice,
    (SELECT COUNT(DISTINCT p4.unitprice) + 1
     FROM products p4
     WHERE p4.categoryid = p1.categoryid AND p4.unitprice > p1.unitprice) as denserankprice
FROM products p1
ORDER BY p1.categoryid, rowno;
```

> To zapytanie wykorzystuje podzapytania do zliczenia liczby produktów w tej samej kategorii o wyższej cenie jednostkowej, co skutecznie klasyfikuje produkty. Należy pamiętać, że to podejście może być znacznie wolniejsze niż używanie funkcji okna, zwłaszcza w przypadku dużych zbiorów danych.

---

# Zadanie 9

Baza: Northwind, tabela product_history

Dla każdego produktu, podaj 4 najwyższe ceny tego produktu w danym roku. Zbiór wynikowy powinien zawierać:

- rok
- id produktu
- nazwę produktu
- cenę
- datę (datę uzyskania przez produkt takiej ceny)
- pozycję w rankingu

Uporządkuj wynik wg roku, nr produktu, pozycji w rankingu

Z powodu różnej składni dla wyboru roku w zapytaniu, dla różnych SZBD, stworzone zostały osobne zapytania dla każdego z nich.

**Zapytania**

_MS SQL_

```sql
WITH RankedPrice AS (
    SELECT
        YEAR(PH.Date) AS Year,
        PH.ProductID,
        PH.ProductName,
        PH.UnitPrice,
        ROW_NUMBER() OVER (PARTITION BY PH.ProductID, YEAR(PH.Date)
                           ORDER BY PH.UnitPrice DESC) AS PriceRank
    FROM product_history as PH
)

SELECT *
FROM RankedPrice
WHERE PriceRank <= 4
ORDER BY Year, ProductID, PriceRank;
```

_Postgres_

```sql
WITH RankedPrice AS (
    SELECT
        EXTRACT(year from PH.date) AS Year,
        PH.ProductID,
        PH.ProductName,
        PH.UnitPrice,
        ROW_NUMBER() OVER (PARTITION BY PH.ProductID, EXTRACT(year from PH.date)
                           ORDER BY PH.UnitPrice DESC) AS PriceRank
    FROM product_history as PH
)

SELECT *
FROM RankedPrice
WHERE PriceRank <= 4
ORDER BY Year, ProductID, PriceRank;
```

_SQLite_

```sql
WITH RankedPrice AS (
    SELECT
        strftime('%Y', PH.date) AS Year,
        PH.ProductID,
        PH.ProductName,
        PH.UnitPrice,
        ROW_NUMBER() OVER (PARTITION BY PH.ProductID, strftime('%Y', PH.date)
                           ORDER BY PH.UnitPrice DESC) AS PriceRank
    FROM product_history as PH
)

SELECT *
FROM RankedPrice
WHERE PriceRank <= 4
ORDER BY Year, ProductID, PriceRank;
```

**Wyniki zapytań**

| MS SQL                    | Postgres                   | SQLite                   |
| ------------------------- | -------------------------- | ------------------------ |
| ![](./img/ex9/mssql1.png) | ![](img/ex9/postgres1.png) | ![](img/ex9/sqlite1.png) |

Spróbuj uzyskać ten sam wynik bez użycia funkcji okna, porównaj wyniki, czasy i plany zapytań. Przetestuj działanie w różnych SZBD (MS SQL Server, PostgreSql, SQLite)

**Zapytania bez funkcji okna**

_MS SQL_

```sql
WITH RankedPrice AS (
    SELECT
        YEAR(PH.Date) AS Year,
        PH.ProductID,
        P.ProductName,
        PH.UnitPrice,
        PH.Date AS PriceDate,
        (
            SELECT COUNT(DISTINCT PH2.UnitPrice) + 1
            FROM product_history AS PH2
            WHERE YEAR(PH2.Date) = YEAR(PH.Date)
                  AND PH2.ProductID = PH.ProductID
                  AND PH2.UnitPrice > PH.UnitPrice
        ) AS PriceRank
    FROM product_history AS PH
    INNER JOIN products AS P ON PH.ProductID = P.ProductID
)

SELECT
    Year,
    ProductID,
    ProductName,
    UnitPrice AS Price,
    PriceDate AS Date,
    PriceRank
FROM RankedPrice
WHERE PriceRank <= 4
ORDER BY Year, ProductID, PriceRank;
```

_Postgres_

```sql
WITH RankedPrice AS (
    SELECT
        EXTRACT(year from PH.date) AS Year,
        PH.ProductID,
        P.ProductName,
        PH.UnitPrice,
        PH.Date AS PriceDate,
        (
            SELECT COUNT(DISTINCT PH2.UnitPrice) + 1
            FROM product_history AS PH2
            WHERE EXTRACT(year from PH2.date) = YEAR(PH.Date)
                  AND PH2.ProductID = PH.ProductID
                  AND PH2.UnitPrice > PH.UnitPrice
        ) AS PriceRank
    FROM product_history AS PH
    INNER JOIN products AS P ON PH.ProductID = P.ProductID
)

SELECT 
    Year,
    ProductID,
    ProductName,
    UnitPrice AS Price,
    PriceDate AS Date,
    PriceRank
FROM RankedPrice
WHERE PriceRank <= 4
ORDER BY Year, ProductID, PriceRank;
```

_SQLite_

```sql
WITH RankedPrice AS (
    SELECT
        strftime('%Y',  PH.date) AS Year,
        PH.ProductID,
        P.ProductName,
        PH.UnitPrice,
        PH.Date AS PriceDate,
        (
            SELECT COUNT(DISTINCT PH2.UnitPrice) + 1
            FROM product_history AS PH2
            WHERE strftime('%Y',  PH2.date) = strftime('%Y', PH.Date)
              AND PH2.ProductID = PH.ProductID
              AND PH2.UnitPrice > PH.UnitPrice
        ) AS PriceRank
    FROM product_history AS PH
             INNER JOIN products AS P ON PH.ProductID = P.ProductID
)

SELECT
    Year,
    ProductID,
    ProductName,
    UnitPrice AS Price,
    PriceDate AS Date,
    PriceRank
FROM RankedPrice
WHERE PriceRank <= 4
ORDER BY Year, ProductID, PriceRank;
```

| MS SQL                    | Postgres                   | SQLite                   |
| ------------------------- | -------------------------- | ------------------------ |
| ![](./img/ex9/mssql2.png) | ![](img/ex9/postgres2.png) | ![](img/ex9/sqlite2.png) |

**Czasy wykonania**

| Funkcja okna lub nie | MS SQL                        | Postgres                         | SQLite                         |
| -------------------- | ----------------------------- | -------------------------------- | ------------------------------ |
| Z funkcją okna       | ![](./img/ex9/mssql1time.png) | ![](img/ex9/postgres1time.png)   | ![](./img/ex9/sqlite1time.png) |
| Bez funkcji okna     | ![](./img/ex9/mssql2time.png) | ![](./img/ex9/postgres2time.png) | ![](./img/ex9/sqlite2time.png) |

**Plany wykonania**

| Funkcja okna lub nie | MS SQL                        | Postgres                         | SQLite                         |
| -------------------- | ----------------------------- | -------------------------------- | ------------------------------ |
| Z funkcją okna       | ![](./img/ex9/mssql1plan.png) | ![](img/ex9/postgres1plan.png)   | ![](./img/ex9/sqlite1plan.png) |
| Bez funkcji okna     | ![](./img/ex9/mssql2plan.png) | ![](./img/ex9/postgres2plan.png) | ![](./img/ex9/sqlite2plan.png) |

> W tym zadaniu, konieczne było skorzystanie z tabeli `product_history`, która posiada 2500 rekordów.

> Wyniki testów wyraźnie pokazują, że korzystanie z funkcji okna znacząco skraca czas wykonania zapytań w porównaniu z alternatywnym podejściem, które ich nie wykorzystuje. W każdym systemie zarządzania bazą danych zauważalne jest przyspieszenie, jednak różnice między użyciem funkcji okna a ich brakiem są najbardziej widoczne w przypadku SQLIte. W Postgres i MS SQL również obserwuje się znaczne skrócenie czasu wykonania zapytań przy użyciu funkcji okna.

> Koszt w przypadku wykorzystania funkcji okna jest znacznie niższy niezależnie od SZBD. Co do planów wykonania to dla `MS SQL` oraz `Postgres` plany są bardzo proste oraz podobne do siebie.

---

# Zadanie 10 - obserwacja

Funkcje `lag()`, `lead()`

Wykonaj polecenia, zaobserwuj wynik. Jak działają funkcje `lag()`, `lead()`

```sql
select productid,
       productname,
       categoryid, date, unitprice,
       lag(unitprice) over (partition by productid order by date) as previousprodprice,
       lead(unitprice) over (partition by productid order by date) as nextprodprice
from product_history
where productid = 1 and year (date) = 2022
order by date;

with t as (select productid, productname, categoryid, date, unitprice,
           lag(unitprice) over (partition by productid order by date) as previousprodprice,
           lead(unitprice) over (partition by productid order by date) as nextprodprice
from product_history
    )
select *
from t
where productid = 1 and year (date) = 2022
order by date;
```

| MS SQL                     |
| -------------------------- |
| ![](./img/ex10/mssql0.png) |

> Funckje `lag` i `lead` pozwalają na dostęp do wartości odpowiednio z poprzednich i kolejnych wierszy. Mogą być przydatne by porównywać wartości w różnych punktach czasu. Zastosowanie funkcji `lag(unitprice)` umożliwia pobranie ceny produktu z poprzedniego rekordu, które przez użycie funkcji okna i w niej order by date są posortowane według daty. Natomiast funkcja `lead(unitprice)` zwraca cenę produktu z następnego rekordu. Dzięki nim można porównywać bieżące wartości z cenami poprzednimi lub następnymi w uporządkowanym zestawie danych.

Spróbuj uzyskać ten sam wynik bez użycia funkcji okna, porównaj wyniki, czasy i plany zapytań. Przetestuj działanie w różnych SZBD (MS SQL Server, PostgreSql, SQLite)

**Wyniki bez funkcji okna**

_Zapytanie 1_

```sql
SELECT
    ph1.productid,
    ph1.productname,
    ph1.categoryid,
    ph1.date,
    ph1.unitprice AS currentprodprice,
    ph2.unitprice AS previousprodprice,
    ph3.unitprice AS nextprodprice
FROM product_history as ph1
LEFT JOIN product_history as ph2 ON ph1.productid = ph2.productid
                            AND ph1.date > ph2.date
                            AND year(ph1.date) = 2022
                            AND ph2.date = (
                                SELECT MAX(date)
                                FROM product_history
                                WHERE productid = ph1.productid
                                AND date < ph1.date
                                AND year(date) = 2022
                       )
LEFT JOIN product_history as ph3 ON ph1.productid = ph3.productid
                            AND ph1.date < ph3.date
                            AND year(ph1.date) = 2022
                            AND ph3.date = (
                                SELECT MIN(date)
                                FROM product_history
                                WHERE productid = ph1.productid
                                AND date > ph1.date
                                AND year(date) = 2022
                       )
WHERE ph1.productid = 1 AND year(ph1.date) = 2022
ORDER BY ph1.date;
```

_Zapytanie 2_

```sql
WITH t AS (
    SELECT
        ph1.productid,
        ph1.productname,
        ph1.categoryid,
        ph1.date,
        ph1.unitprice AS currentprodprice,
        ph2.unitprice AS previousprodprice,
        ph3.unitprice AS nextprodprice
FROM product_history as ph1
LEFT JOIN product_history as ph2 ON ph1.productid = ph2.productid
                            AND ph1.date > ph2.date
                            AND year(ph1.date) = 2022
                            AND ph2.date = (
                                SELECT MAX(date)
                                FROM product_history
                                WHERE productid = ph1.productid
                                AND date < ph1.date
                                AND year(date) = 2022
                           )
LEFT JOIN product_history as ph3 ON ph1.productid = ph3.productid
                            AND ph1.date < ph3.date
                            AND year(ph1.date) = 2022
                            AND ph3.date = (
                                SELECT MIN(date)
                                FROM product_history
                                WHERE productid = ph1.productid
                                AND date > ph1.date
                                AND year(date) = 2022
                           )
)
SELECT *
FROM t
WHERE productid = 1 AND year(date) = 2022
ORDER BY date;
```

**Wyniki zapytań**

| Zapytanie | MS SQL                     | Postgres                    | SQLite                    |
| --------- | -------------------------- | --------------------------- | ------------------------- |
| 1         | ![](./img/ex10/mssql1.png) | ![](img/ex10/postgres1.png) | ![](img/ex10/sqlite1.png) |
| 2         | ![](./img/ex10/mssql2.png) | ![](img/ex10/postgres2.png) | ![](img/ex10/sqlite2.png) |

**Czasy wykonania**

| Zapytanie | MS SQL | Postgres | SQLite |
| --------- | ------ | -------- | ------ |
| 1         | 2.4 s  | 1.5 s    | 1.2 s  |
| 2         | 2.3 s  | 1.7 s    | 1.0 s  |

**Plany wykonania**

| Zapytanie | MS SQL                         | Postgres                        | SQLite                          |
| --------- | ------------------------------ | ------------------------------- | ------------------------------- |
| 1         | ![](./img/ex10/mssql1plan.png) | ![](img/ex10/postgres1plan.png) | ![](./img/ex10/sqlite1plan.png) |
| 2         | ![](./img/ex10/mssql2plan.png) | ![](img/ex10/postgres2plan.png) | ![](./img/ex10/sqlite2plan.png) |

> W tym zadaniu, konieczne było skorzystanie z tabeli `product_history`, która posiada 2500 rekordów.

> Zapytania z funkcjami okna wykonują się znacznie szybciej, są prostrze, czytelniejsze i bardziej zwięzłe. Zapytania bez funkcji okna są bardziej skomplikowane, wymagają złączeń oraz podzapytań, co sprawia, że są mniej czytelne. Zapytania z użyciem funkcji okna mają również wielokrotnie mniejszy koszt wykonania i prostszy plan wykonania niż ich odpowiedniki bez funkcji okna.

> W PostgreSQL i SQLite zauważalne jest nieznaczne przyspieszenie zapytań wykorzystujących funkcje okna w porównaniu z ich odpowiednikami, które nie korzystają z tych funkcji. Natomiast w przypadku SQL Servera zapytania bez funkcji okna są nieco szybsze niż te z ich użyciem.

# Zadanie 11

Baza: Northwind, tabele customers, orders, order details

Napisz polecenie które wyświetla inf. o zamówieniach

Zbiór wynikowy powinien zawierać:

- nazwę klienta, nr zamówienia,
- datę zamówienia,
- wartość zamówienia (wraz z opłatą za przesyłkę),
- nr poprzedniego zamówienia danego klienta,
- datę poprzedniego zamówienia danego klienta,
- wartość poprzedniego zamówienia danego klienta.

**Zapytanie**

```sql
with Data as (
    SELECT O.OrderID, C.CompanyName, O.OrderDate,
    O.Freight + sum(OD.UnitPrice * OD.Quantity * (1 - OD.Discount)) as Cost,
    lag(O.OrderID) over (partition by C.CustomerID order by O.OrderDate) as PrevOrderID,
    lag(O.OrderDate) over (partition by C.CustomerID order by O.OrderDate) as PrevOrderDate
FROM Orders as O
JOIN Customers as C on O.CustomerID = C.CustomerID
JOIN [Order Details] as OD on O.OrderID = OD.OrderID
GROUP BY O.OrderID, C.CustomerID, C.CompanyName, O.OrderDate, O.Freight)


SELECT Data.*,
    O.Freight + sum(OD.UnitPrice * OD.Quantity * (1 - OD.Discount)) as PrevCost
FROM Data
LEFT JOIN Orders as O on O.OrderID = PrevOrderID
LEFT JOIN [Order Details] as OD on O.OrderID = OD.OrderID
GROUP BY O.Freight, Data.OrderID, Data.CompanyName, Data.OrderDate, Data.Cost, Data.PrevOrderID, Data.PrevOrderDate
ORDER BY Data.OrderID;
```

**Wynik**

![](./img/ex11/mssql.png)

**Czas wykonania**

![](./img/ex11/mssqltime.png)

**Plan wykonania**

![](./img/ex11/mssqlplan.png)

> Zapytanie zostało sprawdzone zarówno na bazie danych MS SQL, jak i PostgreSQL. W każdym przypadku czas wykonania wyniósł mniej niż 500 ms. Analiza planu wykonania nie wykazała żadnych istotnych różnic między tymi systemami zarządzania bazą danych.

# Zadanie 12 - obserwacja

Funkcje `first_value()`, `last_value()`

Wykonaj polecenia, zaobserwuj wynik. Jak działają funkcje `first_value()`, `last_value()`. Skomentuj uzyskane wyniki.
Czy funkcja `first_value` pokazuje w tym przypadku najdroższy produkt w danej kategorii, czy funkcja `last_value()`
pokazuje najtańszy produkt? Co jest przyczyną takiego działania funkcji `last_value`. Co trzeba zmienić żeby funkcja
last_value pokazywała najtańszy produkt w danej kategorii

```sql
select productid,
       productname,
       unitprice,
       categoryid,
       first_value(productname) over (partition by categoryid
order by unitprice desc) first,
    last_value(productname) over (partition by categoryid
order by unitprice desc) last
from products
order by categoryid, unitprice desc;
```

**Wynik**

![](./img/ex12/postgres.png)

> Funkcje okna mają zasięg działania (RANGE). Jeśli używamy ORDER BY i nie podamy RANGE to domyślne wartości to: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. Oznacza, że wybierzemy najmniejszą wartość między pierwszym, a obecnym wierszem tabeli. W zadaniu mamy klauzulę: **order by categoryid, unitprice desc**, to tabela już jest posortowana po cenie, daltego otrzyujemy zawsze przedmiot z obecnego wiersza.

> Funkcja **first_value()** pokazuje najdroższy produkt w danej kategorii natomiast funkcja **last_value()** pokazuje wiersz, który posiadałby najwyższą wartość funkcji **row_number()** dla wierszy posiadających taką samą wartość funkcji **rank()** jak aktualnie badany wiersz. Zachowanie funkcji last_value() można zmienić ustawiając opcję range na between unbounded preceding and unbounded following.

> Aby funkcja **last_value()** pokazywała najtańszy produkt w danej kategorii należy zamienić domyślny zakres funkcji z **RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW** na **ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING**. Zmodyfikowane zapytanie wygląda następująco:

```sql
select productid, productname, unitprice, categoryid,
       first_value(productname) over (partition by categoryid order by unitprice desc
       ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) first,
       last_value(productname) over (partition by categoryid order by unitprice desc
       ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) last
from products
order by categoryid, unitprice desc;
```

Spróbuj uzyskać ten sam wynik bez użycia funkcji okna, porównaj wyniki, czasy i plany zapytań. Przetestuj działanie w różnych SZBD (MS SQL Server, PostgreSql, SQLite)

**Zapytania**

_MS SQL_

```sql
select p.productid, p.productname, p.unitprice, p.categoryid,
       (select top 1 p2.productname from product_history p2 where p2.CategoryID=p.CategoryID
       order by p2.UnitPrice desc) first,
       (select top 1 p2.productname from product_history p2 where p2.CategoryID=p.CategoryID
       order by p2.UnitPrice) last
from product_history p
order by p.categoryid, p.unitprice desc;
```

_PostgreSQL_

```sql
select p.productid, p.productname, p.unitprice, p.categoryid,
       (select p2.productname from product_history p2 where p2.CategoryID=p.CategoryID
       order by p2.UnitPrice desc limit 1) first,
       (select p2.productname from product_history p2 where p2.CategoryID=p.CategoryID
       order by p2.UnitPrice limit 1) last
from product_history p
order by p.categoryid, p.unitprice desc;
```

_SQLite_

```sql
select p.productid, p.productname, p.unitprice, p.categoryid,
       (select p2.productname from product_history p2 where p2.CategoryID=p.CategoryID
       order by p2.UnitPrice desc limit 1) first,
       (select p2.productname from product_history p2 where p2.CategoryID=p.CategoryID
       order by p2.UnitPrice limit 1) last
from product_history p
order by p.categoryid, p.unitprice desc;
```

> Bez użycia funkcji okna możemy uzyskać wyniki których potrzebujemy.

> W zadaniu tym należało użyć tabeli `product_history`, która posiada 2500 rekordów.

**Czasy wykonania**

| Zapytanie | MS SQL                         | Postgres                          | SQLite                          |
| --------- | ------------------------------ | --------------------------------- | ------------------------------- |
| 1         | ![](./img/ex12/mssql1time.png) | ![](./img/ex12/postgres1time.png) | ![](./img/ex12/sqlite1time.png) |
| 2         | ![](./img/ex12/mssql2time.png) | ![](./img/ex12/postgres2time.png) | ![](./img/ex12/sqlite2time.png) |

**Plany wykonania**

| Zapytanie | MS SQL                         | Postgres                        | SQLite                        |
| --------- | ------------------------------ | ------------------------------- | ----------------------------- |
| 1         | ![](./img/ex12/mssql1plan.png) | ![](img/ex12/postgres1plan.png) | ![](img/ex12/sqlite1plan.png) |
| 2         | ![](./img/ex12/mssql2plan.png) | ![](img/ex12/postgres2plan.png) | ![](img/ex12/sqlite2plan.png) |

> Wydajność funkcji okna jest najlepsza we wszystkich przypadkach. Widać znaczną różnicę między PostgreSQL a SQLite. W przypadku MS SQL oba zapytania wykonują się szybko. PostgreSQL okazał się być najwolniejszą bazą danych.

> Funkcje okna składały się z prostszych, liniowych ciągów operacji, podczas gdy zagnieżdżone zapytania wiązały się z bardziej drzewiastą strukturą planu. Wszystkie wersje zapytania na tabeli products wykonały się błyskawicznie.
> Jeśli chodzi o koszt, to w przypadku funkcji okna jest on znacznie niższy dla wszystkich SZBD.

> W przypadku MS SQL oraz zapytania bez funkcji okna, na planie zapytania widzimy 3 pełne skany tabeli oraz operację Nested Loops. Z pewnością wpływa to negatywnie na efektywność oraz końcowy czas wykonania zapytania. Mogłoby się wydawać, że bardziej rozgałęziony plan w tym przypadku w porównaniu do funkcji okna, która wykonuje operacje sekwencyjnie jest łatwiejszy do zrównoleglenia, jednak kosztowne operacje na tabeli sprawiają, że zapytanie bez funkcji okna wykonuje się wolniej. Dla porównania, zapytanie z funkcją okna wykonuje tylko jeden skan indeksu, co znacznie przyspiesza jego wykonanie.

---

# Zadanie 13

Baza: Northwind, tabele orders, order details

Napisz polecenie które wyświetla inf. o zamówieniach

Zbiór wynikowy powinien zawierać:

- Id klienta,
- nr zamówienia,
- datę zamówienia,
- wartość zamówienia (wraz z opłatą za przesyłkę),
- dane zamówienia klienta o najniższej wartości w danym miesiącu
  - nr zamówienia o najniższej wartości w danym miesiącu
  - datę tego zamówienia
  - wartość tego zamówienia
- dane zamówienia klienta o najwyższej wartości w danym miesiącu
  - nr zamówienia o najniższej wartości w danym miesiącu
  - datę tego zamówienia
  - wartość tego zamówienia

```sql
with Data as (
    SELECT o.CustomerID as CustomerID, o.OrderID, o.OrderDate,
    o.Freight+od.UnitPrice*od.Quantity-od.Discount as value
    FROM orders AS o
    JOIN orderdetails as od on od.OrderID = o.OrderID)

SELECT
    d.CustomerID, d.OrderDate, d.OrderDate, d.value,
    last_value(concat(d.OrderID,' ', d.OrderDate,' ', d.value)) over (partition by d.CustomerID order by d.value desc rows between unbounded preceding and unbounded following) min_value_order,
    first_value(concat(d.OrderID,' ', d.OrderDate,' ', d.value)) over (partition by d.CustomerID order by d.value desc) max_value_order
FROM Data as d
```

**Wynik**

![](./img/ex13/postgres.png)

**Czas wykonania**

![](./img/ex13/postgrestime.png)

**Plan wykonania**

![](./img/ex13/postgresplan.png)

> Zapytanie zostało przetestowane dla MsSql, Postgres i SQLite, a czas wykonania wynosił około 0.5 sekundy. Nie zaobserwowano znaczących różnic w wydajności między poszczególnymi systemami baz danych.

---

# Zadanie 14

Baza: Northwind, tabela product_history

Napisz polecenie które pokaże wartość sprzedaży każdego produktu narastająco od początku każdego miesiąca. Użyj funkcji
okna

Zbiór wynikowy powinien zawierać:

- id pozycji
- id produktu
- datę
- wartość sprzedaży produktu w danym dniu
- wartość sprzedaży produktu narastające od początku miesiąca

```sql
with Data as (
    SELECT
    id,
    productid,
    date,
    sum(unitprice*quantity) over(partition by productid,convert(date,date)) dayValue
    FROM product_history
)

SELECT distinct
    d.*,
    sum(d.dayValue) over(partition by d.productid, year(d.date), month(d.date)
    order by day(d.date) rows between unbounded preceding and current row) as accumulated
FROM Data as d
ORDER BY d.date
```

**Wynik**

![](./img/ex14/mssql1.png)

> Warto zauważyć, że w w wyniku zapytania otrzymujemy 'powtórki'. Zapytanie zwraca nam po 3 takie same produkty na każdy dzień lecz z inną wartośćia accumulated. Nie wynika to z błedu, tylko z faktu, że tabela product_history została utworzona z takim błędem. Mimo wszystko logika zapytania jest poprawna i pozostaje taka sama. Wartość accumulated jest sumą wartości sprzedaży produktu od początku miesiąca.

Spróbuj wykonać zadanie bez użycia funkcji okna. Spróbuj uzyskać ten sam wynik bez użycia funkcji okna, porównaj wyniki, czasy i plany zapytań. Przetestuj działanie w różnych SZBD (MS SQL Server, PostgreSql, SQLite)

**Zapytania**

_MS SQL_

```sql
with Data as (
    SELECT
    id,
    productid,
    date,
    sum(unitprice*quantity) as dayValue
    FROM product_history
    WHERE productid = 1
    GROUP BY productid, convert(date, date), id
)

SELECT distinct
    d.*,
    (SELECT sum(d2.dayValue)
     FROM Data d2
     WHERE d2.productid = d.productid and
           year(d2.date) = year(d.date) and
           month(d2.date) = month(d.date) and
           day(d2.date) <= day(d.date)
    ) AS accumulated
FROM Data as d
order by d.date
```

_Postgres_

```sql
with Data as (
    SELECT
    id,
    productid,
    date,
    sum(unitprice*quantity) as dayValue
    FROM product_history
    GROUP BY productid, date, id
)

SELECT distinct
    d.*,
    sum(d2.dayValue) over(partition by d.productid, date_part('Year', d.date),
    date_part('Month', d.date) order by date_part('Day', d.date) ) as accumulated
FROM Data as d
JOIN Data as d2 ON d.productid = d2.productid and
                   date_part('Year', d.date) = date_part('Year', d2.date) and
                   date_part('Month', d.date) = date_part('Month', d2.date) and
                   date_part('Day', d.date) >= date_part('Day', d2.date)
ORDER BY d.date
```

_SQLite_

```sql
with Data as (
    SELECT
    id,
    productid,
    date,
    sum(unitprice*quantity) as dayValue
    FROM product_history
    WHERE productid=1
    GROUP BY productid, date, id
)

SELECT
    d.*,
    sum(d2.dayValue) over(partition by d.productid, strftime('%Y %m', d.date)
    order by strftime('%d', d.date) ) as accumulated
FROM Data as d
JOIN Data as d2 on d.productid = d2.productid and
                   strftime('%Y %m', d.date) = strftime('%Y %m', d2.date) and
                   strftime('%d', d.date) >= strftime('%d', d2.date)
ORDER BY d.date
```

**Czasy wykonania**

| Z funkcją okna lub bez | MS SQL                         | Postgres                          | SQLite                          |
| ---------------------- | ------------------------------ | --------------------------------- | ------------------------------- |
| Z funkcją okna         | ![](./img/ex14/mssql1time.png) | ![](./img/ex14/postgres1time.png) | ![](./img/ex14/sqlite1time.png) |
| Bez funkcji okna       | 10 min + (przerwane)           | 10 min + (przerwane)              | 10 min + (przerwane)            |

**Plany wykonania**

| Z funkcją okna lub bez | MS SQL                         | Postgres                        | SQLite                        |
| ---------------------- | ------------------------------ | ------------------------------- | ----------------------------- |
| Z funkcją okna         | ![](./img/ex14/mssql1plan.png) | ![](img/ex14/postgres1plan.png) | ![](img/ex14/sqlite1plan.png) |
| Bez funkcji okna       | ![](./img/ex14/mssql2plan.png) | ![](img/ex14/postgres2plan.png) | ![](img/ex14/sqlite2plan.png) |

> Dla zapytania bez funkcji okna PostgreSQL wydaje się lepszy od SQL Servera pod względem równoległego wykonywania operacji ("Paralellism (Gather Streams)") w planie wykonania, co przekłada się na rzeczywisty czas wykonania. SQLite w tym przypadku nie radził sobie dobrze z zapytaniem o takim stopniu skomplikowania i takiej liczbie wierszy. Wynikowy czas wykonania zapytania z funkcją okna może być akceptowalny, ale już bez niej nie. Jeśli chodzi o zapytanie bez funkcji okna to mamy skany indeksów, osobne obliczanie skalarów i kosztowne agregacje.

---

# Zadanie 15

Wykonaj kilka "własnych" przykładowych analiz. Czy są jeszcze jakieś ciekawe/przydatne funkcje okna (z których nie korzystałeś w ćwiczeniu)? Spróbuj ich użyć w zaprezentowanych przykładach.

**Porównanie działania klauzuli `RANGE` z `ROWS`**

**Zapytania**

_Klauzula `RANGE`_

```sql
WITH Data AS (
    SELECT
    o.customerid,
    o.orderdate,
    SUM(od.unitprice * od.quantity) as sum
    FROM orders as o
    LEFT JOIN orderdetails od ON o.orderid = od.orderid
    GROUP BY o.customerid, o.orderdate
)

SELECT customerid,
       orderdate,
       sum,
       AVG(sum) OVER (
           PARTITION BY customerid
           ORDER BY orderdate ASC
           RANGE BETWEEN INTERVAL '31' DAY PRECEDING AND CURRENT ROW
           ) AS moving_avg
FROM Data
```

_Klauzula `ROWS`_

```sql
WITH Data AS (
    SELECT
    o.orderdate,
    SUM(od.unitprice * od.quantity) as sum
    FROM orders o
    LEFT JOIN orderdetails od ON o.orderid = od.orderid
    GROUP BY o.orderdate
)

SELECT orderdate,
       SUM(sum) OVER (
            ORDER BY orderdate
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 FOLLOWING
            ) as sum_till_this_date
FROM Data
```

> Z wykorzystaniem klauzuli `RANGE` możemy zdefiniować zakres danych, który ma być brany pod uwagę podczas analizy. W tym konkretnym przypadku używamy tej klauzuli do obliczenia tzw. średniej kroczącej, czyli średniej z ostatnich 31 dni. Ponadto korzystamy z specjalnej konstrukcji obsługiwanej przez niektóre silniki baz danych a mianowicie `INTERVAL '31' DAY PRECEDING`.

> Korzystając z klauzuli ROWS, analiza jest również wykonywana dla każdej kategorii produktu, ale zakres danych jest definiowany nieco inaczej, o czym mowa w kolejnym punkcie. Opisana funkcja sumuje zamówienia z wszystkich poprzednich dni oraz następnego dnia dla danego wiersza.

**Wyniki**

| Klauzula `RANGE`              | Klauzula `ROWS`               |
| ----------------------------- | ----------------------------- |
| ![](./img/ex15/postgres1.png) | ![](./img/ex15/postgres2.png) |

**Czas wykonania**

| Klauzula `RANGE`                  | Klauzula `ROWS`                   |
| --------------------------------- | --------------------------------- |
| ![](./img/ex15/postgres1time.png) | ![](./img/ex15/postgres2time.png) |

**Plany wykonania**

| Klauzula `RANGE`                  | Klauzula `ROWS`                   |
| --------------------------------- | --------------------------------- |
| ![](./img/ex15/postgres1plan.png) | ![](./img/ex15/postgres2plan.png) |

> Klauzula `ROWS` umożliwia określenie zakresu za pomocą liczby wierszy poprzedzających lub następujących po obecnym wierszu.

> Z kolei klauzula `RANGE` pozwala określić ramkę za pomocą wartości wierszy poprzedzających lub następujących po obecnym wierszu. Z tego powodu klauzula `RANGE` wymaga podania dokładnie jednej kolumny, według której będziemy sortować tabelę.

> Bardzo istotna uwaga! Jeśli nie używamy klauzuli ORDER BY to przetwarzana ramka jest równa: ROWS `BETWEEN UNBOUNDED PRECEDING AND UNOBUNDED FOLLOWING`, jeżeli skorzystliśmy z klauzuli ORDER BY to domyślnie jest to równoznaczne z `ROWS BETWEEN UNBOUNDED PREEDING AND CURRENT ROW`.

> Możemu zauważyć, że czas wykonywania się klauzuli `ROWS` jest dużo szybszy niż Klasuzuli `RANGE`.

Punktacja

|         |     |
| ------- | --- |
| zadanie | pkt |
| 1       | 0,5 |
| 2       | 0,5 |
| 3       | 1   |
| 4       | 1   |
| 5       | 0,5 |
| 6       | 2   |
| 7       | 2   |
| 8       | 0,5 |
| 9       | 2   |
| 10      | 1   |
| 11      | 2   |
| 12      | 1   |
| 13      | 2   |
| 14      | 2   |
| 15      | 2   |
| razem   | 20  |
