import colander
from deform.widget import MappingWidget, SelectWidget, SequenceWidget, TextAreaWidget
from c2cgeoform.schema import GeoFormSchemaNode
from c2cgeoportal_commons.models.main import Metadata


@colander.deferred
def metadata_types(node, kw):
    return {
        m['name']: m.get('type', 'string')
        for m in kw['request'].registry.settings['admin_interface']['available_metadata']
    }


@colander.deferred
def metadata_name_widget(node, kw):
    return SelectWidget(
        values=[
            (m['name'], m['name'])
            for m in sorted(
                kw['request'].registry.settings['admin_interface']['available_metadata'],
                key=lambda m: m['name'])
        ]
    )


class MetadataSchemaNode(GeoFormSchemaNode):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.available_types = []

        self._add_value_node('string', colander.String())
        self._add_value_node('liste', colander.String())
        self._add_value_node('boolean', colander.Boolean())
        self._add_value_node('int', colander.Int())
        self._add_value_node('float', colander.Float())
        self._add_value_node('url', colander.String())
        self._add_value_node(
            'json',
            colander.String(),
            widget=TextAreaWidget(rows=10))
        # self._add_value_node('date', colander.Date())
        # self._add_value_node('time', colander.Time())
        # self._add_value_node('datetime', colander.DateTime())

    def _add_value_node(self, type_name, colander_type, **kw):
        self.add_before(
            'description',
            colander.SchemaNode(
                colander_type,
                name=type_name,
                missing=colander.null,
                **kw))
        self.available_types.append(type_name)

    def objectify(self, dict_, context=None):
        # depending on the type get the value from the right widget
        dict_['value'] = dict_[self._ui_type(dict_['name'])]
        return super().objectify(dict_, context)

    def dictify(self, obj):
        dict_ = super().dictify(obj)
        value = obj.value or colander.null
        '''
        import dateutil.parser
        ui_type = self._ui_type(obj.name)
        if ui_type == 'date':
            value = dateutil.parser.parse(value).date()
        if ui_type == 'datetime':
            value = dateutil.parser.parse(value)
        if ui_type == 'time':
            value = dateutil.parser.parse(value).time()
        '''
        # depending on the type set the value in the right widget
        dict_[self._ui_type(obj.name)] = value
        return dict_

    def _ui_type(self, metadata_name):
        metadata_type = self.metadata_types.get(metadata_name, 'string')
        return metadata_type if metadata_type in self.available_types else 'string'


metadatas_schema_node = colander.SequenceSchema(
    MetadataSchemaNode(
        Metadata,
        name='metadata',
        metadata_types=metadata_types,
        widget=MappingWidget(template='metadata'),
        overrides={
            'name': {
                'widget': metadata_name_widget
            }
        }
    ),
    name='metadatas',
    metadata_types=metadata_types,
    widget=SequenceWidget(
        template='metadatas',
        category='structural')
)
