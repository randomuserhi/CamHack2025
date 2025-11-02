Shader "Custom/BlurEffect"
{
    Properties
    {
        _MainTex ("Base (RGB)", 2D) = "white" {}
        _BlurSize ("Blur Size", Float) = 1.0
    }
    SubShader
    {
        Cull Off ZWrite Off ZTest Always
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            sampler2D _MainTex;
            float4 _MainTex_TexelSize;
            float _BlurSize;

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            v2f vert(appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                float2 uv = i.uv;
                float2 offset = _MainTex_TexelSize.xy * _BlurSize;

                fixed4 col = tex2D(_MainTex, uv) * 0.227027;
                col += tex2D(_MainTex, uv + float2(offset.x, 0)) * 0.316216;
                col += tex2D(_MainTex, uv - float2(offset.x, 0)) * 0.316216;
                col += tex2D(_MainTex, uv + float2(0, offset.y)) * 0.316216;
                col += tex2D(_MainTex, uv - float2(0, offset.y)) * 0.316216;

                return col;
            }
            ENDCG
        }
    }
}