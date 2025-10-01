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

# --------------------------------------------------------------------------------------------------------------------------------------- class Usuario
class Usuario:
  """
  Representa un usuario del sistema de correo.
  Cada usuario tiene un email, un nombre y varias carpetas (INBOX, SENT, TRASH, etc).
  """
  def __init__(self, email: str, nombre: str):
    """
    Inicializa el usuario con su email y nombre.
    Crea las carpetas básicas por defecto.
    """
    self._email = email.lower()
    self._nombre = nombre
    # Carpetas por nombre (Inbox, Enviados, Papelera, personalizado...)
    self._carpetas: Dict[str, Carpeta] = {
      'INBOX': Carpeta('INBOX'),
      'SENT': Carpeta('SENT'),
      'TRASH': Carpeta('TRASH')
    }

  @property
  def email(self) -> str:
    """Devuelve el email del usuario."""
    return self._email

  @property
  def nombre(self) -> str:
    """Devuelve el nombre del usuario."""
    return self._nombre

  def crear_carpeta(self, nombre: str) -> None:
    """
    Crea una nueva carpeta personalizada para el usuario.
    Lanza un error si ya existe una carpeta con ese nombre.
    """
    key = nombre.upper()
    if key in self._carpetas:
      raise ValueError(f"La carpeta '{nombre}' ya existe")
    self._carpetas[key] = Carpeta(nombre)

  def listar_carpetas(self) -> List[str]:
    """
    Devuelve la lista de nombres de carpetas del usuario.
    """
    return list(self._carpetas.keys())

  def obtener_carpeta(self, nombre: str) -> Carpeta:
    """
    Devuelve la carpeta con el nombre dado.
    Lanza un error si no existe.
    """
    key = nombre.upper()
    if key not in self._carpetas:
      raise KeyError(f"Carpeta '{nombre}' no encontrada")
    return self._carpetas[key]

  # Interfaz para enviar: crea Mensaje y delega al servidor
  def enviar(self, server: 'ServidorCorreo', destinatarios: List[str], asunto: str, cuerpo: str) -> Mensaje:
    """
    Envía un mensaje a través del servidor.
    Crea el mensaje, lo envía y guarda una copia en la carpeta SENT.
    """
    mensaje = Mensaje(remitente=self._email, destinatarios=destinatarios, asunto=asunto, cuerpo=cuerpo)
    ok = server.enviar_email(mensaje)
    if ok:
      # Guardar copia en carpeta SENT
      self.obtener_carpeta('SENT').agregar(mensaje)
      return mensaje
    else:
      raise RuntimeError('Fallo al enviar el mensaje')

  def recibir(self, mensaje: Mensaje) -> None:
    """
    Recibe un mensaje y lo coloca en la carpeta INBOX.
    """
    self.obtener_carpeta('INBOX').agregar(mensaje)

  def __repr__(self) -> str:
    """Representación legible del usuario para depuración."""
    return f"<Usuario {self._email} ({self._nombre})>"

# --------------------------------------------------------------------------------------------------------------------------------------- Class Servidor
class ServidorCorreo:
  """
  Representa el servidor de correo.
  Gestiona los usuarios y la entrega de mensajes entre ellos.
  """
  def __init__(self):
    """
    Inicializa el servidor con un diccionario vacío de usuarios.
    """
    self._usuarios: Dict[str, Usuario] = {}

  def registrar_usuario(self, email: str, nombre: str) -> Usuario:
    """
    Registra un nuevo usuario en el servidor.
    Lanza un error si el usuario ya existe.
    """
    key = email.lower()
    if key in self._usuarios:
      raise ValueError('Usuario ya registrado')
    usuario = Usuario(email=key, nombre=nombre)
    self._usuarios[key] = usuario
    return usuario

  def obtener_usuario(self, email: str) -> Optional[Usuario]:
    """
    Devuelve el usuario con el email dado, o None si no existe.
    """
    return self._usuarios.get(email.lower())

  # Envio sincrono: entrega inmediata a los destinatarios existentes
  def enviar_email(self, mensaje: Mensaje) -> bool:
    """
    Entrega el mensaje a todos los destinatarios registrados en el servidor.
    Devuelve True si al menos uno lo recibió, False si ninguno existe.
    """
    entregados = False
    for dest in mensaje.destinatarios:
      usuario = self.obtener_usuario(dest)
      if usuario:
        usuario.recibir(mensaje)
        entregados = True
      else:
        # En una implementacion real podriamos poner en cola o enviar NDR
        print(f"Advertencia: destinatario {dest} no existe en el servidor")
    return entregados

  def listar_usuarios(self) -> List[str]:
    """
    Devuelve la lista de emails de todos los usuarios registrados.
    """
    return list(self._usuarios.keys())

  def __repr__(self) -> str:
    """Representación legible del servidor para depuración."""
    return f"<ServidorCorreo usuarios={len(self._usuarios)}>"


# Ejemplo de uso / pruebas simples
if __name__ == '__main__':
  server = ServidorCorreo()
  a = server.registrar_usuario('ana@example.com', 'Ana')
  b = server.registrar_usuario('ben@example.com', 'Ben')

  # Ana envia a Ben
  msg = a.enviar(server, ['ben@example.com'], 'Hola', 'Esto es un test')
  print('Mensaje enviado:', msg)

  # Ver carpetas
  print('Carpetas Ana:', a.listar_carpetas())
  print('Carpetas Ben:', b.listar_carpetas())

  # Listar mensajes en INBOX de Ben
  inbox_ben = b.obtener_carpeta('INBOX').listar()
  print('Inbox de Ben:', inbox_ben)