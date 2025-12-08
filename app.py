import streamlit as st
import requests

API_URL = "http://localhost:8000/library"

st.title("📚 도서관 대여 시스템 – Streamlit UI")

# -----------------------
# 도서 등록
# -----------------------
st.header("📘 도서 등록")

book_title = st.text_input("도서명")
author = st.text_input("저자")
year = st.number_input("출판년도", step=1)



if st.button("등록하기"):
    data = {"title": book_title, "author": author, "year": year}
    r = requests.post(f"{API_URL}/books", json=data)
    if r.status_code == 200:
        st.success("도서가 성공적으로 등록되었습니다!")
    else:
        st.error("도서 등록에 실패했습니다.")

st.divider()

# -----------------------
# 도서 목록 조회
# -----------------------
st.header("📚 도서 목록")

res = requests.get(f"{API_URL}/books")
if res.status_code == 200:
    books = res.json()
    for b in books:
        st.subheader(f"{b.get('id')}. {b.get('title')}")
        st.write(f"✍️ 저자: {b.get('author')}")

        # borrowed 필드가 없을 경우 False로 처리
        borrowed = b.get("borrowed", False)
        st.write(f"📌 상태: {'대여 중' if borrowed else '보유 중'}")

        st.write("---")
else:
    st.error("도서 목록을 불러올 수 없습니다.")

st.divider()


# -----------------------
# 📖 도서 대여
# -----------------------
st.header("📖 도서 대여")

borrow_id = st.number_input("대여할 도서 ID 입력", step=1)
borrow_user = st.text_input("대여자 이름 입력 (user)")

if st.button("📘 대여하기"):
    if borrow_user.strip() == "":
        st.error("대여자 이름을 입력해주세요!")
    else:
        r = requests.post(f"http://localhost:8000/library/loan/{borrow_id}?user={borrow_user}")
        if r.status_code == 200:
            st.success("📚 도서가 성공적으로 대여되었습니다!")
        else:
            st.error("❌ 도서 대여에 실패했습니다!")


# -----------------------
# 도서 반납
# -----------------------
st.header("↩️ 도서 반납")

return_id = st.number_input("반납할 도서 ID 입력", step=1)

if st.button("반납하기"):
    r = requests.post(f"{API_URL}/return/{return_id}")
    if r.status_code == 200:
        st.success("도서를 성공적으로 반납했습니다!")
    else:
        st.error("도서 반납에 실패했습니다.")
