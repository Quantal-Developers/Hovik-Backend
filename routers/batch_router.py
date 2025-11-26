from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.batch_service import get_row_by_lot_number

router = APIRouter(tags=["Batch Lookup"])

@router.get("/batch")
def batch_lookup(lot_number):
    try:
        result = get_row_by_lot_number(lot_number)

        if "error" in result:
            return JSONResponse(status_code=404, content=result)

        return result

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "details": str(e)}
        )
