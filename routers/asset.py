from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from schema import AssetDetails, AssetDetailsCreate, AssetDetailsRead

#starting the router
router = APIRouter()

#route to create new asset
@router.post("/createasset", response_model=AssetDetailsRead)
async def create_asset(asset: AssetDetailsCreate, session: AsyncSession = Depends(get_session)):
    #create new assetdetails as an object
    new_asset = AssetDetails(**asset.model_dump())
    #add new asset to the session and commit to database
    session.add(new_asset)
    await session.commit()
    await session.refresh(new_asset) #refresh to get the data
    return new_asset #return the new asset

#route to edit existing asset details
@router.patch("/editasset/{assetid}", response_model=AssetDetailsRead)
async def edit_asset(assetid: int, asset: AssetDetailsCreate, session: AsyncSession = Depends(get_session)):
    #retrieve asset record by id
    asst = await session.get(AssetDetails, assetid)
    if not asst:
        raise HTTPException(status_code=404, detail="Asset not found")
    #update each field with new values
    for key, value in asset.model_dump().items():
        setattr(asst, key, value)
    #save changes and refresh database and return the updated asset details
    await session.commit()
    await session.refresh(asst)
    return asst

#route to get all asset details
@router.get("/getallasset", response_model=list[AssetDetailsRead])
async def getall_asset(session: AsyncSession = Depends(get_session)):
    #execute a select query to fetch all asset details from the database
    result = await session.execute(select(AssetDetails))
    return result.scalars().all()

#route to delete existing asset details
@router.delete("/deleteasset/{assetid}")
async def delete_asset(assetid: int, session: AsyncSession = Depends(get_session)):
    #retrieve asset detail by id
    asst = await session.get(AssetDetails, assetid)
    if not asst:
        raise HTTPException(status_code=404, detail="Asset not found")
    #delete asset detail and save
    await session.delete(asst)
    await session.commit()
    return{"message":"Deleted"}