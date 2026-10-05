from pydantic import BaseModel

class NetworkEvent(BaseModel):
    source_ip: str
    destination_port : int
    packet_count: int

