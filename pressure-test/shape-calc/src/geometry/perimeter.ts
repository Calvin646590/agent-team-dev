import { Line } from "./line.js";
import { Circle } from "./circle.js";
import { Rectangle } from "./rectangle.js";

export type PerimeterShape = Line | Circle | Rectangle;

export function perimeter(shape: PerimeterShape): number {
  if (shape instanceof Line) return shape.length();
  if (shape instanceof Circle) return shape.perimeter();
  if (shape instanceof Rectangle) return shape.perimeter();
  const _never: never = shape;
  throw new Error(`Unknown shape: ${_never}`);
}

export function lineLength(start: { x: number; y: number }, end: { x: number; y: number }): number {
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  return Math.sqrt(dx * dx + dy * dy);
}

export function circleCircumference(radius: number): number {
  return 2 * Math.PI * radius;
}

export function rectanglePerimeter(width: number, height: number): number {
  return 2 * (width + height);
}
