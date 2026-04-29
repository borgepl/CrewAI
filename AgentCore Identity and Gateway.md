# Steps to setup Agentcore Identity and Gateway

# 1. oAuth Server - AWS Create Cognito User Pool (Machine-to-Machine)

# 2. Get the issuer URL, Client ID and client Secret for the registered app (vacation_planner_agent)

# 3. Create DynamoDB Table to host the Travel Packages data.

# 4. Create Lambda function / OpenAPI schema.

# 5. Create Agentcore Gateway (MCP protocol).

    # a. Discovery URL format : https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_XTxrQPRNE/well-known/openid-configuration

    # b. Allowed audience : Leave blank

    # c. Allowed clients : app client id

    # d. Gateway Service Role : Permissions - invoke lambda function

# 6. Test the Gateway with gwtest.py