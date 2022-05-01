<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" indent="yes"/>
    
    <xsl:template match="/">
        <xsl:element name="div"> 
            <xsl:for-each select="//place/placeName[@xml:lang='fr']">
                <xsl:sort select="." order="ascending"/>
                <p class="texte_index">
                    
                    <xsl:element name="b">
                        <xsl:value-of select="."/>
                        <xsl:text> : </xsl:text>
                    </xsl:element>
                    
                    <xsl:variable name="IDPlace">
                        
                        <xsl:value-of select="ancestor::place/@xml:id"/>
                    </xsl:variable>
                    
                    <xsl:for-each select="ancestor::TEI//text//placeName[translate(@ref, '#','')=$IDPlace]">
                        
                        <xsl:element name="a">
                            
                            <xsl:attribute name="href">
                                <xsl:text>/item/</xsl:text><xsl:value-of select="ancestor::text/@n"/>
                            </xsl:attribute>
                            <xsl:value-of select="ancestor::text/@n"/>
                        </xsl:element>
                        
                        <xsl:choose>
                            <xsl:when test="position()!= last()">, </xsl:when>
                            <xsl:otherwise>.</xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </p>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>