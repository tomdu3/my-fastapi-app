# Logging Integration Walkthrough

I have successfully integrated structured logging into your FastAPI application. This ensures that every request and error is captured for better observability, especially useful in production environments.

## Changes

### 1. Configuration and Middleware
I added a `log_requests` middleware in `app/main.py` that captures:
- HTTP Method
- Request Path
- Status Code
- Duration (ms)

It also preserves the `X-Process-Time` header for backward compatibility.

### 2. Global Exception Handler
I updated the `StarletteHTTPException` handler to log errors before returning the response. This ensures you see the error details in your logs even if the user gets a sanitized error message.

## Verification Results

I ran a verification script against the running server.

### Request Logging
When a successful request is made to `/`:
```
INFO:api_logger:method=GET path=/ status=200 duration=1.77ms
```

### Error Logging
When a request is made to a non-existent route `/non-existent-route` (404):
```
ERROR:api_logger:HTTP Error: Not Found path=/non-existent-route code=404
INFO:api_logger:method=GET path=/non-existent-route status=404 duration=0.71ms
```
The error is logged at `ERROR` level, followed by the request completion log at `INFO` level.

Sensitive data is not logged as we are only capturing metadata (path, method, status, duration).
