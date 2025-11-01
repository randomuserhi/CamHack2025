Shader "Custom/WebcamEffect"
{
    Properties
	{
		_MainTex ("Texture", 2D) = "white"
		_PixelWidth ("Pixel Width", Int) = 1
		_PixelHeight ("Pixel Height", Int) = 1
		_LuxMap ("LUX Map", 2D) = "white"
	}
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        Pass
        {
            CGPROGRAM
            #pragma vertex vert_img
            #pragma fragment frag

            #include "UnityCG.cginc"

            sampler2D _MainTex;

            fixed4 frag(v2f_img i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                col.rgb = 1.0 - col.rgb; // invert colors
                return col;
            }
            ENDCG
        }
    }
}