<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/trades">
  <html>
  <head>
    <title>Trade Report</title>
  </head>
  <body>
    <h2>Trade Report</h2>
    <table border="1" cellpadding="5" cellspacing="0">
      <tr style="background-color:#f2f2f2;">
        <th>Trade ID</th>
        <th>Trader Name</th>
        <th>Instrument</th>
        <th>Type</th>
        <th>Quantity</th>
        <th>Price</th>
        <th>Currency</th>
        <th>Timestamp</th>
      </tr>
      <xsl:for-each select="trade">
      <tr>
        <td><xsl:value-of select="trade_id"/></td>
        <td><xsl:value-of select="trader/name"/></td>
        <td><xsl:value-of select="instrument/name"/> (<xsl:value-of select="instrument/symbol"/>)</td>
        <td><xsl:value-of select="transaction_details/type"/></td>
        <td align="right"><xsl:value-of select="transaction_details/quantity"/></td>
        <td align="right"><xsl:value-of select="format-number(transaction_details/price, '#,##0.00')"/></td>
        <td><xsl:value-of select="transaction_details/currency"/></td>
        <td><xsl:value-of select="transaction_details/timestamp"/></td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>