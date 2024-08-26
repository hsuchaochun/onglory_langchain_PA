onglory_overview_metadata = {
    "description": "This table provides an overview of Onglory company's investments, including details on different accounts, exchanges, costs, values, profits, and losses across a variety of strategies and time frames.",
    "columns": {
        "name": {
            "description": "The name of the account or strategy (e.g., binance overall, ETH 202211 L, main account).",
            "type": "string"
        },
        "exchange": {
            "description": "The exchange on which the account or strategy is based (e.g., binance, coinbase).",
            "type": "string"
        },
        "cost": {
            "description": "The initial cost or investment in the account or strategy.",
            "type": "float"
        },
        "value": {
            "description": "The current value of the account or strategy.",
            "type": "float"
        },
        "pnl": {
            "description": "The total profit or loss (PNL) in the account or strategy.",
            "type": "float"
        },
        "pnl_per": {
            "description": "The profit or loss (PNL) expressed as a percentage of the initial cost.",
            "type": "float"
        },
        "24h_change": {
            "description": "The absolute change in the value of the account or strategy over the last 24 hours.",
            "type": "float"
        },
        "24h_change_per": {
            "description": "The percentage change in the value of the account or strategy over the last 24 hours.",
            "type": "float"
        }
    }
}

onglory_portfolio_metadata = {
    "description": "This table tracks Onglory company's cryptocurrency portfolio, including asset types, locations, exchanges, accounts, strategies, and related financial information.",
    "columns": {
        "name": {
            "description": "The name of the asset (e.g., USD, Bitcoin, Ethereum, Binance).",
            "type": "string"
        },
        "symbol": {
            "description": "The symbol of the asset (e.g., USDT, BTC, ETH, BNB).",
            "type": "string"
        },
        "type": {
            "description": "The type of transaction or account classification (e.g., quant, trading fee, manual).",
            "type": "string"
        },
        "location": {
            "description": "The organizational location of the asset within Onglory Corp.",
            "type": "string"
        },
        "exchange": {
            "description": "The exchange on which the asset is traded (e.g., binance, coinbase).",
            "type": "string"
        },
        "account": {
            "description": "The account email or identifier associated with the asset.",
            "type": "string"
        },
        "account_abbre": {
            "description": "A shortened abbreviation or name of the account.",
            "type": "string"
        },
        "amount": {
            "description": "The quantity of the asset in the portfolio.",
            "type": "float"
        },
        "cost": {
            "description": "The initial cost of the asset in the portfolio.",
            "type": "float"
        },
        "value": {
            "description": "The current value of the asset in the portfolio.",
            "type": "float"
        },
        "strategy_class": {
            "description": "The class or category of the trading strategy employed for the asset (e.g., SSL, INTERVAL, MANUAL).",
            "type": "string"
        },
        "strategy_name": {
            "description": "The specific name of the strategy being employed (e.g., SSL BTC [Long Short], INTERVAL AVAX).",
            "type": "string"
        },
        "trading_ticker": {
            "description": "The trading ticker symbol for the asset in the market (e.g., BTC/USDT, AVAX/USDT).",
            "type": "string"
        },
        "comment": {
            "description": "Additional comments or notes regarding the asset, if available.",
            "type": "string"
        }
    }
}

onglory_quant_status_metadata = {
    "description": "",
    "columns": {
        
    }
}

onglory_crypto_quant_indicator_status_metadata = {
    "description": "This table contains Onglory company cryptocurrency trading signals for different strategies, symbols, and time intervals, including indicators like SSL Hybrid, ADX and DI, and Heatmap Volume status.",
    "columns": {
        "strategy_name": {
            "description": "The name of the trading strategy being employed. It may include variations of a base strategy, such as Long, Short, or different versions like [Long Short] or [Long 1].",
            "type": "string"
        },
        "symbol": {
            "description": "The trading pair symbol (e.g., BTC/USDT, ETH/USDT).",
            "type": "string"
        },
        "time_interval": {
            "description": "The time frame of the chart or interval for the trading signals, such as 4 hours (4h).",
            "type": "string"
        },
        "SSL Hybrid": {
            "description": "The signal provided by the SSL Hybrid indicator, typically either bullish or bearish.",
            "type": "string"
        },
        "ADX and DI": {
            "description": "The signal given by the ADX and DI indicator, showing market trend strength and direction (e.g., bullish or bearish).",
            "type": "string"
        },
        "Heatmap Volume": {
            "description": "The status from the heatmap volume analysis, indicating actions like 'exit'.",
            "type": "string"
        },
        "last_updates_at": {
            "description": "The timestamp indicating the last update time for each signal, formatted as YYYY-MM-DD HH:MM:SS.",
            "type": "timestamp"
        }
    }
}

onglory_trading_history_metadata = {
    "description": "This table contains Onglory company detailed trading history records including orders, prices, quantities, and statuses for various trading strategies executed on different exchanges.",
    "columns": {
        "exchange": {
            "description": "The exchange where the trade was executed (e.g., binance).",
            "type": "string"
        },
        "account": {
            "description": "The email account associated with the trade execution.",
            "type": "string"
        },
        "strategy_name": {
            "description": "The name of the trading strategy being used (e.g., ETH 202212 L, AVAX 202403 LS).",
            "type": "string"
        },
        "orderId": {
            "description": "The unique identifier of the order on the exchange.",
            "type": "integer"
        },
        "orderListId": {
            "description": "The identifier of the order list or batch, usually -1 when not applicable.",
            "type": "integer"
        },
        "symbol": {
            "description": "The symbol of the trading pair (e.g., ETHUSDT, AVAXUSDT).",
            "type": "string"
        },
        "status": {
            "description": "The status of the order (e.g., FILLED, NEW).",
            "type": "string"
        },
        "clientOrderId": {
            "description": "The unique identifier of the order from the client side.",
            "type": "string"
        },
        "price": {
            "description": "The price at which the order was placed.",
            "type": "float"
        },
        "avgPrice": {
            "description": "The average price at which the order was filled, if applicable.",
            "type": "float"
        },
        "origQty": {
            "description": "The original quantity of the order.",
            "type": "float"
        },
        "executedQty": {
            "description": "The quantity of the order that has been executed.",
            "type": "float"
        },
        "cumQuote": {
            "description": "The cumulative amount of the quote asset that has been transacted.",
            "type": "float"
        },
        "cumulativeQuoteQty": {
            "description": "The cumulative quantity of the quote asset filled.",
            "type": "float"
        },
        "origQuoteOrderQty": {
            "description": "The original quote order quantity.",
            "type": "float"
        },
        "icebergQty": {
            "description": "The iceberg quantity, which is the hidden part of the order if applicable.",
            "type": "float"
        },
        "timeInForce": {
            "description": "The time in force policy for the order (e.g., GTC - Good Till Cancelled).",
            "type": "string"
        },
        "type": {
            "description": "The type of the order (e.g., LIMIT, MARKET, STOP_MARKET).",
            "type": "string"
        },
        "reduceOnly": {
            "description": "A boolean flag indicating whether the order is a reduce-only order.",
            "type": "boolean"
        },
        "closePosition": {
            "description": "A boolean flag indicating whether the position should be closed.",
            "type": "boolean"
        },
        "side": {
            "description": "The side of the order (e.g., BUY, SELL).",
            "type": "string"
        },
        "positionSide": {
            "description": "The position side for the trade (e.g., BOTH, LONG, SHORT).",
            "type": "string"
        },
        "stopPrice": {
            "description": "The stop price for stop orders.",
            "type": "float"
        },
        "workingType": {
            "description": "The working type of the stop order (e.g., CONTRACT_PRICE).",
            "type": "string"
        },
        "priceMatch": {
            "description": "The price match mode, if any.",
            "type": "string"
        },
        "selfTradePreventionMode": {
            "description": "Indicates if self-trade prevention is enabled (e.g., EXPIRE_MAKER).",
            "type": "string"
        },
        "goodTillDate": {
            "description": "Indicates if the order has a good till date expiration policy.",
            "type": "integer"
        },
        "priceProtect": {
            "description": "A boolean flag indicating if price protection is enabled.",
            "type": "boolean"
        },
        "origType": {
            "description": "The original type of the order (e.g., LIMIT, STOP_MARKET).",
            "type": "string"
        },
        "time": {
            "description": "The timestamp when the order was placed.",
            "type": "timestamp"
        },
        "updateTime": {
            "description": "The timestamp when the order was last updated.",
            "type": "timestamp"
        },
        "isWorking": {
            "description": "A boolean flag indicating whether the order is currently working.",
            "type": "boolean"
        },
        "workingTime": {
            "description": "The timestamp when the order started working.",
            "type": "timestamp"
        }
    }
}

onglory_value_history_metadata = {
    "description": "This table contains the historical value tracking of Onglory company's various trading accounts and strategies, including total values, individual account balances, PNL, and percentage changes over time.",
    "columns": {
        "time": {
            "description": "The date of the recorded values, formatted as YYYY-MM-DD.",
            "type": "date"
        },
        "total_value": {
            "description": "The total value of all accounts combined on that particular date.",
            "type": "float"
        },
        "coinbase_value": {
            "description": "The total value of assets on Coinbase on that particular date.",
            "type": "float"
        },
        "binance_value": {
            "description": "The total value of assets on Binance on that particular date.",
            "type": "float"
        },
        "BN main_account": {
            "description": "The value of the main account on Binance.",
            "type": "float"
        },
        "BN quant": {
            "description": "The value of the quantitative trading account on Binance.",
            "type": "float"
        },
        "BN ETH 202211 L": {
            "description": "The value of the ETH 202211 L strategy on Binance.",
            "type": "float"
        },
        "BN ETH 202211 LS": {
            "description": "The value of the ETH 202211 LS strategy on Binance.",
            "type": "float"
        },
        "BN ETH 202212 L": {
            "description": "The value of the ETH 202212 L strategy on Binance.",
            "type": "float"
        },
        "BN BTC 202301 LS": {
            "description": "The value of the BTC 202301 LS strategy on Binance.",
            "type": "float"
        },
        "BN AVAX 202403 LS": {
            "description": "The value of the AVAX 202403 LS strategy on Binance.",
            "type": "float"
        },
        "BN BNB 202403 LS": {
            "description": "The value of the BNB 202403 LS strategy on Binance.",
            "type": "float"
        },
        "BN AVAX 202403 INTER": {
            "description": "The value of the AVAX 202403 INTER strategy on Binance.",
            "type": "float"
        },
        "BN BTC 202403 INTER": {
            "description": "The value of the BTC 202403 INTER strategy on Binance.",
            "type": "float"
        },
        "BN dca": {
            "description": "The value of the dollar cost average (DCA) strategy on Binance.",
            "type": "float"
        },
        "BN con": {
            "description": "The value of the consolidation strategy on Binance.",
            "type": "float"
        },
        "total pnl": {
            "description": "The total profit and loss (PNL) for all accounts combined.",
            "type": "float"
        },
        "total pnl_percent": {
            "description": "The percentage change in total profit and loss for all accounts combined.",
            "type": "float"
        },
        "CB pnl": {
            "description": "The profit and loss (PNL) for the Coinbase account.",
            "type": "float"
        },
        "CB pnl_percent": {
            "description": "The percentage change in profit and loss for the Coinbase account.",
            "type": "float"
        },
        "BN pnl": {
            "description": "The profit and loss (PNL) for the Binance account.",
            "type": "float"
        },
        "BN pnl_percent": {
            "description": "The percentage change in profit and loss for the Binance account.",
            "type": "float"
        },
        "BN main_account_pnl": {
            "description": "The profit and loss (PNL) for the main Binance account.",
            "type": "float"
        },
        "BN main_account_pnl_percent": {
            "description": "The percentage change in profit and loss for the main Binance account.",
            "type": "float"
        },
        "BN quant pnl": {
            "description": "The profit and loss (PNL) for the quant strategy on Binance.",
            "type": "float"
        },
        "BN quant pnl_percent": {
            "description": "The percentage change in profit and loss for the quant strategy on Binance.",
            "type": "float"
        },
        "BN ETH 202211 L pnl": {
            "description": "The profit and loss (PNL) for the ETH 202211 L strategy on Binance.",
            "type": "float"
        },
        "BN ETH 202211 L pnl_percent": {
            "description": "The percentage change in profit and loss for the ETH 202211 L strategy on Binance.",
            "type": "float"
        },
        "BN ETH 202211 LS pnl": {
            "description": "The profit and loss (PNL) for the ETH 202211 LS strategy on Binance.",
            "type": "float"
        },
        "BN ETH 202211 LS pnl_percent": {
            "description": "The percentage change in profit and loss for the ETH 202211 LS strategy on Binance.",
            "type": "float"
        },
        "BN ETH 202212 L pnl": {
            "description": "The profit and loss (PNL) for the ETH 202212 L strategy on Binance.",
            "type": "float"
        },
        "BN ETH 202212 L pnl_percent": {
            "description": "The percentage change in profit and loss for the ETH 202212 L strategy on Binance.",
            "type": "float"
        },
        "BN BTC 202301 LS pnl": {
            "description": "The profit and loss (PNL) for the BTC 202301 LS strategy on Binance.",
            "type": "float"
        },
        "BN BTC 202301 LS pnl_percent": {
            "description": "The percentage change in profit and loss for the BTC 202301 LS strategy on Binance.",
            "type": "float"
        },
        "BN AVAX 202403 LS pnl": {
            "description": "The profit and loss (PNL) for the AVAX 202403 LS strategy on Binance.",
            "type": "float"
        },
        "BN AVAX 202403 LS pnl_percent": {
            "description": "The percentage change in profit and loss for the AVAX 202403 LS strategy on Binance.",
            "type": "float"
        },
        "BN BNB 202403 LS pnl": {
            "description": "The profit and loss (PNL) for the BNB 202403 LS strategy on Binance.",
            "type": "float"
        },
        "BN BNB 202403 LS pnl_percent": {
            "description": "The percentage change in profit and loss for the BNB 202403 LS strategy on Binance.",
            "type": "float"
        },
        "BN AVAX 202403 INTER pnl": {
            "description": "The profit and loss (PNL) for the AVAX 202403 INTER strategy on Binance.",
            "type": "float"
        },
        "BN AVAX 202403 INTER pnl_percent": {
            "description": "The percentage change in profit and loss for the AVAX 202403 INTER strategy on Binance.",
            "type": "float"
        },
        "BN BTC 202403 INTER pnl": {
            "description": "The profit and loss (PNL) for the BTC 202403 INTER strategy on Binance.",
            "type": "float"
        },
        "BN BTC 202403 INTER pnl_percent": {
            "description": "The percentage change in profit and loss for the BTC 202403 INTER strategy on Binance.",
            "type": "float"
        },
        
        "BN dca pnl": {
            "description": "The profit and loss (PNL) for the dollar cost average (DCA) strategy on Binance.",
            "type": "float"
        },
        "BN dca pnl_percent": {
            "description": "The percentage change in profit and loss for the dollar cost average (DCA) strategy on Binance.",
            "type": "float"
        },
        "BN con pnl": {
            "description": "The profit and loss (PNL) for the consolidation strategy on Binance.",
            "type": "float"
        },
        "BN con pnl_percent": {
            "description": "The percentage change in profit and loss for the consolidation strategy on Binance.",
            "type": "float"
        }
    }
}

whale_trace_metadata = {
    "description": "This table tracks large cryptocurrency transfers, typically referred to as whale transactions, across various blockchain networks, including details such as the transaction amount, source, and destination of the funds.",
    "columns": {
        "blockchain": {
            "description": "The blockchain network on which the transaction occurred (e.g., bitcoin).",
            "type": "string"
        },
        "transaction_type": {
            "description": "The type of transaction, usually a transfer of assets.",
            "type": "string"
        },
        "symbol": {
            "description": "The symbol of the cryptocurrency being transferred (e.g., BTC).",
            "type": "string"
        },
        "amount": {
            "description": "The amount of cryptocurrency transferred.",
            "type": "float"
        },
        "value_usd": {
            "description": "The USD equivalent value of the transferred cryptocurrency.",
            "type": "float"
        },
        "from_address": {
            "description": "The originating wallet address for the transaction, which may sometimes be unknown.",
            "type": "string"
        },
        "to_address": {
            "description": "The destination wallet address for the transaction, which may be a known exchange (e.g., Binance, Coinbase) or an unknown wallet.",
            "type": "string"
        },
        "timestamp": {
            "description": "The timestamp when the transaction was recorded.",
            "type": "timestamp"
        },
        "twitter_url": {
            "description": "A URL to the relevant Twitter announcement or tracking, if applicable.",
            "type": "string"
        },
        "telegram_url": {
            "description": "A URL to the relevant Telegram announcement or tracking, if applicable.",
            "type": "string"
        },
        "comment": {
            "description": "A textual description of the transaction, summarizing the transfer details such as the amount and the parties involved.",
            "type": "string"
        }
    }
}

bitcoinETF_history_metadata = {
    "description": "This table tracks historical Bitcoin ETF-related statistics, including Bitcoin supply, fund flows, and their impact on supply over time.",
    "columns": {
        "id": {
            "description": "The unique identifier for each record in the dataset.",
            "type": "integer"
        },
        "date": {
            "description": "The timestamp of the data record, formatted as YYYY-MM-DD HH:MM:SS.",
            "type": "timestamp"
        },
        "btc_supply": {
            "description": "The total supply of Bitcoin at the time of the record.",
            "type": "integer"
        },
        "byweekly_annualised_impact_on_supply": {
            "description": "The impact of ETF flows on Bitcoin supply, annualized on a biweekly basis.",
            "type": "float"
        },
        "flows_usd_since_approval_in_billions": {
            "description": "The total amount of fund flows into the ETF since its approval, denominated in billions of USD.",
            "type": "float"
        },
        "monthly_annualised_impact_on_supply": {
            "description": "The monthly annualized impact of ETF fund flows on Bitcoin supply.",
            "type": "float"
        },
        "past_week_flows_in_thousands": {
            "description": "The fund flows into the ETF over the past week, denominated in thousands of USD.",
            "type": "float"
        },
        "past_week_flows_usd_in_billions": {
            "description": "The total amount of fund flows into the ETF over the past week, denominated in billions of USD.",
            "type": "float"
        },
        "percentage_of_btc": {
            "description": "The percentage of the total Bitcoin supply accounted for by ETF flows.",
            "type": "float"
        },
        "tvl_in_thousands": {
            "description": "The total value locked (TVL) in the ETF, denominated in thousands of dollars.",
            "type": "float"
        },
        "usd_tvl_in_billions": {
            "description": "The total value locked (TVL) in the ETF, denominated in billions of dollars.",
            "type": "float"
        },
        "week_annualised_impact_on_supply": {
            "description": "The annualized impact of ETF fund flows on Bitcoin supply, calculated on a weekly basis.",
            "type": "float"
        },
        "update_time": {
            "description": "The timestamp of the most recent update for the record, formatted as YYYY-MM-DD HH:MM:SS.",
            "type": "timestamp"
        }
    }
}

bitcoinETF_netflow_metadata = {
    "description": "This table tracks the net flows of various Bitcoin ETFs, including the amount of Bitcoin transferred, its USD value, and details about the ETF issuer and time of transactions.",
    "columns": {
        "amount": {
            "description": "The amount of Bitcoin involved in the transaction.",
            "type": "float"
        },
        "amount_net_flow": {
            "description": "The net flow of Bitcoin for the ETF during the period, which may be positive or negative.",
            "type": "float"
        },
        "amount_usd": {
            "description": "The USD equivalent value of the Bitcoin involved in the transaction.",
            "type": "float"
        },
        "amount_usd_net_flow": {
            "description": "The net flow of USD value for the Bitcoin ETF, accounting for the amount in and out during the period.",
            "type": "float"
        },
        "etf_ticker": {
            "description": "The ticker symbol of the Bitcoin ETF (e.g., IBIT, BITB).",
            "type": "string"
        },
        "issuer": {
            "description": "The company or entity issuing the ETF (e.g., BlackRock, WisdomTree, Grayscale).",
            "type": "string"
        },
        "time": {
            "description": "The time of the transaction, formatted as YYYY-MM-DD HH:MM:SS.",
            "type": "timestamp"
        },
        "update_time": {
            "description": "The time when the data was last updated.",
            "type": "timestamp"
        }
    }
}