package osbourn.cloudcubes.lambda.serverstarter;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import osbourn.cloudcubes.core.constructs.InfrastructureData;

import java.util.Map;

public class ServerStarterLambdaHandler implements RequestHandler<Map<String, String>, String> {
    @Override
    public String handleRequest(Map<String, String> event, Context context) {
        LambdaLogger logger = context.getLogger();
        String response = "200 OK";

        InfrastructureData infrastructureData = InfrastructureData.fromEnvironment();
        logger.log(infrastructureData.getServerDataBaseName());

        return response;
    }
}