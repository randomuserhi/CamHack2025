using UnityEngine;

public class Webcam : MonoBehaviour {
    private WebCamTexture webcamTexture;

    // Color pallate for mapping colours to tik toks from atlas
    public Texture2D pallete;

    // Number of variants we have (different tik toks for the same color)
    public int numVariants = 1;

    // Number of tik tok frames per atlas (width & height)
    // These frames are the frames of the video to play each tik tok
    public int atlasFrameWidth = 6;
    public int atlasFrameHeight = 6;
    private int FramesPerAtlas;

    // Number of atlases, this is to handle the limitation for size of texture.
    // So if we need more frames, we just have more atlases
    public int numAtlas = 1;

    // Size of each tik tok pixel
    public int tikTokWidth = 30;
    public int tikTokHeight = 54;

    // List of atlases and their variants
    // - size is numVariants * numAtlas
    // - indexed as atlas[variantIndex][atlasIndex]
    //
    // NOTE: that all textures need to be marked as readable, as they are copied
    //       to a Texture2DArray
    public Texture2D[] atlas;
    private Texture2DArray textureArray;

    // Post-processing effect on the initially captured image
    // public Material effect;

    // Output render texture
    public RenderTexture outTexture;

    // Texture containing the downscaled captured texture
    // Each pixel represents a single tik tok
    // (tik tok selected based on the pallete color that matches the pixel)
    public RenderTexture downscaleTexture;

    // Shader that converts downscaled image to image containing tik tok frames
    public ComputeShader tiktokShader;
    private int tiktokKernel;

    // Total number of frames for each tik tok
    public int totalNumFrames = 36;

    // Frame Rate to play each tik tok
    public float frameRate = 1.0f / 30.0f;

    private int frame = 0; // Frame index
    private float frameTimer = 0; // Time spent on each frame (at runtime)
    private int[] frameCoord = new int[2]; // Coordinate of frame on texture atlas

    // Trigger a scroll via Unity Editor
    public bool doScroll = false;

    // Scroll Animation properties
    public AnimationCurve scrollCurve;
    public float scrollAnimDuration = 0.5f;
    private int scroll = 0; // Pixel scroll of each tik tok frame
    private float scrollTimer = 0.0f; // Scroll animation timer

    void Start() {
        // Get the first available camera
        string camName = WebCamTexture.devices.Length > 0 ? WebCamTexture.devices[0].name : null;
        Debug.Log(camName);
        if (camName == null) {
            Debug.LogError("No webcam detected!");
            return;
        }

        webcamTexture = new WebCamTexture(camName);
        webcamTexture.Play();

        // 

        FramesPerAtlas = atlasFrameWidth * atlasFrameHeight;

        // Create a Texture2DArray
        textureArray = new Texture2DArray(tikTokWidth * pallete.width * atlasFrameWidth, tikTokHeight * pallete.height * atlasFrameHeight, atlas.Length, TextureFormat.ARGB32, false);
        textureArray.filterMode = FilterMode.Point;
        textureArray.wrapMode = TextureWrapMode.Clamp;

        // Copy pixels from each Texture2D into the array
        for (int i = 0; i < atlas.Length; i++) {
            Texture2D tex = atlas[i];
            textureArray.SetPixels(tex.GetPixels(), i);
        }

        textureArray.Apply();

        //

        tiktokKernel = tiktokShader.FindKernel("TikTok");

        tiktokShader.SetTexture(tiktokKernel, "Source", downscaleTexture);
        tiktokShader.SetTexture(tiktokKernel, "Result", outTexture);
        tiktokShader.SetTexture(tiktokKernel, "Pallete", pallete);
        tiktokShader.SetTexture(tiktokKernel, "Atlas", textureArray);

        tiktokShader.SetInts("TikTokSize", new int[] { tikTokWidth, tikTokHeight });
        tiktokShader.SetInts("PalletSize", new int[] { pallete.width, pallete.height });
        tiktokShader.SetInts("AtlasFrameSize", new int[] { atlasFrameWidth, atlasFrameHeight });
        tiktokShader.SetInts("ResultSize", new int[] { outTexture.width, outTexture.height });
        tiktokShader.SetInt("NumAtlas", numAtlas);
        tiktokShader.SetInt("NumVariants", numVariants);
    }

    void Update() {
        if (webcamTexture == null || !webcamTexture.isPlaying)
            return;

        // Scroll Animation

        if (doScroll && scrollTimer == 0.0f) {
            doScroll = false;
            scrollTimer += Time.deltaTime;
        }

        if (scrollTimer > 0.0f) {
            scrollTimer += Time.deltaTime;

            scroll = (int)(tikTokHeight * scrollCurve.Evaluate(scrollTimer / scrollAnimDuration));

            if (scrollTimer > scrollAnimDuration) {
                scrollTimer = 0.0f;
            }
        }

        // Render

        // Downscale
        Graphics.Blit(webcamTexture, downscaleTexture/*, effect*/);

        tiktokShader.SetInt("ScrollOffset", scroll);
        tiktokShader.SetInt("AtlasIndex", frame / 36);

        int subFrame = frame % 36;
        frameCoord[0] = subFrame % atlasFrameWidth;
        frameCoord[1] = subFrame / atlasFrameWidth;
        tiktokShader.SetInts("FrameCoord", frameCoord);

        // Dispatch threads
        int threadGroupSize = 8; // matches [numthreads(8,8,1)]
        int dispatchX = Mathf.CeilToInt((float)outTexture.width / threadGroupSize);
        int dispatchY = Mathf.CeilToInt((float)outTexture.height / threadGroupSize);
        tiktokShader.Dispatch(tiktokKernel, dispatchX, dispatchY, 1);

        // Go to next frame
        frameTimer += Time.deltaTime;
        if (frameTimer > frameRate) {
            frameTimer = 0;
            frame = (++frame) % totalNumFrames;
        }
    }

    void OnDestroy() {
        if (webcamTexture != null)
            webcamTexture.Stop();
    }
}
