// $Id$
package com.zoho.analytics.client;


/**
 * ServerException is thrown if the analytics server has received the request but did not process the request due to some error. For example if authorization fails.
 */
public class ServerException extends Exception
{
    private final int httpStatusCode;
    private final int errorCode;
    private final String errorMessage;

    protected ServerException(int httpStatusCode, int errorCode, String message)
    {
        this.httpStatusCode = httpStatusCode;
        this.errorCode = errorCode;
        this.errorMessage = message;
    }

    /**
    * The http status code for the request.
    * @return An <code>int</code> value.
    */
    public int getHttpStatusCode()
    {
        return httpStatusCode;
    }

    /**
    * Returns the error code sent by the server.
    * @return A <code>int</code> value.
    */
    public int getErrorCode()
    {
        return errorCode;
    }

    /**
    * Returns the error message sent by the server.
    * @return A <code>String</code> value.
    */
    public String getErrorMessage()
    {
        return errorMessage;
    }

    /**
    * Returns the entire error details sent by the server.
    * @return A <code>String</code> value.
    */
    public String toString()
    {
        return "ServerException (HttpStatusCode: " + httpStatusCode + " Error Code: " + errorCode + ", Message: " + errorMessage+")";
    }                     
}
