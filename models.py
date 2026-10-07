from datetime import datetime
from decimal import Decimal
from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Identity, Integer, Numeric, String, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Rol(Base):
    __tablename__ = 'rol'
    __table_args__ = (UniqueConstraint('nombre', name='uq_rol_nombre'),)
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    usuarios: Mapped[list['Usuarios']] = relationship(back_populates='rol', passive_deletes='all')
    modulos_x_rol: Mapped[list['ModuloXRol']] = relationship(back_populates='rol', passive_deletes='all')

class Modulo(Base):
    __tablename__ = 'modulo'
    __table_args__ = (UniqueConstraint('nombre', name='uq_modulo_nombre'),)
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255))
    ruta: Mapped[str | None] = mapped_column(String(255))
    icono: Mapped[str | None] = mapped_column(String(100))
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    roles: Mapped[list['ModuloXRol']] = relationship(back_populates='modulo', passive_deletes='all')

class Usuarios(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (UniqueConstraint('correo', name='uq_usuarios_correo'),)
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    idrol: Mapped[int] = mapped_column(ForeignKey('rol.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    rol: Mapped['Rol'] = relationship(back_populates='usuarios')
    asignaciones: Mapped[list['AsignacionSensor']] = relationship(back_populates='usuario', passive_deletes='all')

class ModuloXRol(Base):
    __tablename__ = 'modulo_x_rol'
    __table_args__ = (UniqueConstraint('idrol', 'idmodulo', name='uq_modulo_x_rol'),)
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    idrol: Mapped[int] = mapped_column(ForeignKey('rol.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    idmodulo: Mapped[int] = mapped_column(ForeignKey('modulo.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    rol: Mapped['Rol'] = relationship(back_populates='modulos_x_rol')
    modulo: Mapped['Modulo'] = relationship(back_populates='roles')

class TipoSensor(Base):
    __tablename__ = 'tipo_sensor'
    __table_args__ = (UniqueConstraint('nombre', name='uq_tipo_sensor_nombre'),)
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255))
    unidad_medida: Mapped[str] = mapped_column(String(20), nullable=False)
    fabricante: Mapped[str | None] = mapped_column(String(100))
    modelo: Mapped[str | None] = mapped_column(String(100))
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    sensores: Mapped[list['Sensor']] = relationship(back_populates='tipo_sensor', passive_deletes='all')

class Sensor(Base):
    __tablename__ = 'sensor'
    __table_args__ = (UniqueConstraint('codigo', name='uq_sensor_codigo'),)
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    idtiposensor: Mapped[int] = mapped_column(ForeignKey('tipo_sensor.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    modelo: Mapped[str | None] = mapped_column(String(100))
    fabricante: Mapped[str | None] = mapped_column(String(100))
    ubicacion_fisica: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    fecha_instalacion: Mapped[datetime | None] = mapped_column(DateTime)
    tipo_sensor: Mapped['TipoSensor'] = relationship(back_populates='sensores')
    lecturas: Mapped[list['Lectura']] = relationship(back_populates='sensor', passive_deletes='all')
    asignaciones: Mapped[list['AsignacionSensor']] = relationship(back_populates='sensor', passive_deletes='all')

class Dpto(Base):
    __tablename__ = 'dpto'
    __table_args__ = (UniqueConstraint('nombre', name='uq_dpto_nombre'), UniqueConstraint('codigo', name='uq_dpto_codigo'))
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo: Mapped[str | None] = mapped_column(String(10))
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    locaciones: Mapped[list['Locacion']] = relationship(back_populates='departamento', passive_deletes='all')

class Locacion(Base):
    __tablename__ = 'locacion'
    __table_args__ = (CheckConstraint('latitud IS NULL OR latitud BETWEEN -90 AND 90', name='ck_locacion_latitud'), CheckConstraint('longitud IS NULL OR longitud BETWEEN -180 AND 180', name='ck_locacion_longitud'))
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    iddpto: Mapped[int] = mapped_column(ForeignKey('dpto.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255))
    direccion: Mapped[str | None] = mapped_column(String(255))
    latitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 6))
    longitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 6))
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('TRUE'))
    departamento: Mapped['Dpto'] = relationship(back_populates='locaciones')
    lecturas: Mapped[list['Lectura']] = relationship(back_populates='locacion', passive_deletes='all')

class Lectura(Base):
    __tablename__ = 'lectura'
    __table_args__ = (CheckConstraint('valor >= 0 AND valor <= 14', name='ck_lectura_valor'),)
    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    idsensor: Mapped[int] = mapped_column(ForeignKey('sensor.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    idlocacion: Mapped[int] = mapped_column(ForeignKey('locacion.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    temperatura: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    calidad: Mapped[str | None] = mapped_column(String(50))
    sensor: Mapped['Sensor'] = relationship(back_populates='lecturas')
    locacion: Mapped['Locacion'] = relationship(back_populates='lecturas')

class AsignacionSensor(Base):
    __tablename__ = 'asignacion_sensor'
    __table_args__ = (CheckConstraint("estado IN ('ACTIVA', 'FINALIZADA')", name='ck_asignacion_estado'), CheckConstraint('fecha_fin IS NULL OR fecha_fin >= fecha_asignacion', name='ck_asignacion_fechas'))
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    idusuario: Mapped[int] = mapped_column(ForeignKey('usuarios.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    idsensor: Mapped[int] = mapped_column(ForeignKey('sensor.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    fecha_asignacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    fecha_fin: Mapped[datetime | None] = mapped_column(DateTime)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'ACTIVA'"))
    usuario: Mapped['Usuarios'] = relationship(back_populates='asignaciones')
    sensor: Mapped['Sensor'] = relationship(back_populates='asignaciones')



