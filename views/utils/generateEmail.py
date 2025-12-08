import mailslurp_client

def generateEmail(key: str) -> str:

    configuration = mailslurp_client.Configuration()
    configuration.api_key["x-api-key"] = key

    with mailslurp_client.ApiClient(configuration) as api_client:

        inbox_controller = mailslurp_client.InboxControllerApi(api_client)
        inbox = inbox_controller.create_inbox()
        
        return inbox.email_address