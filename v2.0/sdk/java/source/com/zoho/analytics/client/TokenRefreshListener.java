// $Id$
package com.zoho.analytics.client;

/**
 * Receives OAuth access tokens as <code>AnalyticsClient</code> obtains them, so a caller can cache a
 * token and re-supply it later instead of exchanging the refresh token on every run.
 *
 * <p>This is entirely optional. A client with no listener registered behaves exactly as before: it
 * obtains an access token on first use and discards it when the client is garbage collected. A
 * caller that does register one typically persists the token and hands it back to the next client
 * through {@link AnalyticsClient#setAccessToken(String)}, which keeps the number of token exchanges
 * within the account's OAuth rate limit.
 *
 * <p>Implementations must not throw: the client logs and continues, because a failure to cache a
 * token must never fail the API call that produced it. They may also be invoked from more than one
 * thread when a single client is shared, so they must be safe to call concurrently.
 */
@FunctionalInterface
public interface TokenRefreshListener
{
    /**
     * Invoked immediately after a new access token has been obtained from the accounts server.
     *
     * @param accessToken The access token, exactly as returned by the accounts server.
     * @param expiresInSeconds The token lifetime in seconds as reported by the accounts server, or
     *                         <code>-1</code> when the response carried no lifetime.
     */
    void onTokenRefreshed(String accessToken, long expiresInSeconds);
}
