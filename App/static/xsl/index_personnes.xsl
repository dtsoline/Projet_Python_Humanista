<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" indent="yes"/>

    <xsl:template match="/">
        <xsl:element name="div">
            <xsl:attribute name="id">
                <xsl:text>col_short</xsl:text>
            </xsl:attribute>

            <xsl:for-each select="//person/persName[@xml:lang = 'fr']">
                <xsl:sort select="." order="ascending"/>
                <p class="texte_index">

                    <b>
                        <xsl:value-of select="."/>
                        <xsl:text> : </xsl:text>
                    </b>

                    <xsl:variable name="IDName">

                        <xsl:value-of select="ancestor::person/@xml:id"/>
                    </xsl:variable>

                    <xsl:for-each
                        select="ancestor::TEI//text//persName[translate(@ref, '#', '') = $IDName]">

                        <xsl:element name="a">

                            <xsl:attribute name="href">
                                <xsl:text>/item/</xsl:text>
                                <xsl:value-of select="ancestor::text/@n"/>
                            </xsl:attribute>
                            <xsl:value-of select="ancestor::text/@n"/>
                        </xsl:element>

                        <xsl:choose>
                            <xsl:when test="position() != last()">, </xsl:when>
                            <xsl:otherwise>.</xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </p>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
