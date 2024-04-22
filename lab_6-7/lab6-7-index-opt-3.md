# Indeksy, optymalizator <br>Lab 6-7

<!-- <style scoped>
 p,li {
    font-size: 12pt;
  }
</style>  -->

<!-- <style scoped>
 pre {
    font-size: 8pt;
  }
</style>  -->

---

**Imię i nazwisko:**

- **Szymon Budziak**
- **Piotr Ludynia**

---

Celem ćwiczenia jest zapoznanie się z planami wykonania zapytań (execution plans), oraz z budową i możliwością wykorzystaniem indeksów (cz. 2.)

Swoje odpowiedzi wpisuj w miejsca oznaczone jako:

---

> Wyniki:

```sql
--  ...
```

---

Ważne/wymagane są komentarze.

Zamieść kod rozwiązania oraz zrzuty ekranu pokazujące wyniki, (dołącz kod rozwiązania w formie tekstowej/źródłowej)

Zwróć uwagę na formatowanie kodu

## Oprogramowanie - co jest potrzebne?

Do wykonania ćwiczenia potrzebne jest następujące oprogramowanie

- MS SQL Server,
- SSMS - SQL Server Management Studio
- przykładowa baza danych AdventureWorks2017.

Oprogramowanie dostępne jest na przygotowanej maszynie wirtualnej

## Przygotowanie

Stwórz swoją bazę danych o nazwie lab6.

```sql
create database lab5
go

use lab5
go
```

Zamiast lab5 musieliśmy nazwać bazę lab6 ze względu na kolizję nazw z poprzednim laboratorium:

```sql
create database lab6
go

use lab6
go
```

## Dokumentacja

Obowiązkowo:

- [https://docs.microsoft.com/en-us/sql/relational-databases/indexes/indexes](https://docs.microsoft.com/en-us/sql/relational-databases/indexes/indexes)
- [https://docs.microsoft.com/en-us/sql/relational-databases/indexes/create-filtered-indexes](https://docs.microsoft.com/en-us/sql/relational-databases/indexes/create-filtered-indexes)

# Zadanie 1

Skopiuj tabelę Product do swojej bazy danych:

```sql
select * into product from adventureworks2017.production.product
```

Stwórz indeks z warunkiem przedziałowym:

```sql
create nonclustered index product_range_idx
    on product (productsubcategoryid, listprice) include (name)
where productsubcategoryid >= 27 and productsubcategoryid <= 36
```

Sprawdź, czy indeks jest użyty w zapytaniu:

```sql
select name, productsubcategoryid, listprice
from product
where productsubcategoryid >= 27 and productsubcategoryid <= 36
```

Sprawdź, czy indeks jest użyty w zapytaniu, który jest dopełnieniem zbioru:

```sql
select name, productsubcategoryid, listprice
from product
where productsubcategoryid < 27 or productsubcategoryid > 36
```

Skomentuj oba zapytania. Czy indeks został użyty w którymś zapytaniu, dlaczego? Czy indeks nie został użyty w którymś zapytaniu, dlaczego? Jak działają indeksy z warunkiem?

---

> W pierwszym zapytaniu indeks zostaje użyty. Zapytanie zwraca 17 wartości

![](img/ex1/query1.png)

> Jednak drugie zapytanie wykonuje się bez użycia indeksu. Wybierane jest 278 wartości

![](img/ex1/query2.png)

> Indeks jest użyty w zapytaniu, które zawiera warunek użyty przy tworzeniu go a w przeciwnym przypadku nie. Dzieje się tak, ponieważ optymalizator sprawdza, czy warunek z zapytania jest obecny w indeksie i na jego podstawie decyduje, czy użyje indeksu w wykonaniu zapytania.

```sql
--  sprawdzany warunek:
--[...]
where productsubcategoryid >= 27 and productsubcategoryid <= 36
--[...]
```

> Przetestowaliśmy jeszcze jedno zapytanie. Zamieniamy koniunkcję na alternatywę. Cały zbiór będący wynikiem pierwszego zapytania jest w nim zawarty, jednak występują też tam wartości z poza niego (na przykład takie w których `productsubcategoryid` jest większe mniejsze niż 27 a `productsubcategoryid` dalej jest mniejsze bądź równe 36). W tym przypadku indeks również nie został użyty.

```sql
select name, productsubcategoryid, listprice
from product
where productsubcategoryid >= 27 or productsubcategoryid <= 36
```

![](img/ex1/query3.png)

# Zadanie 2 – indeksy klastrujące

Celem zadania jest poznanie indeksów klastrujących![](file:////Users/rm/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image001.jpg)

Skopiuj ponownie tabelę SalesOrderHeader do swojej bazy danych:

```sql
select * into salesorderheader2 from adventureworks2017.sales.salesorderheader
```

Wypisz tysiąc pierwszych zamówień:

```sql
select top 1000 * from salesorderheader2
order by orderdate
```

Stwórz indeks klastrujący według OrderDate:

```sql
create clustered index order_date2_idx on salesorderheader2(orderdate)
```

Wypisz ponownie tysiąc pierwszych zamówień. Co się zmieniło?

---

> Wypisane zamówenia wyglądają tak samo

Wyniki dla zapytania 1:

![](img/ex2/results1.png)

Wyniki dla zapytania 2:

![](img/ex2/results2.png)

> Zmienia się jednak plan wykonania zapytania:

Plan dla zapytania 1:

![](img/ex2/plan1.png)

Plan dla zapytania 2:

![](img/ex2/plan2.png)

> Użycie indeksu znacząco ogranicza czas ze względu na usunięcie sortowania. Przy tworzeniu indeksu nie specyfikujemy bezpośrednio tego, że musi być posortowany, jednak użycie go sortowanie. Można z tego wywnioskować, że domyślnie tworzony jest indeks posortowany.

Sprawdź zapytanie:

```sql
select top 1000 * from salesorderheader2
where orderdate between '2010-10-01' and '2011-06-01'
```

Dodaj sortowanie według OrderDate ASC i DESC. Czy indeks działa w obu przypadkach. Czy wykonywane jest dodatkowo sortowanie?

---

> Sprawdziliśmy 3 zapytania:

```sql
--query 3
select top 1000 * from salesorderheader2
where orderdate between '2010-10-01' and '2011-06-01'

--query 4
select top 1000 * from salesorderheader2
where orderdate between '2010-10-01' and '2011-06-01'
order by orderdate asc

--query 5
select top 1000 * from salesorderheader2
where orderdate between '2010-10-01' and '2011-06-01'
order by orderdate desc
```

Wyniki dla zapytania 3:

![](img/ex2/results3.png)

Wyniki dla zapytania 4:

![](img/ex2/results4.png)

Wyniki dla zapytania 5:

![](img/ex2/results5.png)

> Wyniki dwóch pierwszych zapytań wyglądają tak samo. Przy wykonywaniu zapytania pierwszego, - bez spacyfikowania kolejności, - dostajemy taki sam wynik jak przy kolejności rosnącej. Oznacza to, że właśnie w takiej kolejności posortowany jest indeks.

Plan dla zapytania 3:

![](img/ex2/plan3.png)

Plan dla zapytania 4:

![](img/ex2/plan4.png)

Plan dla zapytania 5:

![](img/ex2/plan5.png)

> Plany wykonania wszystkich trzech zapytań wyglądają tak samo.

# Zadanie 3 – indeksy column store

Celem zadania jest poznanie indeksów typu column store![](file:////Users/rm/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image001.jpg)

Utwórz tabelę testową:

```sql
create table dbo.saleshistory(
 salesorderid int not null,
 salesorderdetailid int not null,
 carriertrackingnumber nvarchar(25) null,
 orderqty smallint not null,
 productid int not null,
 specialofferid int not null,
 unitprice money not null,
 unitpricediscount money not null,
 linetotal numeric(38, 6) not null,
 rowguid uniqueidentifier not null,
 modifieddate datetime not null
 )
```

Załóż indeks:

```sql
create clustered index saleshistory_idx
on saleshistory(salesorderdetailid)
```

Wypełnij tablicę danymi:

(UWAGA `GO 100` oznacza 100 krotne wykonanie polecenia. Jeżeli podejrzewasz, że Twój serwer może to zbyt przeciążyć, zacznij od GO 10, GO 20, GO 50 (w sumie już będzie 80))

```sql
insert into saleshistory
 select sh.*
 from adventureworks2017.sales.salesorderdetail sh
go 100
```

Sprawdź jak zachowa się zapytanie, które używa obecny indeks:

```sql
select productid, sum(unitprice), avg(unitprice), sum(orderqty), avg(orderqty)
from saleshistory
group by productid
order by productid
```

Załóż indeks typu ColumnStore:

```sql
create nonclustered columnstore index saleshistory_columnstore
 on saleshistory(unitprice, orderqty, productid)
```

Sprawdź różnicę pomiędzy przetwarzaniem w zależności od indeksów. Porównaj plany i opisz różnicę.

---

Zapytanie z indeksem klastrowym

![](img/ex3/plan1.png)

Zapytanie z indeksem ColumnStore

![](img/ex3/plan2.png)

> Indeks typu ColumnStore w przeciwieństwie do zwykłych indeksów ustawia kolejność pamięci kolumnami, a nie wierszami. Przez to, zapytanie, które bierze pod uwagę całość kolumny w celu pogrupowania lub obliczenia jej średnich wartości może wykonać się szybciej i prościej - bez dodania równoległości.

# Zadanie 4 – własne eksperymenty

Należy zaprojektować tabelę w bazie danych, lub wybrać dowolny schemat danych (poza używanymi na zajęciach), a następnie wypełnić ją danymi w taki sposób, aby zrealizować poszczególne punkty w analizie indeksów. Warto wygenerować sobie tabele o większym rozmiarze.

Do analizy, proszę uwzględnić następujące rodzaje indeksów:

- Klastrowane (np.  dla atrybutu nie będącego kluczem głównym)
- Nieklastrowane
- Indeksy wykorzystujące kilka atrybutów, indeksy include
- Filtered Index (Indeks warunkowy)
- Kolumnowe

## Analiza

Proszę przygotować zestaw zapytań do danych, które:

- wykorzystują poszczególne indeksy
- które przy wymuszeniu indeksu działają gorzej, niż bez niego (lub pomimo założonego indeksu, tabela jest w pełni skanowana)
  Odpowiedź powinna zawierać:
- Schemat tabeli
- Opis danych (ich rozmiar, zawartość, statystyki)
- Trzy indeksy:
- Opis indeksu
- Przygotowane zapytania, wraz z wynikami z planów (zrzuty ekranow)
- Komentarze do zapytań, ich wyników
- Sprawdzenie, co proponuje Database Engine Tuning Advisor (porównanie czy udało się Państwu znaleźć odpowiednie indeksy do zapytania)

> Wyniki:

### Klastrowane (np. dla atrybutu nie będącego kluczem głównym)

> Pierwszy eksperyment, polega na stworzeniu indeksu klastrowego dla atrybutu, który nie jest kluczem głównym tabeli. W przypadku, gdy atrybut nie jest kluczem głównym, indeks klastrowy jest tworzony na podstawie klucza głównego. W przypadku, gdy atrybut jest kluczem głównym, indeks klastrowy jest tworzony na podstawie tego atrybutu.

**Schemat tabeli**

Tworzymy tabelę `Orders` z następującymi kolumnami:

- **OrderID**
- **CustomerID**
- **OrderDate**
- **OrderPrice**

```sql
CREATE TABLE Orders (
  OrderID INT NOT NULL PRIMARY KEY,
  CustomerID INT NOT NULL,
  OrderDate DATE NOT NULL,
  OrderPrice DECIMAL(10, 2) NOT NULL
)
```

Wypełniamy tabelę przykładowymi danymi:

```sql
DECLARE @count INT = 0

WHILE @count < 100000
BEGIN
  INSERT INTO Orders (OrderID, CustomerID, OrderDate, OrderPrice) VALUES (
    @count,
    @count % 100,
    DATEADD(DAY, @count % 365, '2020-01-01'),
    ROUND(RAND() * 100, 2)
  )
  SET @count = @count + 1
END
```

Dodajemy indeks klastrowany dla kolumny `OrderDate`, która nie jest kluczem głównym tabeli `Orders`:

```sql
CREATE CLUSTERED INDEX Index_OrderDate ON Orders (OrderDate);
```

**Przykładowe zapytania**

Wykonujemy teraz przykładowe zapytania. Pierwsze zwróci nam wszystkie zamówienia z danego dnia i będzie to zapytanie, które będzi korzystało z indeksu klastrowanego. Drugie, które będzie odwoływało się w klauzuli where do klucza głównego nie będzie korzystało z naszego wcześniej utworzonego indeksu klastrowanego. Zostanie wykonane porównanie działania zapytania z indeksem i bez niego. Przedstawione zostaną wyniki, plany wykonania oraz napisane zostaną wnioski.

```sql
SELECT * FROM Orders WHERE OrderDate = '2020-02-14'
```

```sql
SELECT * FROM Orders WHERE OrderID = 58
```

**Wyniki**

| Zapytanie | Wynik                   |
| --------- | ----------------------- |
| 1         | ![](img/ex4/query1.png) |
| 2         | ![](img/ex4/query2.png) |

**Plany wykonania**

| Zapytanie | Plan wykonania              |
| --------- | --------------------------- |
| 1         | ![](img/ex4/query1plan.png) |
| 2         | ![](img/ex4/query2plan.png) |

**Plany po zmianie indeksu**

| Zapytanie | Plan wykonania               |
| --------- | ---------------------------- |
| 1         | ![](img/ex4/query1plan2.png) |
| 2         | ![](img/ex4/query2plan2.png) |

**Komantarz**

> Możemy zauważyć, że w przypadku zapytania, które korzysta z indeksu klastrowanego, czas wykonania zapytania jest znacznie krótszy. W przypadku zapytania, które nie korzysta z indeksu klastrowanego, czas wykonania zapytania jest dłuższy. W przypadku zapytania, które korzysta z indeksu klastrowanego, plan wykonania zapytania jest prostszy, a w przypadku zapytania, które nie korzysta z indeksu klastrowanego, plan wykonania zapytania jest bardziej skomplikowany. Różnice jednak nie są bardzo duże, bo są to tysięczne sekundy, ale w przypadku korzystania z indeksu klastrowanego, możemy zaobserwować na schemtach wykonywanie `Seek` w przeciwieństwie do `Scan` w przypadku niekorzystania z indeksu klastrowanego.

> Aby móc użyć stworzonego indeksu należało usunąc już isntiejący dla Primary Key. Zostało to wykonane następującą komendą:

```sql
ALTER TABLE Orders
DROP CONSTRAINT PK__Orders__C3905BAF4281CDA8;
```

### Nieklastrowane

> Drugi eksperyment polega na użyciu indeksu nieklastrowego. Indeks nieklastrowy jest indeksem, który nie zmienia kolejności wierszy w tabeli. Indeks nieklastrowy jest tworzony na kolumnach, które nie są kluczami głównymi tabeli.

**Schemat tabeli**

Tworzymy tabelę `Products` z następującymi kolumnami:

- **ProductID**
- **ProductName**
- **CategoryID**
- **ProductPrice**

```sql
CREATE TABLE Products (
  ProductID INT NOT NULL PRIMARY KEY,
  ProductName NVARCHAR(50) NOT NULL,
  CategoryID INT NOT NULL,
  ProductPrice DECIMAL(10, 2) NOT NULL
)
```

Wypełniamy tabelę przykładowymi danymi:

```sql
DECLARE @count INT = 0

WHILE @count < 100000
BEGIN
  INSERT INTO Products (ProductID, ProductName, CategoryID, ProductPrice) VALUES (
    @count,
    CONCAT('Product', @count),
    @count % 10,
    ROUND(RAND() * 100, 2)
  )
  SET @count = @count + 1
END
```

Dodajemy indeks nieklastrowany dla kolumny `CategoryID`:

```sql
CREATE NONCLUSTERED INDEX Index_CategoryID ON Products (CategoryID);
```

**Przykładowe zapytania**

Wykonujemy teraz przykładowe zapytania. Pierwsze zwróci nam wszystkie produkty z danej kategorii i będzie to zapytanie, które nie będzie korzystało z indeksu nieklastrowego. Drugie, które będzie bezpośrednio korzystało z indeksu w klauzuli WITH. Zostanie wykonane porównanie działania zapytania z indeksem i bez niego. Przedstawione zostaną wyniki, plany wykonania oraz napisane zostaną wnioski.

```sql
SELECT * FROM Products WHERE CategoryID = 5
```

```sql
SELECT * FROM Products WITH(INDEX(Index_CategoryID)) WHERE CategoryID = 5
```

**Wyniki**

| Zapytanie | Wynik                   |
| --------- | ----------------------- |
| 1         | ![](img/ex4/query3.png) |
| 2         | ![](img/ex4/query4.png) |

**Plany wykonania**

| Zapytanie | Plan wykonania              |
| --------- | --------------------------- |
| 1         | ![](img/ex4/query3plan.png) |
| 2         | ![](img/ex4/query4plan.png) |

**Komantarz**

> W przypadku indeksu nieklastrowego, zapytanie wykonuje się dłużej, ponieważ musi przeszukać całą tabelę. W przypadku korzystania z indeksu, zapytanie wykonuje się szybciej, ponieważ optymalizator korzysta z indeksu, który jest posortowany i zawiera tylko interesujące nas wartości. W przypadku indesku klastrowego wykonujemy `Scan` w przeciwieństwie do `Nested Loop` który jest następnie rozbijany na `Index Seek` oraz `Key Lookup`. Powoduje to, że zapytanie wykonuje się nieznacznie dłużej.

### Indeksy wykorzystujące kilka atrybutów, indeksy include

> Trzeci ekperyment polega na użyciu indeksu wykorzystującego kilka atrybutów, czyli indeksu include. Polega on na dodaniu do indeksu dodatkowych kolumn, które nie są kluczami indeksu, ale są dodawane do indeksu, aby zwiększyć jego wydajność.

**Schemat tabeli**

Tworzymy tabelę `Employees` z następującymi kolumnami:

- **EmployeeID**
- **Name**
- **Surname**
- **City**
- **Salary**

```sql
CREATE TABLE Employees (
  EmployeeID INT NOT NULL PRIMARY KEY,
  Name NVARCHAR(50) NOT NULL,
  Surname NVARCHAR(50) NOT NULL,
  City NVARCHAR(30) NOT NULL,
  Salary DECIMAL(10, 2) NOT NULL
)
```

Wypełniamy tabelę przykładowymi danymi:

```sql
DECLARE @count INT = 0

WHILE @count < 100000
BEGIN
  INSERT INTO Employees (EmployeeID, Name, Surname, City, Salary)
  VALUES (
    @count,
    CONCAT('Name', @count),
    CONCAT('Surname', @count),
    CONCAT('City', @count % 20),
    ROUND(RAND() * 10000, 2)
  )
  SET @count = @count + 1
END
```

Dodajemy indeks nieklastrowany dla kolumn `City` i `Salary`, jako indeksy wykorzystujące kilka atrybutów - include:

```sql
CREATE NONCLUSTERED INDEX Index_City_Salary ON Employees (City) INCLUDE (Salary);
```

**Przykładowe zapytania**

Wykonujemy teraz przykładowe zapytania. Pierwsze zwróci nam miasto oraz średnie zarobki w mieście `City1`, które nie będzie korzystało z utworzonego indeksu. Drugie, które będzie korzystało z indeksu, ale nie bezpośrednio i zwróci nam imie, nazwisko oraz zarobki wszystkich pracowników w mieście `City1` oraz których zarobki są poniżej 5000. Oraz trzecie, które będzie korzystało bezpośrednio z indeksu w klauzuli WITH. Zostanie wykonane porównanie działania zapytania z indeksem i bez niego. Przedstawione zostaną wyniki, plany wykonania oraz napisane zostaną wnioski.

```sql
SELECT City, AVG(Salary)
FROM Employees
WHERE City = 'City1'
GROUP BY City
```

```sql
SELECT Name, Surname, Salary
FROM Employees
WHERE City = 'City1' AND Salary < 5000
```

```sql
SELECT Name, Surname, AVG(Salary) as AvgSalary
FROM Employees WITH(INDEX(Index_City_Salary))
WHERE City = 'City1' AND Salary < 5000
GROUP BY Name, Surname
```

**Wyniki**

| Zapytanie | Wynik                   |
| --------- | ----------------------- |
| 1         | ![](img/ex4/query5.png) |
| 2         | ![](img/ex4/query6.png) |
| 3         | ![](img/ex4/query7.png) |

**Plany wykonania**

| Zapytanie | Plan wykonania              |
| --------- | --------------------------- |
| 1         | ![](img/ex4/query5plan.png) |
| 2         | ![](img/ex4/query6plan.png) |
| 3         | ![](img/ex4/query7plan.png) |

**Komantarz**

> W tym ekperymencie przetestowane zostały 3 zapytania. Możemy zauważyć, że w przypadku zapytania, które ni używa indeksu, cały plan składa się z 3 etapów: Compute Scalar, Stream Aggregate i dopiero Index Seek. W przypadku drugiego zapytania, które korzysta z indeksu, ale nie bezpośrednio, plan składa się z jednego etapu - Inde Scan W przypadku trzeciego zapytania, które korzysta z indeksu bezpośrednio, plan składa się z już z kkilku etapów które są mocno rozbijane na pomniejsze. Możemy zauważyć, że w przypadku zapytania, które korzysta z indeksu, ale nie bezpośrednio, czas wykonania zapytania jest dłuższy, ponieważ optymalizator musi wykonać dodatkowe operacje. W przypadku zapytania, które korzysta z indeksu bezpośrednio, czas wykonania zapytania jest krótszy, ponieważ optymalizator korzysta z indeksu, który jest posortowany i zawiera tylko interesujące nas wartości.

### Filtered Index (Indeks warunkowy)

> Filtered Index, czyli Indeks warunkowy, którego używamy w 4 eksperymencie jest to indeks, który zawiera tylko wiersze, które spełniają określone warunki. Indeks warunkowy jest tworzony na podstawie warunku, który jest określony w klauzuli WHERE.

**Schemat tabeli**

Tworzymy tabelę `Customer` z następującymi kolumnami:

- **CustomerID**
- **Name**
- **City**
- **Mail**

```sql
CREATE TABLE Customer (
  CustomerID INT NOT NULL PRIMARY KEY,
  Name NVARCHAR(50) NOT NULL,
  City NVARCHAR(30) NOT NULL,
  Mail NVARCHAR(50) NOT NULL
)
```

Wypełniamy tabelę przykładowymi danymi:

```sql
DECLARE @count INT = 0

WHILE @count < 100000
BEGIN
  INSERT INTO Customer (CustomerID, Name, City, Mail) VALUES (
    @count,
    CONCAT('Name', @count),
    CONCAT('City', @count % 5),
    CONCAT('Mail', @count)
  )
  SET @count = @count + 1
END
```

Dodajemy indeks warunkowy (filtered index) dla kolumny `City`, dla określonego miasta np. 'City3':

```sql
CREATE NONCLUSTERED INDEX Index_City
ON Customer (City, CustomerID, Name)
INCLUDE (Mail)
WHERE City = 'City3';
```

**Przykładowe zapytania**

Wykonujemy teraz przykładowe zapytania. Pierwsze, które korzystać będzie z indeksu warunkowego zwróci nam wszystkie dane o Customerach z miasta `City3`. Drugie, które nie będzie korzystać z indeksu warunkowego, zwróci nam wszystkie dane o Customerach z miasta `City1`. Zostanie wykonane porównanie działania zapytania z indeksem i bez niego. Przedstawione zostaną wyniki, plany wykonania oraz napisane zostaną wnioski.

```sql
SELECT *
FROM Customer
WHERE City = 'City3'
```

```sql
SELECT *
FROM Customer
WHERE City = 'City1'
```

**Wyniki**

| Zapytanie | Wynik                   |
| --------- | ----------------------- |
| 1         | ![](img/ex4/query8.png) |
| 2         | ![](img/ex4/query9.png) |

**Plany wykonania**

| Zapytanie | Plan wykonania              |
| --------- | --------------------------- |
| 1         | ![](img/ex4/query8plan.png) |
| 2         | ![](img/ex4/query9plan.png) |

**Komantarz**

> W tym eksperymencie, możemy zauważyć, że tam gdzie jest użyty indeks warunkowy, zapytanie wykonuje się szybciej i to o wiele. Korzystamy tam z `Index Seek`. W przypadku zapytania, które korzysta z indeksu warunkowego, plan wykonania zapytania jest prostszy, a w przypadku zapytania, które nie korzysta z indeksu warunkowego, plan wykonania zapytania jest bardziej skomplikowany. W przypadku zapytania, które korzysta z indeksu warunkowego, czas wykonania zapytania jest krótszy, ponieważ optymalizator korzysta z indeksu, który zawiera tylko interesujące nas wartości. W przypadku zapytania, które nie korzysta z indeksu warunkowego, czas wykonania zapytania jest dłuższy, ponieważ optymalizator musi przeszukać całą tabelę, wykonując scana tabeli, co można zaobserwować na planie wykonania zapytania, co jest przedstawione jako `Clustered Index Scan`.

### Kolumnowe

> Indeksy Kolumnowe to indeksy, które przechowują dane w kolumnach, a nie w wierszach. Są one tworzone na kolumnach, które są często używane w zapytaniach, które wykonują operacje agregujące, takie jak SUM, AVG, COUNT, MAX, MIN. Tych indeksów użyjemy w eksperymencie 5.

Tworzymy tabelę `Orders` z następującymi klumnami:

- **OrderID**
- **CustomerID**
- **ProductID**
- **Quantity**
- **OrderPrice**

```sql
CREATE TABLE Orders (
  OrderID INT NOT NULL PRIMARY KEY,
  CustomerID INT NOT NULL,
  ProductID INT NOT NULL,
  Quantity DECIMAL(10, 2) NOT NULL,
  OrderPrice DECIMAL(10, 2) NOT NULL
)
```

Wypełniamy tabelę przykładowymi danymi:

```sql
DECLARE @count INT = 0

WHILE @count < 100000
BEGIN
  INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderPrice) VALUES (
    @count,
    @count % 100,
    @count % 10,
    ROUND(RAND() * 20, 2),
    ROUND(RAND() * 100, 2)
  )
  SET @count = @count + 1
END
```

Tworzymy indeks kolumnowy na kolumnę `OrderPrice`:

```sql
CREATE NONCLUSTERED COLUMNSTORE INDEX Index_OrderPrice
ON Orders (OrderPrice);
```

**Przykładowe zapytania**

Wykonujemy teraz przykładowe zapytania. Pierwsze, które nie korzystać będzie z indeksu kolumnowego na `OrderPrice` zwróci nam ProductId oraz TotalSale, co jest sumą cen zamówień. Drugie, które będzie korzystać z indeksu kolumnowego zwróci nam to samo, jednak czas wykonania będzie znacznie szybszy, co zauważymy poniżej. Zostanie wykonane porównanie działania zapytania z indeksem i bez niego. Przedstawione zostaną wyniki, plany wykonania oraz napisane zostaną wnioski.

```sql
SELECT ProductID, SUM(OrderPrice) as TotalSale
FROM Orders
GROUP BY ProductID
```

**Wyniki**

| Zapytanie | Wynik                    |
| --------- | ------------------------ |
| 1         | ![](img/ex4/query10.png) |
| 2         | ![](img/ex4/query11.png) |

**Plany wykonania**

| Zapytanie | Plan wykonania               |
| --------- | ---------------------------- |
| 1         | ![](img/ex4/query10plan.png) |
| 2         | ![](img/ex4/query11plan.png) |

**Komantarz**

> W przypadku wykorzystania indeksu kolumnowego, zapytanie wykonuje się znacznie szybciej, ponieważ optymalizator korzysta z indeksu, który zawiera tylko interesujące nas wartości. W przypadku zapytania, które nie korzysta z indeksu kolumnowego, czas wykonania zapytania jest dłuższy, ponieważ optymalizator musi przeszukać całą tabelę, wykonując scana tabeli, co można zaobserwować na planie wykonania zapytania. Oba plany wyglądają bardzo podobnie, jednak możemy zauważyć, koszty jakie stanowiły ich operacje. W przypadku zapytania, które korzysta z indeksu kolumnowego, 91% kosztów stanowiło `ClusteredIndex Scan`, bo `Hash Match` był już znany. W przypadku zapytania, które nie korzysta z indeksu kolumnowego, koszty się podzieiłu prawie po 50 % pomiędzy `Hash Match` a `Clustered Index Scan`, co jest spowodowane nie znajomością `Hash Match` przez optymalizator.

### Próbnie

|         |     |     |     |
| ------- | --- | --- | --- |
| zadanie | pkt |     |     |
| 1       | 2   |     |     |
| 2       | 2   |     |     |
| 3       | 2   |     |     |
| 4       | 10  |     |     |
| razem   | 16  |     |     |
