from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.dictionary.models import Language, Book, Author
from app.common.db import get_db


router = APIRouter()


# получить всех авторов
@router.get("/Authors")
def read_root(session: Session = Depends(get_db)):
    #try:
        return [
            {
                "ФИО": x.fio,
                "Дата рождения": x.birthday,
                "Биография": x.biography
            } for x in session.query(Author)
        ]
    #except:
        #return {"status": "no data to return"}


# получить все языки
@router.get("/Languages")
def read_root(session: Session = Depends(get_db)):
    try:
        return [
            {
                "Язык": x.language,
            } for x in session.query(Language)
        ]
    except:
        return {"status": "no data to return"}


# получить все книги
@router.get("/Books")
def read_root(session: Session = Depends(get_db)):

    try:
        return [
            {
                "Книга": x.Book.name_book,
                "Дата издания": x.Book.year_book,
                "Язык": x.Language.language,
                "Автор": x.Author.fio,
                "Прочитана": x.Book.state_read
            } for x in session.query(Book, Language, Author).join(Language).join(Author)
        ]
    except:
        return {"status": "no data to return"}


# поиск книг данного автора (на любом языке или на конкретном, среди прочитанных, среди планируемых к прочтению)
# если значение id языка дефолтное (-1) то читай книги на всех языках, дефолтное значение для чтения = Не прочитана
@router.get("/authors_book")
def read_root(id: int, id_languages :int = -1, read: bool = False, session: Session = Depends(get_db)):
    books = session.query(Book, Language, Author).join(Language).join(Author).filter(Book.id_author == id, Book.state_read == read)
    if id_languages != -1:

        languag = session.query(Language).filter(Language.id == id_languages).first()

        if languag == None:
            return {"status": "no data to return"}

        books = books.filter(Book.id_language == id_languages)
    try:
        return [
            {
                "Книга": x.Book.name_book,
                "Дата издания": x.Book.year_book,
                "Язык": x.Language.language,
                "Автор": x.Author.fio,
                "Прочитана": x.Book.state_read
            } for x in books
        ]
    except:
        return {"status": "no data to return"}


# поиск всех прочитанных книг;
@router.get("/read_book")
def read_root(session: Session = Depends(get_db)):
    books = session.query(Book, Language, Author).join(Language).join(Author).filter(Book.state_read == True)

    try:
        return [
            {
                "Книга": x.Book.name_book,
                "Дата издания": x.Book.year_book,
                "Язык": x.Language.language,
                "Автор": x.Author.fio,
                "Прочитана": x.Book.state_read
            } for x in books
        ]
    except:
        return {"status": "no data to return"}


# поиск всех планируемых к прочтению книг (на любом языке или конкретном)
# если значение id языка дефолтное (-1) то читай книги на всех языках, дефолтное значение для чтения = Не прочитана
@router.get("/not_read_book")
def read_root(id_languages :int = -1, session: Session = Depends(get_db)):
    books = session.query(Book, Language, Author).join(Language).join(Author).filter(Book.state_read == False)

    if id_languages != -1:

        languag = session.query(Language).filter(Language.id == id_languages).first()

        if languag == None:
            return {"status": "no data to return"}

        books = books.filter(Book.id_language == id_languages)

    try:
        return [
            {
                "Книга": x.Book.name_book,
                "Дата издания": x.Book.year_book,
                "Язык": x.Language.language,
                "Автор": x.Author.fio,
                "Прочитана": x.Book.state_read
            } for x in books
        ]
    except:
        return {"status": "no data to return"}


#  поиск автора по имени
@router.get("/author")
def read_root(fio :str, session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.fio == fio)
    try:
        return [
            {
                "ФИО": x.fio,
                "Дата рождения": x.birthday,
                "Биография": x.biography
            } for x in author
        ]
    except:
        return {"status": "no data to return"}


# поиск книги по названию
@router.get("/book")
def read_root(name_book :str, session: Session = Depends(get_db)):
    book = session.query(Book, Language, Author).join(Language).join(Author).filter(Book.name_book == name_book)
    try:
        return [
            {
                "Книга": x.Book.name_book,
                "Дата издания": x.Book.year_book,
                "Язык": x.Language.language,
                "Автор": x.Author.fio,
                "Прочитана": x.Book.state_read
            } for x in book
        ]
    except:
        return {"status": "no data to return"}

# добавить ии изменить язык
# если язык есть изменить его имя, если нет то создать
# если id языка нет то мы его создаем иначе изменяем его поля
@router.post("/languages/add")
def read_item(id: int, language: str, session: Session = Depends(get_db)):
    languag = session.query(Language).filter(Language.id == id).first()
    if languag == None:
        new_language = Language(id = id, language = language)
        session.add(new_language)
    else:
        languag.language = language

    session.commit()

    return {"status": "OK"}


# создать или изменит автора
# по дефолту поэтому можно указывать не все параметры
# если id автора нет то мы его создаем иначе изменяем его поля
@router.post("/authors/add")
def read_item(id: int, fio="", birthday="", biography="", session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.id == id).first()
    if author == None:
        if fio!="":
            new_author = Author(id = id, fio = fio, birthday = birthday, biography = biography)
            session.add(new_author)
        else:
            return {"status": "no have all need data"}
    else:
        if fio!="":
            author.fio = fio
        if birthday!="":
            author.birthday = birthday
        if biography!="":
            author.biography = biography
    session.commit()

    return {"status": "OK"}


# создать или изменить книгу
# если книга есть то мы обязаны изменить её состояние (можем оставить на том же)
# если id книги нет то мы его создаем иначе изменяем его поля
@router.post("/books/add")
def read_item(id: int, state_read: bool, name_book="", year_book ="", id_language:int= -1, id_author:int = -1, session: Session = Depends(get_db)):
    book = session.query(Book).filter(Book.id == id).first()
    if book == None:
        language = session.query(Language).filter(Language.id == id_language)
        author = session.query(Author).filter(Author.id == id_author)

        if language.first() == None or author.first() == None:
            return {"status": "no have all need data"}

        if name_book!="":
            new_book = Book(
                id = id,
                name_book = name_book,
                year_book = year_book,
                id_language = id_language,
                id_author = id_author,
                state_read = state_read
            )
            session.add(new_book)
            session.commit()
            return {"status": "OK"}
        else:
            return {"status": "no have all need data"}
    else:
        if id_language != -1:
            language = session.query(Language).filter(Language.id == id_language)
            if language.first() == None:
                return {"status": "no have all need data"}
            book.id_language = id_language

        if id_author != -1:
            author = session.query(Author).filter(Author.id == id_author)
            if author.first() == None:
                return {"status": "no have all need data"}
            book.id_author = id_author

        if name_book != "":
            book.name_book = name_book
        if year_book !="":
            book.year_book = year_book

        book.state_read = state_read
        session.commit()
        return {"status": "OK"}


# удаление автора по id
@router.delete("/authors/delete")
def read_item(id: int,session: Session = Depends(get_db)):
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
