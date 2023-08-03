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

<!-- uppercase tag -->
<xsl:template match="eventModel">
  <ca:EventModel>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:EventModel>
</xsl:template>

<!-- uppercase tag -->
<xsl:template match="event">
  <ca:Event>
    <xsl:for-each select="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </ca:Event>
</xsl:template>

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

<!--
<xsl:template match="/ca:ComponentType">
  <ca:CompositeApplication xmlns:ca="http://siena.ibm.com/model/CompositeApplication">
	<xsl:attribute name="name"><xsl:value-of select="/ca:ComponentType/@id" /></xsl:attribute>
    <ca:Component id="TestEntity" name="TestEntity">
      <xsl:attribute name="id"><xsl:value-of select="/ca:ComponentType/@id" /></xsl:attribute>
      <xsl:attribute name="name"><xsl:value-of select="/ca:ComponentType/@name" /></xsl:attribute>
      <ca:ProvidedService id="{/ca:ComponentType/@id}Lifecycle_Transition_0" name="{/ca:ComponentType/@id}">
		<ca:InputMessage id="{/ca:ComponentType/@id}Lifecycle_Transition_0Request" schemaUri="data/{/ca:ComponentType/@id}.xsd" rootElement="{/ca:ComponentType/@id}"/>
		<ca:OutputMessage id="{/ca:ComponentType/@id}Lifecycle_Transition_0Response" schemaUri="data/{/ca:ComponentType/@id}.xsd" rootElement="{/ca:ComponentType/@id}"/>
	  </ca:ProvidedService>
	  <ca:InformationModel id="{/ca:ComponentType/@id}InformationModel" rootDataItemId="{/ca:ComponentType/@id}">
        <ca:DataItem id="{/ca:ComponentType/@id}" schemaUri="data/{/ca:ComponentType/@id}.xsd" rootElement="{/ca:ComponentType/@id}" listElement="{/ca:ComponentType/@id}s"/>
      </ca:InformationModel>
      <ca:LifecycleModel id="{/ca:ComponentType/@id}LifecycleModel">
        <ca:Lifecycle id="{/ca:ComponentType/@id}Lifecycle" stateXPath="/{/ca:ComponentType/@id}/CurrentState">
        <ca:State id="Created" initial="true"/>
        <ca:Transition id="{/ca:ComponentType/@id}Lifecycle_Transition_0" name="Create{/ca:ComponentType/@id}" targetStateIds="Created" serviceId="{/ca:ComponentType/@id}Lifecycle_Transition_0">
          <ca:Assign>
            <ca:Mapping>
              <ca:Source sourceId="{/ca:ComponentType/@id}Lifecycle_Transition_0Request" refType="serviceRequest" xPath="/{/ca:ComponentType/@id}"/>
              <ca:Target targetId="{/ca:ComponentType/@id}" refType="artifact" xPath="/{/ca:ComponentType/@id}"/>
            </ca:Mapping>
          </ca:Assign>
          <ca:Assign>
            <ca:Mapping>
              <ca:Source sourceId="{/ca:ComponentType/@id}" refType="artifact" xPath="/{/ca:ComponentType/@id}"/>
              <ca:Target targetId="{/ca:ComponentType/@id}Lifecycle_Transition_0Response" refType="serviceResponse" xPath="/{/ca:ComponentType/@id}"/>
            </ca:Mapping>
          </ca:Assign>
        </ca:Transition>
        </ca:Lifecycle>
      </ca:LifecycleModel>
    <ca:DataAccessModel id="{/ca:ComponentType/@id}AccessControlModel"/>
    <ca:AccessControlModel/>      

	  
	  <xsl:apply-templates select="node()"/>
    </ca:Component>
  </ca:CompositeApplication>
</xsl:template>
-->

</xsl:stylesheet>