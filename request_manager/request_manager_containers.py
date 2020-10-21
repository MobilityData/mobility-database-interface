from dependency_injector import providers, containers
from request_manager.api_client import ApiClient
from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_client import SparqlClient
from request_manager.sparql_request_manager import SparqlRequestManager
import utilities.external_utils


class Configs(containers.DeclarativeContainer):
    """Configuration containers for dependency injection for request managers usage.
    """
    staging_api_config = providers.Configuration('config')
    staging_api_config.set("url", utilities.external_utils.get_staging_api_url())
    staging_sparql_config = providers.Configuration('config')
    staging_sparql_config.set("url", utilities.external_utils.get_staging_sparql_url())

    production_api_config = providers.Configuration('config')
    production_api_config.set("url", utilities.external_utils.get_production_api_url())
    production_sparql_config = providers.Configuration('config')
    production_sparql_config.set("url", utilities.external_utils.get_production_sparql_url())


class Clients(containers.DeclarativeContainer):
    """Client containers for dependency injection for request managers usage.
    """
    staging_api_client = providers.Singleton(ApiClient, Configs.staging_api_config)
    staging_sparql_client = providers.Singleton(SparqlClient, Configs.staging_sparql_config)

    production_api_client = providers.Singleton(ApiClient, Configs.production_api_config)
    production_sparql_client = providers.Singleton(SparqlClient, Configs.production_sparql_config)


class Managers(containers.DeclarativeContainer):
    """Manager containers for dependency injection for request managers usage.
    """
    staging_api_request_manager = providers.Factory(ApiRequestManager, client=Clients.staging_api_client)
    staging_sparql_request_manager = providers.Factory(SparqlRequestManager, client=Clients.staging_sparql_client)

    production_api_request_manager = providers.Factory(ApiRequestManager, client=Clients.production_api_client)
    production_sparql_request_manager = providers.Factory(SparqlRequestManager, client=Clients.production_sparql_client)
