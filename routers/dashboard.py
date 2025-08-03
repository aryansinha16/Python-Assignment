from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from schema import DashboardView, DashboardViewResponse, EmployeeDetails, EmployeeAssetMapping
from collections import Counter

#start the router
router = APIRouter()

#route to get dashboard view of all employees and their asset count
@router.get("/getdetails", response_model=DashboardViewResponse)
async def view_dashboard(session: AsyncSession = Depends(get_session)):
    #fetch all employee records from database
    emp_result = await session.execute(select(EmployeeDetails))
    employees = emp_result.scalars().all()
    #fetch all employee asset maps from database
    map_result = await session.execute(select(EmployeeAssetMapping))
    mapping = map_result.scalars().all()
    #count number of assets assigned to each employee by their employee id
    asset_count = Counter(m.empid for m in mapping)

    #prepare response list with employee details and their asset count
    output = []
    for emp in employees:
        output.append(DashboardView(
            empid = emp.empid,
            firstname = emp.firstname,
            lastname = emp.lastname,
            gender = emp.gender,
            phonenumber = emp.phonenumber,
            employeeemail = emp.employeeemail,
            address = emp.address,
            bloodgroup = emp.bloodgroup,
            emergencycontactnumber = emp.emergencycontactnumber,
            assetcount = asset_count.get(emp.empid, 0) #default to 0 if no assets
        ))
    #return structured response
    return{"EmployeeList": output}  