import markdown
import pdfkit
from functions import generate_pdf_from_markdown

# Sample markdown content
markdown_content = '''
Based on the data retrieved from the `onglory_portfolio` table, I will create an HTML table with the requested format. Here is the HTML code for the table:

```html
<table>
    <tr>
        <th>Name</th>
        <th>Symbol</th>
        <th>Type</th>
        <th>Location</th>
        <th>Exchange</th>
        <th>Account Abbr.</th>
        <th>Amount</th>
        <th>Cost</th>
        <th>Value</th>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BTC 202301 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Bitcoin</td>
        <td>BTC</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BTC 202301 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202211 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Ethereum</td>
        <td>ETH</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202211 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202211 L</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Ethereum</td>
        <td>ETH</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202211 L</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202212 L</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Ethereum</td>
        <td>ETH</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202212 L</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BNB 202403 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BNB 202403 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>AVAX 202403 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Avalanche</td>
        <td>AVAX</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>AVAX 202403 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BTC 202301 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202211 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202211 L</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>ETH 202212 L</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BNB 202403 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>AVAX 202403 LS</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>AVAX 202403 INTER</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Avalanche</td>
        <td>AVAX</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>AVAX 202403 INTER</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>AVAX 202403 INTER</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>manual</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>MANUAL</td>
        <td>503209.9379033400</td>
        <td></td>
        <td>503209.9379033400</td>
    </tr>
    <tr>
        <td>Bitcoin</td>
        <td>BTC</td>
        <td>manual</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>MANUAL</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>MANUAL</td>
        <td>23.9532422800</td>
        <td></td>
        <td>13617.4182361800</td>
    </tr>
    <tr>
        <td>USD</td>
        <td>USDT</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BTC 202403 INTER</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Bitcoin</td>
        <td>BTC</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BTC 202403 INTER</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td>BNB</td>
        <td>trading fee</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>BTC 202403 INTER</td>
        <td>0.0000000000</td>
        <td></td>
        <td>0.0000000000</td>
    </tr>
    <tr>
        <td>Ethereum</td>
        <td>ETH</td>
        <td>manual</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>MANUAL</td>
        <td>92.4469931660</td>
        <td></td>
        <td>245728.7301848863</td>
    </tr>
    <tr>
        <td>The Sandbox</td>
        <td>SAND</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>MANUAL</td>
        <td>217962.4271236600</td>
        <td></td>
        <td>57803.6356731946</td>
    </tr>
    <tr>
        <td>Decentraland</td>
        <td>MANA</td>
        <td>quant</td>
        <td>onglory corp</td>
        <td>binance</td>
        <td>MANUAL</td>
        <td>217851.8860372900</td>
        <td></td>
        <td>59451.7796995764</td>
    </tr>
</table>
```

This HTML table includes the data from the `onglory_portfolio` table and is formatted with proper HTML tags for readability and suitable for an A4 horizontal PDF output.
'''

# # Convert markdown to HTML
# html_content = markdown.markdown(markdown_content)

# # Convert HTML to PDF
# pdfkit.from_string(html_content, 'output.pdf')

generate_pdf_from_markdown(markdown_content, 'output.pdf')