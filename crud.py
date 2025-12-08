from sqlalchemy.orm import Session
import models, schemas

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    return db.query(models.Book).all()

def loan_book(db: Session, book_id: int, user: str):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book or not book.is_available:
        return None
    book.is_available = False
    loan = models.Loan(book_id=book_id, user=user)
    db.add(loan)
    db.commit()
    return loan

def return_book(db: Session, book_id: int):
    # 1. Kitobni topish
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        # Kitob bazada mavjud emas
        return {"error": "도서를 찾을 수 없습니다."} # Kitob topilmadi.

    # 2. Kitobning qarzga olinganligini tekshirish (is_available == False bo'lishi kerak)
    if book.is_available:
        return {"error": "이미 반납되었거나, 대출 기록이 없는 도서입니다."} # Allaqaсhon qaytarilgan yoki qarzga olinmagan.

    # 3. Faol (qaytarilmagan) Loan yozuvini topish
    active_loan = db.query(models.Loan).filter(
        models.Loan.book_id == book_id,
        models.Loan.returned == False
    ).first()

    if not active_loan:
        # Kitob 'available' emas, lekin faol Loan yozuvi topilmadi. Book holatini tiklaymiz.
        book.is_available = True
        db.commit()
        return {"error": "미반납 대출 기록을 찾을 수 없습니다."} # Qaytarilmagan qarzga olish yozuvi topilmadi.

    # --- 반납 처리 (Qaytarish amali) ---

    # 4. Loan yozuvini yangilash: Qaytarildi deb belgilash
    active_loan.returned = True
    
    # 5. Book yozuvini yangilash: Mavjud (Available) deb belgilash
    book.is_available = True 

    # 6. O'zgarishlarni bazaga kiritish
    db.commit()
    db.refresh(book)

    return {"message": "반납 완료", "book_id": book_id}