import json
from fastapi import HTTPException
# Импортируем из папки utils БЕЗ слова backend
from utils.scanner import scan_port, scan_port_range
from utils.database import pool

async def handle_single_scan(ip: str, port: int):
    is_open = await scan_port(ip, port)
    return {"ip": ip, "port": port, "status": "open" if is_open else "closed"}

async def handle_range_scan(ip: str, start_port: int, end_port: int):
    if start_port > end_port:
        raise HTTPException(status_code=400, detail="Start port cannot be greater than end port")

    open_ports = await scan_port_range(ip, start_port, end_port)
    
    ports_json = json.dumps(open_ports)
    await pool.execute(
        """
        INSERT INTO scan_history (ip, start_port, end_port, open_ports)
        VALUES ($1, $2, $3, $4)
        """,
        ip, start_port, end_port, ports_json
    )
    
    return {
        "ip": ip,
        "open_ports": open_ports
    }