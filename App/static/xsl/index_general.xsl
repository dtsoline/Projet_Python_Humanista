<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" indent="yes"/>
    
        
    <xsl:template match="/">
       
        <xsl:for-each select="//text/group/text">
            <p>
            <xsl:element name="li">
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:value-of select="concat('/item/', translate(@n, '#', ''))"/>
                    </xsl:attribute>
                    
                    <xsl:for-each select="./front/docDate/persName[@role='dest']">
                        <xsl:value-of select="concat('Lettre adressée à ', translate(@ref, '#', ''))"/>
                    </xsl:for-each>
                    
                    <xsl:if test="./front/docDate/persName[@role='author']">
                        <xsl:for-each select="./front/docDate/persName[@role='author']">
                            <xsl:value-of select="concat(', par ', translate(@ref, '#', ''))"/>
                        </xsl:for-each>
                    </xsl:if>
                    
                    <xsl:if test="./front/docDate/date">
                        <xsl:text>   DATE A AJOUTER</xsl:text>
                    </xsl:if>

                </xsl:element>
                
            </xsl:element>
            </p>
        </xsl:for-each>
       
       

    </xsl:template>
</xsl:stylesheet>