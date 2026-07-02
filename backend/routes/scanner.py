from fastapi import APIRouter
from controllers.scanner import handle_single_scan, handle_range_scan

scan_router = APIRouter(
    prefix="/scan",
    tags=["Scanner"]
)

@scan_router.get('/single')
async def run_scan(ip: str, port: int):
    return await handle_single_scan(ip, port)

@scan_router.get('/range')
async def run_scan_range(ip: str, start_port: int, end_port: int):
    return await handle_range_scan(ip, start_port, end_port)