// $Id$
package com.zoho.analytics.client;

/**
 * ParseException is thrown if the server has responded but client was not able to parse the response.
 * Possible reasons could be version mismatch.The client might have to be updated to a newer version.
 */
public class ParseException extends Exception
{
    private String responseContent;

    protected ParseException(String responseContent,String message,Throwable th)
    {
        super(message,th);
        this.responseContent = responseContent;
    }

    /**
     * Returns the complete response content as sent by the server.
     * @return A <code>String</code> of response content
     */
    public String getResponseMessage()
    {
        return responseContent;
    }
}
