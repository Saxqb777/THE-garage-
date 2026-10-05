/**
 * How high the car currently rides on the lift (metres). One shared mutable value, tweened by
 * the Lift and read every frame by the car, the parked shadow and the camera, so a lift move
 * never re-renders React.
 */
export const carLift = { y: 0 };

/** Top height of the lift, from the garage floor to the car's floor line. */
export const LIFT_HEIGHT = 1.55;
