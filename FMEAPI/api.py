class APIConfig:

    def __init__(self):
        self.api_url = {
            "api_root": "http://%s/fmerest/v3/",
            "health_check": "healthcheck?textResponse=false",
            "list_repos": "repositories?limit=-1&offset=-1&fmetoken=",
            "get_repo_info": "repositories/%s?fmetoken=",
            "create_repo": "repositories/?fmetoken=",
            "list_repo_fmws": "repositories/%s/items?fmetoken=",
            "get_repo_fmw": "repositories/%s/items/%s?fmetoken=",
            "list_fmw_datasets": "repositories/%s/items/%s/datasets/%s?fmetoken=",
            "get_fmw_datasets_info": "repositories/%s/items/%s/datasets/%s/%s?fmetoken=",
            "list_fmw_datasets_features": "repositories/%s/items/%s/datasets/%s/%s/featuretypes?fmetoken=",
            "get_fmw_datasets_feature_info": "repositories/%s/items/%s/datasets/%s/%s/featuretypes/%s?fmetoken=",
            "list_fmw_parameters": "repositories/%s/items/%s/parameters?fmetoken=",
            "get_fmw_parameters_pub_info": "repositories/%s/items/%s/parameters/%s?fmetoken=",
            "list_fmw_services": "repositories/%s/items/%s/services?fmetoken=",
            "create_repo": "repositories?fmetoken=",
            "delete_repo": "repositories/%s?fmetoken=",
            "create_fmw": "repositories/%s/items?fmetoken=",
            "delete_fmw": "repositories/%s/items/%s?fmetoken=",
            "create_fmw_service": "repositories/%s/items/%s/services?fmetoken=",
            "list_fmw_resources": "repositories/%s/items/%s/resources?fmetoken=",
            "get_fmw_resource": "repositories/%s/items/%s/resources/%s?fmetoken=",
            "create_fmw_resources": "repositories/%s/items/%s/resources?fmetoken=",
            "delete_fmw_resources": "repositories/%s/items/%s/resources/%s?fmetoken="
        }
