package osbourn.cloudcubes.core.server;

public interface Server {
    /**
     * Gets the numeric id of the server.
     *
     * @return The numeric id of the server.
     */
    int getId();

    /**
     * Gets the state of the server:
     * <ul>
     * <li>OFFLINE: Server is currently offline (there are no EC2 instances launched for it)</li>
     * <li>ONLINE:  Server is online (there may be an EC2 instance that corresponds to the server)</li>
     * <li>UNKNOWN: It is unknown what the state of the server is because an operation may have failed</li>
     * </ul>
     * Please note that that this method may or may not do some work to check the state of the server to make sure it
     * matches the return value of this method, especially if the state is recorded as UNKNOWN.
     *
     * @return The state of the server
     */
    ServerState getServerState();

    /**
     * Launches the server if it is offline. If the server is not in an OFFLINE state, an IllegalStateException may be
     * thrown.
     *
     * @throws java.lang.IllegalStateException If the server is currently online
     */
    void startServer();
}
