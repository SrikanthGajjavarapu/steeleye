import random    #Importing necessary modules and packages
from datetime import datetime, timedelta
import datetime as dt
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from random import randint, uniform, choice

#Two Pydantic models are defined: TradeDetails and Trade. These models represent the structure of the model and datatypes of model.
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None,
                                       description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")

#An instance of the FastAPI class is created
app = FastAPI()

# created Mock database
database = []

#this function generates random trades
#generating randomly assetclass,counterparty,traders,instrumentname...etc
def generate_random_trades(num_trades):
    trades = []
    trade_id = 0
    for _ in range(num_trades):   
        asset_class=random.choice(["Bond", "Equity", "FX"])
        counterparty=random.choice(["counterparty1", "counterparty2"])
        traders=random.choice(["trader1", "trader2", "trader3"])
        instrument_id = random.choice(["TSLA","AAPL","AMZN"])
        instrument_name = random.choice(["strategy1","strategy2"])
        trade_datetime = datetime.utcnow() - timedelta(days=randint(1, 365))   
        trade_id = trade_id+1     
        trade_details = TradeDetails(
            buySellIndicator=choice(["BUY", "SELL"]),
            price=uniform(10.0, 100.0),
            quantity=randint(1, 100),            
        )
        trade = Trade(
            assetClass=str(asset_class),
            counterparty=str(counterparty),
            instrumentId=str(instrument_id),
            instrumentName=str(instrument_name),
            tradeDateTime=trade_datetime,
            tradeDetails=trade_details,
            tradeId= str(trade_id),
            trader=str(traders),
        )
        trades.append(trade)
    return trades
    
database = generate_random_trades(30)
#storing randomly generated trades into mock database

#this endpoint returns all trades 
@app.get("/trades", response_model=List[Trade])
def get_trades():
    return database

#this endpoint returns counterparty,instrumentid,instrumentname,trader according our search
#search none returns all trades(database)
#if our search not found result raise an exception prints No trades found matching the search query
#endpoint Example: http://127.0.0.1:8000/trades/search?search=AAPL
@app.get("/trades/search")
def search_trades(
    search: str = Query(None, description="Search query for trades")
):
    if search is None:
        return database  # Return all trades if no search query is provided
    
    matching_trades = []
    for trade in database:
        if (
            search.lower() in trade.counterparty.lower()
            or search.lower() in trade.instrument_id.lower()
            or search.lower() in trade.instrument_name.lower()
            or search.lower() in trade.trader.lower()
        ):
            matching_trades.append(trade)
    
    if not matching_trades:
        raise HTTPException(status_code=404, detail="No trades found matching the search query")
    
    return matching_trades

#this endpoint filters according to our requiements assetclass,start&end time,min&max price,tradetype
#in function we can mention query otherwise it gives error
#ex: http://127.0.0.1:8000/trades/filter?tradeType=SELL
@app.get("/trades/filter", response_model=List[Trade])
async def filter_trades(
        filter: Optional[str] = Query(None, description="Search query"),
        assetClass: Optional[str] = Query(None, description="Asset class of the trade"),
        start: Optional[dt.datetime] = Query(None, description="Minimum date for the tradeDateTime field"),
        end: Optional[dt.datetime] = Query(None, description="Maximum date for the tradeDateTime field"),
        minPrice: Optional[float] = Query(None, description="Minimum value for the tradeDetails.price field"),
        maxPrice: Optional[float] = Query(None, description="Maximum value for the tradeDetails.price field"),
        tradeType: Optional[str] = Query(None, description="The tradeDetails.buySellIndicator is a BUY or SELL"),
):
    
    filtered_trades = []

    for trade in database:
        if filter and filter.lower() not in str(trade).lower():
            continue
        if assetClass and trade.asset_class != assetClass:
            continue
        if start and trade.trade_date_time < start:
            continue
        if end and trade.trade_date_time > end:
            continue
        if minPrice and trade.trade_details.price < minPrice:
            continue
        if maxPrice and trade.trade_details.price > maxPrice:
            continue
        if tradeType and trade.trade_details.buySellIndicator != tradeType:
            continue
        filtered_trades.append(trade)

    return filtered_trades

#this endpoint returns specific trade according to trade_id
#in this model trade_id from 1-20
#ex: http://127.0.0.1:8000/trades/5
#trade_id out of range raise an exception returns trade not found
@app.get("/trades/{trade_id}", response_model=Trade)
def get_traders(trade_id: str):
    for trade in database:
        if trade.trade_id == trade_id:
            return trade
    raise HTTPException(status_code=404, detail="Trade not found")





