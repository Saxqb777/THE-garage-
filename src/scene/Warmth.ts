import { Effect } from 'postprocessing';
import { Uniform } from 'three';

const fragment = /* glsl */ `
uniform float warmth;
void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
  vec3 c = inputColor.rgb;
  vec3 warm = c * vec3(1.10, 0.96, 0.80);
  outputColor = vec4(mix(c, warm, warmth), inputColor.a);
}`;

/**
 * Golden hour grade for the time of day slider: a gentle warm multiply before tone mapping.
 * It pulls its amount every frame from the getter, so React never has to mutate it.
 */
export class WarmthEffect extends Effect {
  private readonly getWarmth: () => number;

  constructor(getWarmth: () => number) {
    super('WarmthEffect', fragment, { uniforms: new Map([['warmth', new Uniform(0)]]) });
    this.getWarmth = getWarmth;
  }

  update() {
    this.uniforms.get('warmth')!.value = this.getWarmth();
  }
}
