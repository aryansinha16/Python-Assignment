from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from schema import AssetDetails, AssetDetailsCreate, AssetDetailsRead

#starting the router
router = APIRouter()

#route to create new asset
@router.post("/createasset", response_model=list[AssetDetailsRead])
async def create_asset(assets: list[AssetDetailsCreate] = Body(...), session: AsyncSession = Depends(get_session)):
    new_assets = []
    #a loop methord  to add multiple asset details
    for asset_data in assets:
        asset = AssetDetails(**asset_data.model_dump())
        session.add(asset)
        new_assets.append(asset)
    await session.commit()
    for asset in new_assets:
        await session.refresh(asset)
    return new_assets

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