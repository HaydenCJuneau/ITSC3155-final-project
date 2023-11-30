# AI Image Generation Pipeline
This documentation page serves to explain the method to which we are generating our ai images. 

## Background
Originally, we wanted to handle AI image generation ourselves. We were planning to use a local version of stable diffusion with control net, and we were going to utilize a realism model. The idea was that the web app would be running alongside the idle generator. The Flask app would inturrupt the generator when it wanted to request an image, which would then be forwarded back to the app afterwards. However, this became unfeasible as we considered our deployment and demo. *AI image generation requires too many resources, and it is not guaranteed that it will run on all devices.* Therefore, we had to switch gears and go with an api. Luckily, AI image generation is very popular at the present time. It was not hard to find a service that is providing exactly what we need. 

## Service
The team decided to go with [a site called getimg.ai](https://getimg.ai/tools/api). They provide a simple api that supports many models and allows for the controlnet extension. We have made an account, registered an organization, and linked payment. Testing was done to tweak all proper settings and the service seems to be working great.

## ControlNet and API usage
[Documentation on ControlNet](https://stable-diffusion-art.com/controlnet/#What_is_ControlNet)
<br />
[Documentation on getimg.ai API](https://docs.getimg.ai/reference/introduction)
<br />
In summary - ControlNet is an extension to stable diffusion, and allows for greater control over the output image. In our case, we want to use the 'scribble' processor. This processor takes a control image of white pixels on a black background, and uses that to shape the subject of the image. In this way, you are essentially drawing the overall shapes of the image, and letting AI fill in the details. 
<br />
**Note:** Although we will likely be drawing black lines on a white canvas, controlnet works best with a dark background and white lines. Remember to put image inversion as part of the pipeline.

### Models:
There are a lot of models we can use for this, but some stand to be better at this type of subject generation than others.
<br />
If you want to see the full list of models that will work with controlnet call the "parse_models" function. Some of the best ones will be listed below  

- dream-shaper-v8: This was the default model I was using for testing, it is pretty good with realism, but not great at capturing a single subject. It also has the ability to generate NSFW, and it is hard to disuede it from generating it
- icbinp-seco: "I cant believe its not photography" is really good at subject generationfor some reason. It understands fruit well. However I believe it also can be used to generate nsfw. We will have to place heavy negative weights or we will have to filter out positive prompts that we dont want. 
<br />

### Notes on other settings for the ai:
- model: See the note above. The id for the model being used.
- controlnet: Should always be set to `scribble-1.1`, since we are using scribble control images
- prompt: A positive prompt for the image, what do we want it to generate.
- negative_prompt: Keywords which we do not want the model to generate, nsfw should always be here
- width/height: size in pixels for the image, we should stay at a max of `512` since we are paying per pixelstep
- steps: How many steps to process the image. `20` is a good maximum because this also increases cost
- guidance: How strictly the model should conform to prompt, `5` is generally good
- scheduler: Most schedulers are pretty good, but `dpmsolver++` is the best for subject generation
- image: a base64 encoded string that contains our control image
