using UnityEngine;

public class Webcam : MonoBehaviour {
    private WebCamTexture webcamTexture;

    // Color pallate for mapping colours to tik toks from atlas
    public Texture2D pallete;
    public int palletWidth = 16;
    public int palletHeight = 16;

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

    // Output render texture
    public RenderTexture outTexture;

    // Texture containing the downscaled captured texture
    // Each pixel represents a single tik tok
    // (tik tok selected based on the pallete color that matches the pixel)
    public RenderTexture downscaleTexture;

    // Shader for computing difference between current and last frame
    // This is to pick up motion to determine when to reset frame index to 0
    public Material diffMat;

    // Shader for blurring the webcam footage
    public Material blurMat;

    // Texture that contains motion
    public RenderTexture motionTexture;

    // Texture containing the downscaled capture texture of the last frame
    // Used to take a difference to set the frame index to 0
    public RenderTexture previousDownscaledTexture;

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
    private int scrollMultiple = 0;
    private float scrollTimer = 0.0f; // Scroll animation timer

    void Start() {
        // Get the first available camera
        string camName = WebCamTexture.devices.Length > 0 ? WebCamTexture.devices[1].name : null;
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
        textureArray = new Texture2DArray(tikTokWidth * palletWidth * atlasFrameWidth, tikTokHeight * palletHeight * atlasFrameHeight, atlas.Length, TextureFormat.ARGB32, false);
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
        tiktokShader.SetInts("PalletSize", new int[] { palletWidth, palletHeight });
        tiktokShader.SetInts("AtlasFrameSize", new int[] { atlasFrameWidth, atlasFrameHeight });
        tiktokShader.SetInts("ResultSize", new int[] { outTexture.width, outTexture.height });
        tiktokShader.SetInt("NumAtlas", numAtlas);
        tiktokShader.SetInt("NumVariants", numVariants);

        //

        diffMat.SetTexture("_TexA", downscaleTexture);
        diffMat.SetTexture("_TexB", previousDownscaledTexture);
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
                scroll = 0;
                ++scrollMultiple;
            }
        }

        // Render

        // Downscale
        Graphics.Blit(webcamTexture, downscaleTexture/*, blurMat*/);

        // Compute motion (On CPU for now)
        {
            Graphics.Blit(null, motionTexture, diffMat);

            RenderTexture.active = motionTexture;
            Texture2D tex = new Texture2D(motionTexture.width, motionTexture.height, TextureFormat.RFloat, false);
            tex.ReadPixels(new Rect(0, 0, motionTexture.width, motionTexture.height), 0, 0);
            tex.Apply();

            Color[] pixels = tex.GetPixels();
            float activeCount = 0f;
            for (int i = 0; i < pixels.Length; i++)
                activeCount += pixels[i].r; // 1 if active, 0 if not

            float motionFraction = activeCount / pixels.Length;

            // If there is motion, reset frame index to first frame of tik tok
            if (activeCount > 0.1f) {
                frame = totalNumFrames - 1;
            }
        }

        Graphics.Blit(downscaleTexture, previousDownscaledTexture);

        tiktokShader.SetInt("ScrollOffset", scrollMultiple * tikTokHeight + scroll);
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
            frame = (--frame) % totalNumFrames;
            if (frame < 0) frame += totalNumFrames;
        }
    }

    void OnDestroy() {
        if (webcamTexture != null)
            webcamTexture.Stop();
    }
}
