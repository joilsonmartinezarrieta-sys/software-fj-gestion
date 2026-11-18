import re
from abc import ABC, abstractmethod
from src.excepciones import (
    DatosClienteInvalidosError,
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
)


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    _contador = 0

    def __init__(self):
        Entidad._contador += 1
        self._id_entidad = Entidad._contador

    @property
    def id_entidad(self):
        """Devuelve el id de la entidad (solo lectura)."""
        return self._id_entidad

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe explicar cómo se describe (polimorfismo)."""

    def __str__(self):
        return self.describir()


class Cliente(Entidad):
    """Cliente de Software FJ con datos personales encapsulados."""

    def __init__(self, nombre, documento, correo, telefono=None):
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        super().__init__()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = self._validar_nombre(valor)

    @staticmethod
    def _validar_nombre(valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosClienteInvalidosError("El nombre es obligatorio y debe ser texto.")
        nombre = " ".join(valor.split())
        if len(nombre) < 3:
            raise DatosClienteInvalidosError("El nombre debe tener al menos 3 caracteres.")
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", nombre):
            raise DatosClienteInvalidosError("El nombre solo puede contener letras y espacios.")
        return nombre.title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        self.__documento = self._validar_documento(valor)

    @staticmethod
    def _validar_documento(valor):
        texto = str(valor).strip()
        try:
            int(texto)
        except ValueError as error:
            raise DatosClienteInvalidosError("El documento debe contener solo números.") from error
        if not texto.isdigit() or not 6 <= len(texto) <= 12:
            raise DatosClienteInvalidosError("El documento debe tener entre 6 y 12 dígitos.")
        return texto

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()):
            raise DatosClienteInvalidosError("El correo electrónico no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            self.__telefono = "No registrado"
            return
        texto = str(valor).strip()
        if not texto.isdigit() or not 7 <= len(texto) <= 15:
            raise DatosClienteInvalidosError("El teléfono debe tener entre 7 y 15 dígitos.")
        self.__telefono = texto

    def describir(self):
        return f"Cliente #{self.id_entidad}: {self.nombre} (Doc: {self.documento}, Correo: {self.correo})"


class GestorClientes:
    """Administra el registro y búsqueda de clientes del sistema."""

    def __init__(self):
        self._clientes = []

    def registrar_cliente(self, cliente):
        for existente in self._clientes:
            if existente.documento == cliente.documento:
                raise ClienteDuplicadoError(f"Ya existe un cliente con el documento {cliente.documento}.")
        self._clientes.append(cliente)

    def buscar_por_documento(self, documento):
        doc = str(documento).strip()
        for cliente in self._clientes:
            if cliente.documento == doc:
                return cliente
        raise ClienteNoEncontradoError(f"No se encontró ningún cliente con documento {doc}.")

    def listar_clientes(self):
        return list(self._clientes)