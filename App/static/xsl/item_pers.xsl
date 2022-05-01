<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" indent="yes"/>
    
    <xsl:param name="idpers"/>
    
   
    
    <xsl:template match="/">
        <div>
            <p>
                <xsl:value-of select="$idpers"/>
                <xsl:text>Mais affiche quelque chose stp !</xsl:text>
            </p>
        </div>
    </xsl:template>
    
    
</xsl:stylesheet>
