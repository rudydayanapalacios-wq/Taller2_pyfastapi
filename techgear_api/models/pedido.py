from pydantic import BaseModel


class Pedido(BaseModel):
    cliente: str
    producto_id: str
    cantidad: int
    total: float

class PedidooRespuesta(Pedido):
    id: str