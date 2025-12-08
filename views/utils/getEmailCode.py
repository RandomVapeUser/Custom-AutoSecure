import mailslurp_client
import re

def getEmailCode(email: str, key: str) -> str:

    emailID = email.split("@")[0]

    configuration = mailslurp_client.Configuration()
    configuration.api_key["x-api-key"] = key

    with mailslurp_client.ApiClient(configuration) as api_client:
        inbox_api = mailslurp_client.InboxControllerApi(api_client)
        email_api = mailslurp_client.EmailControllerApi(api_client)

        while True:

            emails = inbox_api.get_emails(
                inbox_id = emailID,
                limit = 3,
                sort = "DESC"
            )

            if not emails:
                continue

            else:
                    
                email_id = emails[0].id

                bemail = email_api.get_email(email_id).body
                code = re.search(r"Security code:\s*<\/?[^>]*>\s*(\d{6})", bemail).group(1)

                return code
