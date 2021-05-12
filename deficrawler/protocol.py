from deficrawler.protocol_base import ProtocolBase

from datetime import datetime


class Protocol(ProtocolBase):
    def __init__(self, protocol, chain, version):
        super().__init__(
            protocol=protocol,
            chain=chain,
            version=version
        )

    def get_data_from_date_range(self, from_date, to_date, entity):

        from_timestamp = int(
            datetime.strptime(from_date, '%d/%m/%Y %H:%M:%S').strftime("%s"))

        to_timestamp = int(datetime.strptime(
            to_date, '%d/%m/%Y %H:%M:%S').strftime("%s"))

        config = super().get_protocol_config(entity)

        response_data = super().query_data_from_date_range(
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
            entity=entity
        )

        return super().map_data(
            response_data=response_data,
            config=config
        )

    def get_all_users(self):

        config = super().get_protocol_config('user')

        response_data = super().query_data_parameter(
            entity='user'
        )

        return super().map_data(
            response_data=response_data,
            config=config
        )

    def get_user_positions(self, user):

        config = super().get_protocol_config('user_position')
        user_name = self.mappings_file['entities']['user_position']['query']['params']['user']

        response_data = super().query_data_filtered(
            entity='user_position',
            filters={user_name: user}
        )

        return super().map_data(
            response_data=response_data,
            config=config
        )

