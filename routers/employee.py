from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from schema import EmployeeDetails, EmployeeDetailsCreate, EmployeeDetailsRead

#starting the router
router = APIRouter()

#route to create new employee
@router.post("/createemployee", response_model= list[EmployeeDetailsRead])
async def create_employlee(employees: list[EmployeeDetailsCreate] = Body(...), session: AsyncSession = Depends(get_session)):
    new_employee = []
    #a loop methord to add multiple employee details
    for employee_data in employees:
        employee = EmployeeDetails(**employee_data.model_dump())
        session.add(employee)
        new_employee.append(employee)
    await session.commit()
    for employee in new_employee:
        await session.refresh(employee)
    return new_employee

#route to edit existing employee details
@router.patch("/editemployee/{employeeid}", response_model=EmployeeDetailsRead)
async def edit_employee(employeeid: int, employee: EmployeeDetailsCreate, session: AsyncSession = Depends(get_session)):
    #retrieve employee record by id
    emp = await session.get(EmployeeDetails, employeeid)
    if not emp:
        raise HTTPException(status_code= 404, detail="Employee not found")
    #update each field with new values
    for key, value in employee.model_dump().items():
        setattr(emp, key, value)
    #save changes and refresh database and return the update employee details 
    await session.commit()
    await session.refresh(emp)
    return emp

#route to delete existing employee details
@router.delete("/deleteemployee/{employeeid}")
async def delete_employee(employeeid: int, session: AsyncSession = Depends(get_session)):
    #retrieve employee detail by id
    emp = await session.get(EmployeeDetails, employeeid)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    #delete employee details and save
    await session.delete(emp)
    await session.commit()
    return{"message":"Deleted"}

#route to get employee detail by id
@router.get("/getemployee/{employeeid}", response_model=EmployeeDetailsRead)
async def get_employee(employeeid: int, session: AsyncSession = Depends(get_session)):
    #retrieve employee detail by id
    emp = await session.get(EmployeeDetails, employeeid)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return emp #return employee detail

#route to get all employee details
@router.get("/getallemployee", response_model=list[EmployeeDetailsRead])
async def get_all(session: AsyncSession = Depends(get_session)):
    #execute a select query to fetch all employee details from the database
    result = await session.execute(select(EmployeeDetails))
    return result.scalars().all()