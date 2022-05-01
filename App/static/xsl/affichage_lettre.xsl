<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" indent="yes"/>

    <xsl:param name="numero"/>

    <xsl:variable name="lettre_arbo" select="descendant::text[@type = 'lettre'][@n = $numero]"/>


    <xsl:template match="/">

        <xsl:for-each select="$lettre_arbo">
            <div class="preletter">
                <p>
                        <xsl:value-of select="//front"/>
                </p>
            </div>

            <div class="body">
                <xsl:for-each select=".//p">
                    <p>
                        <xsl:copy>
                            <xsl:apply-templates/>
                        </xsl:copy>
                    </p>
                </xsl:for-each>
            </div>
        </xsl:for-each>

    </xsl:template>



    <xsl:template match="p//persName">
        <xsl:variable name="value_pers">
            <xsl:value-of select="translate(@ref, '#', '')"/>
        </xsl:variable>
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="concat('/pers/', $value_pers)"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </a>
    </xsl:template>
    
    
    <xsl:template match="p//placeName">
        <xsl:variable name="value_place">
            <xsl:value-of select="translate(@ref, '#', '')"/>
        </xsl:variable>
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="concat('/place/', $value_place)"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </a>
    </xsl:template>

</xsl:stylesheet>
