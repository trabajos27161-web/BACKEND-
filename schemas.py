from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

class RolCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool = True
class RolUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool | None = None
class RolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; nombre: str; descripcion: str | None; estado: bool

class ModuloCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    ruta: str | None = Field(default=None, max_length=255)
    icono: str | None = Field(default=None, max_length=100)
    estado: bool = True
class ModuloUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    ruta: str | None = Field(default=None, max_length=255)
    icono: str | None = Field(default=None, max_length=100)
    estado: bool | None = None
class ModuloResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; nombre: str; descripcion: str | None; ruta: str | None; icono: str | None; estado: bool

class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    correo: EmailStr = Field(max_length=150)
    password: str = Field(min_length=10, max_length=255)
    idrol: int = Field(gt=0)
    estado: bool = True
class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    apellido: str | None = Field(default=None, min_length=1, max_length=100)
    correo: EmailStr | None = Field(default=None, max_length=150)
    password: str | None = Field(default=None, min_length=10, max_length=255)
    idrol: int | None = Field(default=None, gt=0)
    estado: bool | None = None
class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; nombre: str; apellido: str; correo: str; idrol: int; estado: bool; fecha_creacion: datetime

class ModuloXRolCreate(BaseModel):
    idrol: int = Field(gt=0); idmodulo: int = Field(gt=0); estado: bool = True
class ModuloXRolUpdate(BaseModel):
    idrol: int | None = Field(default=None, gt=0); idmodulo: int | None = Field(default=None, gt=0); estado: bool | None = None
class ModuloXRolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; idrol: int; idmodulo: int; estado: bool

class TipoSensorCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, max_length=255)
    unidad_medida: str = Field(min_length=1, max_length=20)
    fabricante: str | None = Field(default=None, max_length=100)
    modelo: str | None = Field(default=None, max_length=100)
    estado: bool = True
class TipoSensorUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, max_length=255)
    unidad_medida: str | None = Field(default=None, min_length=1, max_length=20)
    fabricante: str | None = Field(default=None, max_length=100)
    modelo: str | None = Field(default=None, max_length=100)
    estado: bool | None = None
class TipoSensorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; nombre: str; descripcion: str | None; unidad_medida: str; fabricante: str | None; modelo: str | None; estado: bool

class SensorCreate(BaseModel):
    idtiposensor: int = Field(gt=0)
    codigo: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=100)
    modelo: str | None = Field(default=None, max_length=100)
    fabricante: str | None = Field(default=None, max_length=100)
    ubicacion_fisica: str | None = Field(default=None, max_length=255)
    estado: bool = True
    fecha_instalacion: datetime | None = None
class SensorUpdate(BaseModel):
    idtiposensor: int | None = Field(default=None, gt=0)
    codigo: str | None = Field(default=None, min_length=1, max_length=50)
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    modelo: str | None = Field(default=None, max_length=100)
    fabricante: str | None = Field(default=None, max_length=100)
    ubicacion_fisica: str | None = Field(default=None, max_length=255)
    estado: bool | None = None
    fecha_instalacion: datetime | None = None
class SensorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; idtiposensor: int; codigo: str; nombre: str; modelo: str | None; fabricante: str | None; ubicacion_fisica: str | None; estado: bool; fecha_instalacion: datetime | None

class DptoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    codigo: str | None = Field(default=None, max_length=10)
    estado: bool = True
class DptoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    codigo: str | None = Field(default=None, max_length=10)
    estado: bool | None = None
class DptoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; nombre: str; codigo: str | None; estado: bool

class LocacionCreate(BaseModel):
    iddpto: int = Field(gt=0)
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    direccion: str | None = Field(default=None, max_length=255)
    latitud: Decimal | None = Field(default=None, ge=-90, le=90, max_digits=10, decimal_places=6)
    longitud: Decimal | None = Field(default=None, ge=-180, le=180, max_digits=10, decimal_places=6)
    estado: bool = True
class LocacionUpdate(BaseModel):
    iddpto: int | None = Field(default=None, gt=0)
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    direccion: str | None = Field(default=None, max_length=255)
    latitud: Decimal | None = Field(default=None, ge=-90, le=90, max_digits=10, decimal_places=6)
    longitud: Decimal | None = Field(default=None, ge=-180, le=180, max_digits=10, decimal_places=6)
    estado: bool | None = None
class LocacionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; iddpto: int; nombre: str; descripcion: str | None; direccion: str | None; latitud: Decimal | None; longitud: Decimal | None; estado: bool

class LecturaCreate(BaseModel):
    idsensor: int = Field(gt=0); idlocacion: int = Field(gt=0)
    valor: Decimal = Field(ge=0, le=14, max_digits=6, decimal_places=2)
    temperatura: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    fecha_hora: datetime | None = None
    calidad: str | None = Field(default=None, max_length=50)
class LecturaUpdate(BaseModel):
    idsensor: int | None = Field(default=None, gt=0); idlocacion: int | None = Field(default=None, gt=0)
    valor: Decimal | None = Field(default=None, ge=0, le=14, max_digits=6, decimal_places=2)
    temperatura: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    fecha_hora: datetime | None = None
    calidad: str | None = Field(default=None, max_length=50)
class LecturaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; idsensor: int; idlocacion: int; valor: Decimal; temperatura: Decimal | None; fecha_hora: datetime; calidad: str | None

class AsignacionSensorCreate(BaseModel):
    idusuario: int = Field(gt=0); idsensor: int = Field(gt=0)
    fecha_asignacion: datetime | None = None; fecha_fin: datetime | None = None
    estado: Literal['ACTIVA', 'FINALIZADA'] = 'ACTIVA'
    @model_validator(mode='after')
    def validate_dates(self):
        if self.fecha_asignacion and self.fecha_fin and self.fecha_fin < self.fecha_asignacion:
            raise ValueError('fecha_fin debe ser posterior o igual a fecha_asignacion')
        return self
class AsignacionSensorUpdate(BaseModel):
    idusuario: int | None = Field(default=None, gt=0); idsensor: int | None = Field(default=None, gt=0)
    fecha_asignacion: datetime | None = None; fecha_fin: datetime | None = None
    estado: Literal['ACTIVA', 'FINALIZADA'] | None = None
class AsignacionSensorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; idusuario: int; idsensor: int; fecha_asignacion: datetime; fecha_fin: datetime | None; estado: Literal['ACTIVA', 'FINALIZADA']
