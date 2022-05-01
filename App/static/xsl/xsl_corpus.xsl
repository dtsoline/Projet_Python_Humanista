<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" indent="yes"/>
    
    <xsl:template match="/">
        <xsl:for-each select="//text/group/text">
            <xsl:element name="div">
                <h1>
                    <xsl:if test="@type='lettre'">
                        <xsl:value-of select="concat('Lettre identifiée sous le numéro ', @n)" />
                    </xsl:if>
                </h1>
                <div>
                    <xsl:element name="h2">
                            <xsl:value-of select="descendant::docDate"/>
                    </xsl:element>
                </div>
                <div>
                    <xsl:value-of select="descendant::body"/>
                </div>
            </xsl:element>
        </xsl:for-each>

    </xsl:template>
</xsl:stylesheet>