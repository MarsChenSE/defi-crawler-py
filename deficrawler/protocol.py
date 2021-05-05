from deficrawler.querys import Querys
from deficrawler.mappers import Mappers
from deficrawler.api_calls import get_data_from, get_data_parameter, get_data_filtered

from datetime import date, datetime
import pkgutil
import json


class Protocol:
    def __init__(self, protocol, chain, version):
        self.protocol = protocol
        self.query_from_timestamp = Querys.QUERY_FROM_TIMESTAMP
        self.query_all_elements = Querys.QUERY_ALL_ELEMENTS
        self.query_filter = Querys.QUERY_ELEMENT_FILTER
        config_file = pkgutil.get_data(
            'deficrawler.config',
            protocol.lower() + "-" + str(version) + ".json"
        )

        self.mappings_file = json.loads(config_file.decode())
        self.chain = chain
        self.version = version
        self.endpoint = self.mappings_file['protocol']['endpoint'][chain.lower(
        )]

    def get_data_from_date_range(self, from_date, to_date, entity):

        from_timestamp = int(
            datetime.strptime(from_date, '%d/%m/%Y %H:%M:%S').strftime("%s"))

        to_timestamp = int(datetime.strptime(
            to_date, '%d/%m/%Y %H:%M:%S').strftime("%s"))

        attributes = self.mappings_file['entities'][entity]['attributes']
        transformations = self.mappings_file['entities'][entity]['transformations']
        query_elements = self.mappings_file['entities'][entity]['query']['fields']

        json_data = get_data_from(query_input=self.query_from_timestamp,
                                  from_timestamp=from_timestamp,
                                  to_timestamp=to_timestamp,
                                  entity=entity,
                                  mappings_file=self.mappings_file,
                                  protocol=self.protocol,
                                  endpoint=self.endpoint)

        return Mappers.map_data(json_data=json_data,
                                protocol=self.protocol,
                                chain=self.chain,
                                version=self.version,
                                entity=entity,
                                attributes=attributes,
                                transformations=transformations,
                                query_elements=query_elements)

    def get_all_users(self):

        attributes = self.mappings_file['entities']['user']['attributes']
        transformations = self.mappings_file['entities']['user']['transformations']
        query_elements = self.mappings_file['entities']['user']['query']['fields']

        json_data = get_data_parameter(query_input=self.query_all_elements,
                                       entity='user',
                                       mappings_file=self.mappings_file,
                                       protocol=self.protocol,
                                       endpoint=self.endpoint)

        return Mappers.map_data(json_data=json_data,
                                protocol=self.protocol,
                                chain=self.chain,
                                version=self.version,
                                entity='user',
                                attributes=attributes,
                                transformations=transformations,
                                query_elements=query_elements)

    def get_user_positions(self, user):

        attributes = self.mappings_file['entities']['user_position']['attributes']
        transformations = self.mappings_file['entities']['user_position']['transformations']
        query_elements = self.mappings_file['entities']['user_position']['query']['fields']

        json_data = get_data_filtered(query_input=self.query_filter,
                                      entity='user_position',
                                      mappings_file=self.mappings_file,
                                      protocol=self.protocol,
                                      endpoint=self.endpoint,
                                      filters={"user": user})

        return Mappers.map_data(json_data=json_data,
                                protocol=self.protocol,
                                chain=self.chain,
                                version=self.version,
                                entity='user_position',
                                attributes=attributes,
                                transformations=transformations,
                                query_elements=query_elements)