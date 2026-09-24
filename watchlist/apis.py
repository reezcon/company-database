from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from engine.engine import get_db
from watchlist.service import WatchlistService as service
from watchlist.schemas import Watchlist, WatchlistUpdate, WatchlistCreate, WatchlistOut

router = APIRouter(prefix="/watchlists", tags = ["Watchlists"])
session = Depends(get_db)

# @router.get("", response_model=WatchlistOut)
# async def read_watchlists(db: Session = session):
#     try: 
#         return service(db).get_watchlists
#     except Exception as e: 
#         print (e)
#         return str(e)
# READ all roles
@router.get("", response_model=list[WatchlistOut])
async def read_watchlist(db: Session = session):
    return service(db).get_watchlists()

@router.get("/{role_id}")
async def read_watchlist(watchlist_id: int, db:Session = session):
    watchlist = service(db).get_watchlist(watchlist_id)
    if watchlist is None: 
        raise HTTPException(status_code=404, detail = "Watchlist not found")
    return watchlist

@router.post("", response_model=WatchlistOut)
async def create_watchlist(payload: WatchlistCreate, db: Session=session):
    try: 
        return service(db).create_watchlist(payload)
    except ValueError as e: 
        raise HTTPException(status_code= 409, detail = str(e))
    except SQLAlchemyError: 
        raise HTTPException(status_code=500, detail="Database error while creating watchlist")

@router.put("/{watchlist_id}", response_model=WatchlistOut)
async def update_watchlist(watchlist_id: int, payload: WatchlistCreate, db:Session=session):
    try: 
        watchlist = service(db).update_watchlist(watchlist_id, payload)
    except ValueError as e: 
        raise HTTPException (status_code=409, detail = str(e))
    except SQLAlchemyError: 
        raise HTTPException(status_code=500, detail = "Database error while updating watchlist")
    if watchlist is None:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    return watchlist

@router.delete("/{watchlist_id}")
async def delete_watchlist(watchlist_id: int, db: Session = session):
    watchlist = service(db).delete_watchlist(watchlist_id)
    if watchlist is None: 
        raise HTTPException(status_code=404, detail = "Watchlist not found")
    return {"detail": f"Watchlist {watchlist_id} deleted"}