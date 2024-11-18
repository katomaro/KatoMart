import json

from . import Base
from sqlalchemy import Column, Integer, String, Boolean, Text

class Configuration(Base):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    configuration_group_name = Column(String(100), nullable=False, default='geral')
    key = Column(String(100), nullable=False, unique=True)
    title = Column(String(300), nullable=True, default='Configuração sem título!')
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    value_type = Column(String(32), nullable=False, default='str')  # 'str', 'int', 'float', 'bool', 'list', 'json'
    hidden = Column(Boolean, default=True)
    voidable = Column(Boolean, default=False)
    editable = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)
    sponsor_only = Column(Boolean, default=False)
    created_at = Column(Integer, nullable=False, default=0)
    updated_at = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Configuration(configuration_group_name='{self.configuration_group_name}', key='{self.key}', title='{self.title}, value='{self.value}', description='{self.description}', value_type='{self.value_type}', hidden='{self.hidden}' voidable='{self.voidable}', can_edit='{self.editable}' enabled={self.enabled}, created_at='{self.created_at}, updated_at='{self.updated_at}')>"

    def to_dict(self):
        if isinstance(self.configuration_group_name, bytes):
            normalized_config_group = self.configuration_group_name.decode('utf-8')
        else:
            normalized_config_group = self.configuration_group_name

        if isinstance(self.value, bytes):
            normalized_value = self.value.decode('utf-8')
        else:
            normalized_value = self.value

        if isinstance(self.description, bytes):
            normalized_description = self.description.decode('utf-8')
        else:
            normalized_description = self.description

        try:
            normalized_value = json.loads(normalized_value)
        except json.JSONDecodeError:
            try:
                normalized_value = eval(normalized_value)
            except:
                normalized_value = normalized_value

        if not normalized_description:
            normalized_description = ''

        if isinstance(self.value_type, bytes):
            normalized_value_type = self.value_type.decode('utf-8')
        else:
            normalized_value_type = self.value_type

        if normalized_value_type == 'bool':
            normalized_value = bool(normalized_value)

        return {
            'id': int(self.id),
            'configuration_group_name': normalized_config_group,
            'key': str(self.key),
            'title': str(self.title),
            'value': normalized_value,
            'description': normalized_description,
            'value_type': normalized_value_type,
            'hidden': bool(self.hidden),
            'voidable': bool(self.voidable),
            'editable': bool(self.editable),
            'enabled': bool(self.enabled),
            'sponsor_only': bool(self.sponsor_only),
            'created_at': int(self.created_at),
            'updated_at': int(self.updated_at)
        }
