Shader "Custom/DiffShader"
{
    Properties {}
    SubShader
    {
        Pass
        {
            ZTest Always Cull Off ZWrite Off
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            sampler2D _TexA;
            sampler2D _TexB;

            struct appdata {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };
            struct v2f {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            v2f vert (appdata v) {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target {
                float3 a = tex2D(_TexA, i.uv).rgb;
                float3 b = tex2D(_TexB, i.uv).rgb;

                float lumA = dot(a, float3(0.299, 0.587, 0.114));
				float lumB = dot(b, float3(0.299, 0.587, 0.114));
				float diff = step(0.15, abs(lumA - lumB));
                
				return fixed4(diff, diff, diff, 1);
            }
            ENDCG
        }
    }
}