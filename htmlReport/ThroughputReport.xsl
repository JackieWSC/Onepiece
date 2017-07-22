<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html"
              doctype-system="about:legacy-compat"
              encoding="UTF-8"
              indent="yes" />

  <xsl:template match="/">
    <html>
      <head>
        <title>Throughput Report</title>

        <link rel="stylesheet" href="Report.css" />
      </head>
      <body>

        <!--Hearder Table-->
        <table class="reportTable">
          <thead>
            <tr>
              <th>Shell API Version</th>
              <!--<th>Test Data</th>-->
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>ShellConversionAPI v2.5.0.L5</td>
              <!--<td>\\10.32.26.161\Share\User\Jackie\ShellAPI\Performance Test\TestData\Memory\v2.5.0.L2</td>-->
            </tr>
          </tbody>
        </table>

        <!--Test Case Result Table-->
        <table class="reportTable">
          <thead>
            <tr>
              <th>Test Case</th>
              <th>Average Used Time (ms)</th>
              <th>Total Update Count</th>
              <th>Average Output PayloadSize (byte)</th>
            </tr>
          </thead>
          <tbody>
            <xsl:for-each select="testCases/testCase">
            <xsl:sort select="title"/>
            <tr>
              <td><xsl:value-of select="title"/></td>
              <td><xsl:value-of select="averageUsedTime"/></td>
              <td><xsl:value-of select="totalUpdateCount"/></td>
              <td><xsl:value-of select="averageOutputPayloadSize"/></td>              
            </tr>
            </xsl:for-each>
          </tbody>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>