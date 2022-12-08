from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.dictionary.models import Language, Book, Author
from app.common.db import get_db
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()



# получить всех авторов
@router.get("/Authors")
def read_root(session: Session = Depends(get_db)):
    try:
        return {"status": "", "result":[
            {
                "id": x.id,
                "FIO": x.fio,
                "Birthday": x.birthday,
                "Biography": x.biography
            } for x in session.query(Author)
        ]}
    except:
        return {"status": "no data to return", "result": []}


# получить все языки
@router.get("/Languages")
def read_root(session: Session = Depends(get_db)):
    try:
        return {"status": "", "result":[
            {
                "id": x.id,
                "Language": x.language,
            } for x in session.query(Language)
        ]}
    except:
        return {"status": "no data to return", "result": []}


# получить все книги
@router.get("/Books")
def read_root(session: Session = Depends(get_db)):

    try:
        return {"status": "", "result":[
            {
                "id": x.Book.id,
                "NameBook": x.Book.name_book,
                "YearBook": x.Book.year_book,
                "Language": x.Language.language,
                "Author": x.Author.fio,
                "StateRead": x.Book.state_read
            } for x in session.query(Book, Language, Author).join(Language).join(Author)
        ]}
    except:
        return {"status": "no data to return", "result": []}


# поиск книг данного автора (на любом языке или на конкретном, среди прочитанных, среди планируемых к прочтению)
# если значение id языка дефолтное (-1) то читай книги на всех языках, дефолтное значение для чтения = Не прочитана
@router.get("/authors_book")
def read_root(fio: str, language :str = "", read: bool = False, session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.fio == fio).first()
    books = session.query(Book, Language, Author).join(Language).join(Author).filter(Book.id_author == author.id, Book.state_read == read)
    if language != "":

        languag = session.query(Language).filter(Language.language == language).first()

        if languag == None:
            return {"status": "no data to return", "result": []}

        books = books.filter(Book.id_language == languag.id)
    try:
        return {"status": "", "result":[
            {
                "id": x.id,
                "NameBook": x.Book.name_book,
                "YearBook": x.Book.year_book,
                "Language": x.Language.language,
                "Author": x.Author.fio,
                "StateRead": x.Book.state_read
            } for x in books
        ]}
    except:
        return {"status": "no data to return", "result": []}


# поиск всех прочитанных книг;
@router.get("/read_book")
def read_root(session: Session = Depends(get_db)):
    books = session.query(Book, Language, Author).join(Language).join(Author).filter(Book.state_read == True)

    try:
        return {"status": "", "result":[
            {
                "NameBook": x.Book.name_book,
                "YearBook": x.Book.year_book,
                "Language": x.Language.language,
                "Author": x.Author.fio,
                "StateRead": x.Book.state_read
            } for x in books
        ]}
    except:
        return {"status": "no data to return", "result": []}


# поиск всех планируемых к прочтению книг (на любом языке или конкретном)
# если значение id языка дефолтное (-1) то читай книги на всех языках, дефолтное значение для чтения = Не прочитана
@router.get("/not_read_book")
def read_root(languages :str, session: Session = Depends(get_db)):
    books = session.query(Book, Language, Author).join(Language).join(Author).filter(Book.state_read == False)

    if languages != "":

        languag = session.query(Language).filter(Language.language == languages).first()

        if languag == None:
            return {"status": "no data to return", "result": []}

        books = books.filter(Book.id_language == languag.id)

    try:
        return {"status": "", "result":[
            {
                "NameBook": x.Book.name_book,
                "YearBook": x.Book.year_book,
                "Language": x.Language.language,
                "Author": x.Author.fio,
                "StateRead": x.Book.state_read
            } for x in books
        ]}
    except:
        return {"status": "no data to return", "result": []}


#  поиск автора по имени
@router.get("/author")
def read_root(id: int, session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.id == id)
    try:
        return {"status": "", "result":[
            {
                "id": x.id,
                "FIO": x.fio,
                "Birthday": x.birthday,
                "Biography": x.biography
            } for x in author
        ]}
    except:
        return {"status": "no data to return", "result": []}


# поиск книги по названию
@router.get("/book")
def read_root(id :int, session: Session = Depends(get_db)):
    book = session.query(Book, Language, Author).join(Language).join(Author).filter(Book.id == id)
    try:
        return {"status": "", "result":[
            {
                "id": x.Book.id,
                "NameBook": x.Book.name_book,
                "YearBook": x.Book.year_book,
                "Language": x.Language.language,
                "Author": x.Author.fio,
                "StateRead": x.Book.state_read
            } for x in book
        ]}
    except:
        return {"status": "no data to return", "result": []}


# добавить ии изменить язык
# если язык есть изменить его имя, если нет то создать
# если id языка нет то мы его создаем иначе изменяем его поля
@router.post("/languages/add")
def read_item(id: int, language: str,  session: Session = Depends(get_db)):
    languag = session.query(Language).filter(Language.id == id).first()
    if languag == None:
        new_language = Language(language = language)
        session.add(new_language)
    else:
        languag.language = language

    session.commit()

    return {"status": "OK"}


# создать или изменит автора
# по дефолту поэтому можно указывать не все параметры
# если id автора нет то мы его создаем иначе изменяем его поля
@router.post("/authors/mod")
def read_item(id: int, fio:str , birthday="", biography="", session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.id == id).first()
    if author == None:
        return {"status": "no have all need data"}
    else:
        author.fio = fio
        if birthday!="":
            author.birthday = birthday
        if biography!="":
            author.biography = biography
    session.commit()

    return {"status": "OK"}

@router.put("/authors/add")
def read_item(fio:str , birthday="", biography="", session: Session = Depends(get_db)):
    new_author = Author(fio = fio, birthday = birthday, biography = biography)
    session.add(new_author)
    session.commit()

    return {"status": "OK"}

# создать или изменить книгу
# если книга есть то мы обязаны изменить её состояние (можем оставить на том же)
# если id книги нет то мы его создаем иначе изменяем его поля
@router.post("/books/mod")
def read_item(id: int, state_read: bool, name_book, year_book ="", language:str= "", fio:str = "", session: Session = Depends(get_db)):
    book = session.query(Book).filter(Book.id == id).first()
    if book == None:
        return {"status": "no have all need data"}
    else:
        if language != "":
            languages = session.query(Language).filter(Language.language == language)
            if languages.first() == None:
                return {"status": "no have all need data"}
            book.id_language = languages.first().id

        if fio != "":
            author = session.query(Author).filter(Author.fio == fio)
            if author.first() == None:
                return {"status": "no have all need data"}
            book.id_author = author.first().id

        if name_book != "":
            book.name_book = name_book
        if year_book !="":
            book.year_book = year_book

        book.state_read = state_read
        session.commit()
        return {"status": "OK"}




@router.put("/books/add")
def read_item(state_read: bool, name_book, year_book ="", language:str= "", fio:str = "", session: Session = Depends(get_db)):
    languages = session.query(Language).filter(Language.language == language)
    author = session.query(Author).filter(Author.fio == fio)

    if languages.first() == None or author.first() == None:
        return {"status": "no have all need data"}

    new_book = Book(
                name_book = name_book,
                year_book = year_book,
                id_language = languages.first().id,
                id_author = author.first().id,
                state_read = state_read
        )
    session.add(new_book)
    session.commit()
    return {"status": "OK"}

# удаление автора по id
@router.delete("/authors/delete")
def read_item(id: int, session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.id == id).first()
    if author:
        session.delete(author)
        session.commit()
        return {"status": "OK"}
    else:
        return {"status": "no have all need data"}


#удаление книги по id
@router.delete("/book/delete")
def read_item(id: int, session: Session = Depends(get_db)):
    book = session.query(Book).filter(Book.id == id).first()
    if book:
        session.delete(book)
        session.commit()
        return {"status": "OK"}
    else:
        return {"status": "no have all need data"}
