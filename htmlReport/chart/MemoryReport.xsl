<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html"
              doctype-system="about:legacy-compat"
              encoding="UTF-8"
              indent="yes" />

  <!--find the max memoryUsagePerRecord node-->
  <xsl:variable name="max">
    <xsl:for-each select="/testCases/testCase">
      <xsl:sort select="memoryUsagePerRecord" data-type="number" order="descending"/>
      <xsl:if test="position() = 1">         
         <table class="reportTable">
          <thead>
            <tr>
              <th>Max-Test Case</th>
              <th>Record Depth</th>
              <th>Memory Usage Per Record (KB)</th>
            </tr>
          </thead>
          <tbody>                      
            <tr>
              <td><xsl:value-of select="title"/></td>
              <td><xsl:value-of select="recordDepth"/> Depth</td>
              <td><xsl:value-of select="memoryUsagePerRecord"/> KB</td>
            </tr>            
          </tbody>
         </table>
      </xsl:if>
    </xsl:for-each>
  </xsl:variable>

  <!--find the max memoryUsagePerRecord test case-->
  <xsl:variable name="maxTestCase">
    <xsl:for-each select="/testCases/testCase">
      <xsl:sort select="memoryUsagePerRecord" data-type="number" order="descending"/>
      <xsl:if test="position() = 1">
        <xsl:value-of select="title"/>                 
      </xsl:if>
    </xsl:for-each>
  </xsl:variable>

  <xsl:template match="/">
    <html>
      <head>
        <title>Memory Report</title>
        <script src="Chart.js"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <script src="http://cdn.datatables.net/1.10.2/js/jquery.dataTables.min.js"></script>
        <link rel="stylesheet" href="http://cdn.datatables.net/1.10.2/css/jquery.dataTables.css"/>
        <link rel="stylesheet" href="Report.css" />
      </head>
      <body>      
        <script>
          var name=[];
          var values=[];
          <xsl:for-each select="testCases/testCase">
            name.push("<xsl:value-of select="title"/>");
            values.push(<xsl:value-of select="memoryUsagePerRecord"/>);
          </xsl:for-each>

          console.log(name);
          console.log(values);

          var randomScalingFactor = function(){ return Math.round(Math.random()*100)};

          var barChartData = 
          {
            labels : name,
            datasets : [
              {
                fillColor : "rgba(151,187,205,0.5)",
                strokeColor : "rgba(151,187,205,0.8)",
                highlightFill : "rgba(151,187,205,0.75)",
                highlightStroke : "rgba(151,187,205,1)",
                data : values
              }
            ]

          }

          window.onload = function()
          {
            var ctx = document.getElementById("canvas").getContext("2d");
            window.myBar = new Chart(ctx).Bar(barChartData, {
              responsive : true
            });
          }

          $(document).ready(function() 
          {
            $('#example').dataTable( {
                "paging":   true,
                "ordering": true,
                "info":     true
            } );
          } );

        </script>

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
              <td><xsl:value-of select="testCases/@version"/></td>
              <!--<td>\\10.32.26.161\Share\User\Jackie\ShellAPI\Performance Test\TestData\Memory\v2.5.0.L2</td>-->
            </tr>
          </tbody>
        </table>

        <!--<xsl:copy-of select="$max" />-->
        <div style="width: 100%">
          <canvas id="canvas" height="300" width="600"></canvas>
        </div>

        <!--Test Case Result Table-->      
        <table id="example" class="display" cellspacing="0" width="100%">
          <thead>
            <tr>
              <th>Test Case</th>
              <th>Record Depth</th>
              <th>Memory Usage Per Record (KB)</th>
            </tr>
          </thead>
          <tbody>
            <xsl:for-each select="testCases/testCase">
            <xsl:sort select="title" data-type="text"/>            
              <xsl:choose>
                <xsl:when test="title=$maxTestCase">
                  <tr>
                    <td class="reportTableMax"><xsl:value-of select="title"/></td>
                    <td class="reportTableMax"><xsl:value-of select="recordDepth"/> Depth</td>
                    <td class="reportTableMax"><xsl:value-of select="memoryUsagePerRecord"/> KB (max)</td>
                  </tr>
                </xsl:when>
                <xsl:otherwise>
                  <tr>
                    <td><xsl:value-of select="title"/></td>
                    <td><xsl:value-of select="recordDepth"/> Depth</td>
                    <td><xsl:value-of select="memoryUsagePerRecord"/> KB</td>
                  </tr>
                </xsl:otherwise>
              </xsl:choose>                         
            </xsl:for-each>
          </tbody>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>