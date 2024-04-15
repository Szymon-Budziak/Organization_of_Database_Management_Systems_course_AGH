
# Indeksy,  optymalizator <br>Lab 6-7

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

(UWAGA    `GO 100` oznacza 100 krotne wykonanie polecenia. Jeżeli podejrzewasz, że Twój serwer może to zbyt przeciążyć, zacznij od GO 10, GO 20, GO 50 (w sumie już będzie 80))

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

```sql
--  ...
```




|         |     |     |     |
| ------- | --- | --- | --- |
| zadanie | pkt |     |     |
| 1       | 2   |     |     |
| 2       | 2   |     |     |
| 3       | 2   |     |     |
| 4       | 10  |     |     |
| razem   | 16  |     |     |
