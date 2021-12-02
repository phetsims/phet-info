# UI Sound - Quickstart Guide

@author Chris Malley (PixelZoom, Inc.)

Follow these steps to add support for UI sound to a simulation.

1. In your sim's package.json, add `"supportsSound": true` this to the “phet.simFeatures” section, like this:

```
{
   ...
   "phet": {
      "simFeatures": {
         "supportsSound": true,
         ...
      }
   },
   ...
}
```

2. In your sim's repository `{{SIM_REPO}}`, run `grunt update` to regenerate `{{SIM_REPO}}_en.html`.
     

3. After completing steps 1 & 2, your sim now supports all sounds that are provided by common code.
If you need to turn some sounds off, you can do so by setting the output level for a _category_ to zero.
(If you're not familiar with _category_, see the `categoryName` option in soundManager.js `addSoundGenerator`.)
For example, to turn off the `ui-sounds` category of sounds, add this to `{{SIM_REPO}-main.js`, after the call to `sim.start()`:

```js
soundManager.setOutputLevelForCategory( 'user-interface', 0 );
```

4. To add a sound to your sim, you'll first need a sound file that is in MP3 format. 
Common-code sounds live in `{{COMMON_REPO}}/sounds/` or in `tambo/sounds`.
Sim-specific sounds live in `{{SIM_REPO}}/sounds`. 
(Note that creating new sounds involves sound design, and should involve designers.)

    To add a sim-specific sound file:

   * Put the `.mp3` sound file in `{{REPO}}/sounds/` and make an entry in  `{{REPO}}/sounds/license.json`.
   * Put the corresponding `.wav` file in `{{REPO}}/assets/`.
   * Run `grunt modulify` to generate the `_mp3.js` file for the .mp3 file. The `_mp3.js` file will be used in code.
     
5. To use a sound file in a sim, you'll need to import it, create a `SoundClip`, 
and add it to the soundManager. For example:

```js
import bing_mp3 from '../../../sounds/bing_mp3.js;
...
const bingSoundClip = new SoundClip( bing_mp3, {
  ...
} );
soundManager.addSoundGenerator( bingSoundClip, { 
  categoryName: 'ui-sounds',
  ...
} );
```

It is highly recommend to include a `categoryName` that is appropriate for your sound.
See `SoundClip` and `soundManager.addSoundGenerator` for additional options.
       
6. If your sound is associated with a common-code UI component that supports sound, provide
the `SoundClip` to the UI component. This is typically done via `options`. For example:

```js
const bingButton = new RoundPushButton( ..., {
  soundPlayer: bingSoundClip
} );
```

7. If your sound is related to a custom user interaction (not supported via common code), 
you will need to explicitly call `play`.  

```js
const dragListener = new DragListener( {
  start: () => bingSoundClip.play()
  ...
} );
```

8. If your sound is associated with a model state change, you will need to explicitly call `play`
when the state changes. For example, for a Property:

```js
const lightIsOnPropertry = new BooleanProperty( true );
lightIsOnPropertry.link( lightIsOn => lightIsOn ? lightOnSound.play() : lightOffSound.play() );
```
