from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# 임시 DB 역할
boards = []

# 데이터 모델
class Board(BaseModel):
    id: int
    title: str
    content: str

# 게시글 생성
@router.post("/boards", response_model=Board)
def create_board(board: Board):
    for b in boards:
        if b.id == board.id:
            raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")
    boards.append(board)
    return board

# 전체 게시글 조회
@router.get("/boards", response_model=List[Board])
def get_boards():
    return boards

# 특정 게시글 조회
@router.get("/boards/{board_id}", response_model=Board)
def get_board(board_id: int):
    for b in boards:
        if b.id == board_id:
            return b
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

# 게시글 수정
@router.put("/boards/{board_id}", response_model=Board)
def update_board(board_id: int, updated: Board):
    for i, b in enumerate(boards):
        if b.id == board_id:
            boards[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

# 게시글 삭제
@router.delete("/boards/{board_id}")
def delete_board(board_id: int):
    for i, b in enumerate(boards):
        if b.id == board_id:
            boards.pop(i)
            return {"message": "삭제 완료"}
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
