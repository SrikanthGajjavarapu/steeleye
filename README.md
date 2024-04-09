API Documentation
This document provides an overview of the endpoints available in the FastAPI implementation and how to use them.

Overview
The API offers endpoints for managing trades, including retrieving all trades, searching for specific trades, filtering trades based on various parameters, and accessing individual trades by their IDs.

Base URL
The base URL for accessing the API is http://127.0.0.1:8000.

Endpoints
Get All Trades
Endpoint: /trades

Method: GET

Description: Returns a list of all trades stored in the database.

Search Trades
Endpoint: /trades/search

Method: GET

Description: Searches for trades based on the provided query parameter. If no query parameter is provided, all trades are returned.

Query Parameters:

search: Search query for trades
Filter Trades
Endpoint: /trades/filter

Method: GET

Description: Filters trades based on various parameters such as asset class, trade date-time range, price range, and trade type.

Query Parameters:

filter: Additional filter criteria (optional)
assetClass: Asset class of the trade (optional)
start: Minimum date for the tradeDateTime field (optional)
end: Maximum date for the tradeDateTime field (optional)
minPrice: Minimum value for the tradeDetails.price field (optional)
maxPrice: Maximum value for the tradeDetails.price field (optional)
tradeType: The tradeDetails.buySellIndicator is a BUY or SELL (optional)
Get Trade by ID
Endpoint: /trades/{trade_id}

Method: GET

Description: Retrieves a specific trade by its unique ID.

Path Parameters:

trade_id: The unique ID of the trade to retrieve
Example Usage
Get All Trades
bash
Copy code
GET /trades
Search Trades
sql
Copy code
GET /trades/search?search=AAPL
Filter Trades
sql
Copy code
GET /trades/filter?tradeType=SELL
Get Trade by ID
bash
Copy code
GET /trades/5
Data Models
The API uses two Pydantic models to represent trade data:

TradeDetails: Contains details such as buy/sell indicator, price, and quantity.
Trade: Represents a trade with attributes including asset class, counterparty, instrument ID, instrument name, trade date-time, trade details, trade ID, and trader.
Responses
Successful requests return status code 200 (OK).
If a requested resource cannot be found, the API returns status code 404 (Not Found).
Invalid requests may result in status code 400 (Bad Request).
You can use this template to create an "API.md" file for your FastAPI implementation. Make sure to update any placeholders with actual values or descriptions specific to your project.





