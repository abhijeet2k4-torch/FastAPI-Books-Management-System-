from fastapi import HTTPException, status, APIRouter
from typing import List
from src.authors.schemas import AuthorModel, PatchAuthorModel
from src.authors.author_data import authors

router = APIRouter()

@router.get('/', response_model = List[AuthorModel])
async def get_all_authors():
    if not authors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No authors found")
    return authors

@router.get('/{author_id}', response_model=AuthorModel, status_code=status.HTTP_200_OK)
async def get_author_by_id(author_id:int):
    for author in authors:
        if author['id'] == author_id:
            return author
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

@router.post('/',response_model=AuthorModel, status_code=status.HTTP_201_CREATED)
async def create_author(author_data: AuthorModel):
    new_author = author_data.model_dump()
    authors.append(new_author)
    return new_author

@router.patch('/{author_id}', response_model=PatchAuthorModel, status_code=status.HTTP_200_OK)
async def update_author(author_id:int, author_update_data: PatchAuthorModel):
    for author  in authors:
        if author['id'] == author_id:
            author['name'] = author_update_data.name
            author['email'] = author_update_data.email
            return author
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

@router.delete('/{author_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id:int):
    for author in authors:
        if author['id'] == author_id:
            authors.remove(author)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")