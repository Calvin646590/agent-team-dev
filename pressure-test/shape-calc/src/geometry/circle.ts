import { Point } from "./point.js";

export class Circle {
  constructor(
    public readonly center: Point,
    public readonly radius: number
  ) {
    if (radius <= 0) throw new Error("radius must be positive");
  }

  area(): number {
    return Math.PI * this.radius * this.radius;
  }

  perimeter(): number {
    return 2 * Math.PI * this.radius;
  }

  contains(point: Point): boolean {
    return this.center.distanceTo(point) <= this.radius;
  }

  toString(): string {
    return `Circle(${this.center}, ${this.radius})`;
  }
}
