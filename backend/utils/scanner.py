import asyncio

async def scan_port(ip: str, port: int) -> bool:
   try:
      reader, writer = await asyncio.wait_for(
         asyncio.open_connection(ip, port),
         timeout=1.0
      )
      writer.close()
      await writer.wait_closed()
      
      return True
   except Exception:
      return False
   
# Сканирование диапозона портов
async def scan_port_range(ip: str, start_port: int, end_port: int) -> list[int]:
   tasks = []
   for port in range(start_port, end_port + 1):
      tasks.append(scan_port(ip, port))
   results = await asyncio.gather(*tasks)
   
   open_ports = []
   for port, is_open in zip(range(start_port, end_port + 1), results):
      if is_open:
         open_ports.append(port)
   return open_ports
   
   
   
