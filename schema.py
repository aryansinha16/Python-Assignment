from sqlmodel import SQLModel, Field
from sqlalchemy import Integer, Column

#entire Schema for our employee details
class EmployeeDetails(SQLModel, table = True):
    empid: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    firstname: str
    lastname: str
    gender: str
    phonenumber: str
    employeeemail: str
    address: str
    bloodgroup: str
    emergencycontactnumber: str

#schema for inputs of the employee details
class EmployeeDetailsCreate(SQLModel):
    firstname: str
    lastname: str
    gender: str
    phonenumber: str
    employeeemail: str
    address: str
    bloodgroup: str
    emergencycontactnumber: str

#output schema for the employee details
class EmployeeDetailsRead(SQLModel):
    empid: int
    firstname: str
    lastname: str
    gender: str
    phonenumber: str
    employeeemail: str
    address: str
    bloodgroup: str
    emergencycontactnumber: str

#entire Schema for asset details
class AssetDetails(SQLModel, table = True):
    assetid: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    assetname: str
    assettype: str

#input schema for asset details
class AssetDetailsCreate(SQLModel):
    assetname: str
    assettype: str

#output schema for asset details
class AssetDetailsRead(SQLModel):
    assetid: int
    assetname: str
    assettype: str

#entire schema for employee asset mapping
class EmployeeAssetMapping(SQLModel, table = True):
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    empid: int = Field(foreign_key="employeedetails.empid")
    assetid: int = Field(foreign_key="assetdetails.assetid")

#input schema for the employee asset mapping
class EmployeeAssetMappingCreate(SQLModel):
    empid: int
    assetid: int

#output schema for the employee asset mapping
class EmployeeAssetMappingRead(EmployeeAssetMappingCreate):
    id: int

#schema for the dashboard
class DashboardView(SQLModel):
    empid: int
    firstname: str
    lastname: str
    gender: str
    phonenumber: str
    employeeemail: str
    address: str
    bloodgroup: str
    emergencycontactnumber: str
    assetcount: int

#list the dashboard view
class DashboardViewResponse(SQLModel):
    EmployeeList: list[DashboardView]