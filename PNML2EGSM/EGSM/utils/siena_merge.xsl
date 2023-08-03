<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ca="http://siena.ibm.com/model/CompositeApplication">
  <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
  
 <!-- keep comments -->
<xsl:template match="comment()">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

<!-- fix namespaces -->  
<xsl:template match="*">
    <!-- remove element prefix -->
    <xsl:element name="ca:{local-name()}" namespace="http://siena.ibm.com/model/CompositeApplication">
      <!-- process attributes -->
      <xsl:for-each select="@*">
        <!-- remove attribute prefix -->
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
      <xsl:apply-templates/>
    </xsl:element>
</xsl:template>


<xsl:template match="eventModel">
  <xsl:copy-of select="document('egsm-temp.xml')/ca:CompositeApplicationType/ca:EventModel" />
  <!--
  <ca:EventModel>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:EventModel>
  -->
</xsl:template>

<!--
<xsl:template match="event">
  <ca:Event>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:Event>
</xsl:template> -->

<!-- uppercase tag -->
<xsl:template match="component">
  <ca:Component>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:Component>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="informationModel">
  <ca:InformationModel>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:InformationModel>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="dataItem">
  <ca:DataItem>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:DataItem>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="guardedStageModel">
  <ca:GuardedStageModel>
    <xsl:copy-of select="document('egsm-temp.xml')/ca:CompositeApplicationType/ca:Component/ca:GuardedStageModel/ca:Stage" />
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:GuardedStageModel>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="stage">
  <ca:Stage>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:Stage>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="subStage">
  <ca:SubStage>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:SubStage>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="dataFlowGuard">
  <ca:DataFlowGuard>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:DataFlowGuard>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="processFlowGuard">
  <ca:ProcessFlowGuard>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:ProcessFlowGuard>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="milestone">
  <ca:Milestone>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:Milestone>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="condition">
  <ca:Condition>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:Condition>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="faultLogger">
  <ca:FaultLogger>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:FaultLogger>
</xsl:template>

</xsl:stylesheet>