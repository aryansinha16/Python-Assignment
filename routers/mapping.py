from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from schema import EmployeeAssetMapping, EmployeeAssetMappingCreate, EmployeeAssetMappingRead, AssetDetailsRead, AssetDetails

#start the router
router = APIRouter()

#route to assign an asset to an employee (mapping)
@router.post("/assignassetmapping", response_model=EmployeeAssetMappingRead)
async def assign_multiple_assets(mappings: list[EmployeeAssetMappingCreate] = Body(...), session: AsyncSession = Depends(get_session)):
    new_mappings = []
    #a loop methord to map multiple employees to assets
    for mapping in mappings:
        new_mapping = EmployeeAssetMapping(**mapping.model_dump())
        session.add(new_mapping)
        new_mappings.append(new_mapping)
    await session.commit()
    for new_mapping in new_mappings:
        await session.refresh(new_mapping)
    return new_mappings

#route to get assets assigned to specific employee
@router.get("/getallassets/{employeeid}", response_model=list[AssetDetailsRead])
async def get_assets_employee(employeeid: int, session: AsyncSession = Depends(get_session)):
    #get all mapping for given employee
    result = await session.execute(select(EmployeeAssetMapping).where(EmployeeAssetMapping.empid == employeeid))
    mappings = result.scalars().all()
    #extract asset id from the mapping result
    asset_ids = [m.assetid for m in mappings]
    #query and return asset details for retrieved asset id
    result = await session.execute(select(AssetDetails).where(AssetDetails.assetid.in_(asset_ids)))
    return result.scalars().all()

#route to delete asset map by mapping id
@router.delete("/removeassetmapping/{mappingid}")
async def remove_asset_map(mappingid: int, session: AsyncSession = Depends(get_session)):
    #retrieve map by id
    mapp = await session.get(EmployeeAssetMapping, mappingid)
    if not mapp:
        raise HTTPException(status_code=404, detail="Map not found")
    #delete and commit mapping
    await session.delete(mapp)
    await session.commit()
    return{"message":"Mapping Removed"}