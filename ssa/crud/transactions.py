from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete, select, insert

import datetime
import decimal 

from ssa import models, schemas 


async def get_transactions(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    query = await db.execute(
        select(models.Transaction).join(models.User).where(models.User.id == user_id)
        .order_by(models.Transaction.id.desc())
        .limit(limit)
        .offset(skip)
    )
    return query.scalars().all()


async def create_transaction(db: AsyncSession, user_db: models.User, amount: decimal.Decimal):
    #amount = decimal.Decimal(amount)
    trans_db = models.Transaction(
        datetime = datetime.datetime.now(),
        user_id = user_db.id,
        amount = amount,
    )
    db.add(transaction_db)
    
    user_db.amount -= amount
    await db.flush()
    return transaction_db

