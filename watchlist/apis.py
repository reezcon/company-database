from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from engine.engine import get_db
from watchlist.service import WatchlistService as service
from watchlist.schemas import Watchlist, WatchlistUpdate, WatchlistCreate, WatchlistOut

from auth.apis import require_admin_or_manager, require_self_or_admin_or_manager

router = APIRouter(prefix="/watchlists", tags = ["Watchlists"])
session = Depends(get_db)

# READ all roles
@router.get("", response_model=list[WatchlistOut])
async def read_watchlists(db: Session = session,
                          _: Watchlist = Depends(require_admin_or_manager)):
    return service(db).get_watchlists()

@router.get("/{watchlist_id}")
async def read_watchlist(watchlist_id: int, db:Session = session,
                         _: Watchlist = Depends(require_self_or_admin_or_manager)):
    watchlist = service(db).get_watchlist(watchlist_id)
    if watchlist is None: 
        raise HTTPException(status_code=404, detail = "Watchlist not found")
    return watchlist

@router.post("", response_model=WatchlistOut)
async def create_watchlist(payload: WatchlistCreate, db: Session=session,
                           _: Watchlist = Depends(require_admin_or_manager)):
    try: 
        return service(db).create_watchlist(payload)
    except ValueError as e: 
        raise HTTPException(status_code= 409, detail = str(e))
    except SQLAlchemyError: 
        raise HTTPException(status_code=500, detail="Database error while creating watchlist")

@router.put("/{watchlist_id}", response_model=WatchlistOut)
async def update_watchlist(watchlist_id: int, payload: WatchlistUpdate, db:Session=session,
                           _: Watchlist = Depends(require_admin_or_manager)):
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
async def delete_watchlist(watchlist_id: int, db: Session = session,
                           _: Watchlist = Depends(require_admin_or_manager)):
    watchlist = service(db).delete_watchlist(watchlist_id)
    if watchlist is None: 
        raise HTTPException(status_code=404, detail = "Watchlist not found")
    return {"detail": f"Watchlist {watchlist_id} deleted"}