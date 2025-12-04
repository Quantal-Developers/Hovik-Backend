from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.batch_service import get_row_by_lot_number

router = APIRouter(tags=["Batch Lookup"])

from pydantic import BaseModel

class BatchLookupRequest(BaseModel):
    lot_number: str

@router.post("/batch")
def batch_lookup(req:BatchLookupRequest):
    try:
        result = get_row_by_lot_number(req.lot_number)

        if "error" in result:
            return JSONResponse(status_code=404, content=result)

        return result

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "details": str(e)}
        )
