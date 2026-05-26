import { Circle } from "./circle.js";
import { Rectangle } from "./rectangle.js";

// Union type (Line has no area, so not included)
export type Shape = Circle | Rectangle;

// Polymorphic dispatch function
export function area(shape: Shape): number {
  if (shape instanceof Circle) return shape.area();
  if (shape instanceof Rectangle) return shape.area();
  // TypeScript exhaustive check
  const _never: never = shape;
  throw new Error(`Unknown shape: ${_never}`);
}

// Convenience functions
export function circleArea(radius: number): number {
  return Math.PI * radius * radius;
}

export function rectangleArea(width: number, height: number): number {
  return width * height;
}
