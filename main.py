# --------------------------------------------------------------------------------------------------------------------------------------- Entrega 1

from __future__ import annotations
from typing import List, Dict, Optional
from datetime import datetime
import uuid

# --------------------------------------------------------------------------------------------------------------------------------------- Class Mensaje
class Mensaje:
  """
  Representa un mensaje de correo electrónico.
  Cada mensaje tiene un remitente, una lista de destinatarios, asunto, cuerpo, un identificador único y una marca de tiempo.
  Permite marcar/desmarcar flags (por ejemplo, leído, importante).
  """
  def __init__(self, remitente: str, destinatarios: List[str], asunto: str, cuerpo: str):
    """
    Inicializa un nuevo mensaje con los datos proporcionados.
    El id se genera automáticamente y la fecha es la actual (UTC).
    """
    self._id = str(uuid.uuid4()) # Identificador único del mensaje
    self._remitente = remitente
    self._destinatarios = list(destinatarios)
    self._asunto = asunto
    self._cuerpo = cuerpo
    self._timestamp = datetime.utcnow()
    self._flags = set()

  #--------------------------------------------------------------------------------------------------------------------------------------- Propiedades de solo lectura
  """
  Propiedades de solo lectura para los atributos del mensaje.
  Permiten acceder a los datos pero no modificarlos directamente.
  """
  @property
  def id(self) -> str:
    """Devuelve el identificador único del mensaje."""
    return self._id

  @property
  def remitente(self) -> str:
    """Devuelve el email del remitente."""
    return self._remitente

  @property
  def destinatarios(self) -> List[str]:
    """Devuelve la lista de destinatarios."""
    return list(self._destinatarios)

  @property
  def asunto(self) -> str:
    """Devuelve el asunto del mensaje."""
    return self._asunto

  @property
  def cuerpo(self) -> str:
    """Devuelve el cuerpo del mensaje."""
    return self._cuerpo

  @property
  def timestamp(self) -> datetime:
    """Devuelve la fecha y hora de creación del mensaje."""
    return self._timestamp

  # Métodos para banderas (flags)
  def marcar(self, flag: str) -> None:
    """
    Marca el mensaje con una bandera (por ejemplo, 'leído', 'importante').
    """
    self._flags.add(flag)

  def desmarcar(self, flag: str) -> None:
    """
    Elimina una bandera del mensaje.
    """
    self._flags.discard(flag)

  def tiene_flag(self, flag: str) -> bool:
    """
    Verifica si el mensaje tiene una bandera específica.
    """
    return flag in self._flags

  def __repr__(self) -> str:
    """Representación legible del mensaje para depuración."""
    return f"<Mensaje {self._id[:8]} {self._asunto!r} from={self._remitente}>"

# --------------------------------------------------------------------------------------------------------------------------------------- Carpeta
class Carpeta:
  """
  Representa una carpeta de mensajes (por ejemplo, INBOX, SENT, TRASH).
  Puede contener mensajes.
  """
  def __init__(self, nombre: str):
    """
    Inicializa la carpeta con un nombre y una lista vacía de mensajes.
    """
    self._nombre = nombre
    self._mensajes: List[Mensaje | Carpeta] = []

  @property
  def nombre(self) -> str:
    """Devuelve el nombre de la carpeta."""
    return self._nombre

  def agregar(self, mensaje: Mensaje) -> None:
    """
    Agrega un mensaje a la carpeta.
    """
    self._mensajes.append(mensaje)

  def eliminar(self, mensaje_id: str) -> bool:
    """
    Elimina un mensaje por su id. Devuelve True si se eliminó, False si no se encontró.
    """
    for i, m in enumerate(self._mensajes):
      if m.id == mensaje_id:
        del self._mensajes[i]
        return True
    return False

  def listar(self) -> List[Mensaje]:
    """
    Devuelve una lista de todos los mensajes en la carpeta.
    """
    return list(self._mensajes)

  def buscar_por_asunto(self, clave: str) -> List[Mensaje]:
    """
    Busca mensajes cuyo asunto contenga la clave (no sensible a mayúsculas).
    """
    clave_low = clave.lower()
    return [m for m in self._mensajes if clave_low in m.asunto.lower()]

  def __repr__(self) -> str:
    """Representación legible de la carpeta para depuración."""
    return f"<Carpeta {self._nombre} ({len(self._mensajes)} mensajes)>"

