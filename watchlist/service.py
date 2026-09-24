from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from watchlist.schemas import Watchlist, WatchlistCreate, WatchlistUpdate

class WatchlistService:
    def __init__(self, db:Session):
        self.db = db

    def get_watchlists(self):
        return self.db.query(Watchlist).all()

    def get_watchlist(self, watchlist_id: int):
        return self.db.get(Watchlist, watchlist_id)

    def _check_duplicates(self, watchlist_name: str = None):
        if watchlist_name is None:
            return 
        query = self.db.query(Watchlist).filter(Watchlist.watchlist_name == watchlist_name)
        if query.first() is not None:
            raise ValueError("That watchlist already exists")

    def create_watchlist(self, payload: WatchlistCreate):
        self._check_duplicates(watchlist_name=payload.watchlist_name)
        data = payload.model_dump()
        watchlist = Watchlist(**data)
        try: 
            self.db.add(watchlist)
            self.db.commit()
            self.db.refresh(watchlist)
            return watchlist 
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update_watchlist(self, watchlist_id, payload: WatchlistUpdate):
        watchlist = self.db.get(Watchlist, watchlist_id)
        if watchlist is None: 
            return None
        updates = payload.model_dump(exclude_unset=True)

        self._check_duplicates(watchlist_name=updates.get("watchlist_name"))

        for field, value in updates.items():
            setattr(watchlist, field, value)
            try: 
                self.db.commit()
                self.db.refresh(watchlist)
                return watchlist
            except SQLAlchemyError:
                self.db.rollback()
                raise

    def delete_watchlist(self, watchlist_id: int):
        watchlist = self.db.get(Watchlist, watchlist_id)
        if watchlist is None: 
            return None
        try: 
            self.db.delete(watchlist)
            self.db.commit()
            return watchlist
        except SQLAlchemyError:
            self.db.rollback()
            raise