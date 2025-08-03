import unittest
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_session

#create a test database in sqlite
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#override dependencies
async def override_get_session():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

#payloads for employee data and asset data
EMPLOYEE_DATA = {
    "firstname": "Aryan",
    "lastname": "Sinha",
    "gender": "Male",
    "phonenumber": "1234567890",
    "employeeemail": "aryan.sinha@gmail.com",
    "address": "111 City",
    "bloodgroup": "O+",
    "emergencycontactnumber": "9876543210"
}

ASSET_DATA = {
    "assetname": "Laptop",
    "assettype": "Electronics"
}

#class to test all routes
class TestAllRoutes(unittest.IsolatedAsyncioTestCase):
    #setup before each test case
    async def asyncSetUp(self):
        #create all tables before testing
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        #create transport route requests directly to fastapi
        transport = ASGITransport(app=app)
        #create client that will send requests back to test app
        self.client = AsyncClient(transport=transport, base_url="http://test")
    
    #teardown methord after each test case 
    async def asyncTearDown(self):
        #close client
        await self.client.aclose()

    #test all cases
    async def test_full_flow(self):
        #create employee
        res = await self.client.post("/employee/createemployee", json=EMPLOYEE_DATA)
        self.assertEqual(res.status_code, 200)
        emp = res.json()
        empid = emp["empid"]

        #get employee
        res = await self.client.get(f"/employee/getemployee/{empid}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["firstname"], EMPLOYEE_DATA["firstname"])

        #create asset
        res = await self.client.post("/asset/createasset", json=ASSET_DATA)
        self.assertEqual(res.status_code, 200)
        asset = res.json()
        assetid = asset["assetid"]

        #get all assets
        res = await self.client.get("/asset/getallasset")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.json()), 1)

        #map asset to employee
        res = await self.client.post("/mapping/assignassetmapping", json={
            "empid": empid,
            "assetid": assetid
        })
        self.assertEqual(res.status_code, 200)
        mappingid = res.json()["id"]

        #get mapped assets
        res = await self.client.get(f"/mapping/getallassets/{empid}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)

        #dashboard
        res = await self.client.get("/dashboard/getdetails")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["EmployeeList"][0]["assetcount"], 1)

        #delete mapping
        res = await self.client.delete(f"/mapping/removeassetmapping/{mappingid}")
        self.assertEqual(res.status_code, 200)

        #delete employee
        res = await self.client.delete(f"/employee/deleteemployee/{empid}")
        self.assertEqual(res.status_code, 200)

        #delete asset
        res = await self.client.delete(f"/asset/deleteasset/{assetid}")
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()