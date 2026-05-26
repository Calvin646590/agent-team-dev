import { Point } from "./point.js";

export class Line {
  constructor(
    public readonly start: Point,
    public readonly end: Point
  ) {}

  length(): number {
    return this.start.distanceTo(this.end);
  }

  slope(): number | null {
    const dx = this.end.x - this.start.x;
    if (dx === 0) {
      return null;
    }
    return (this.end.y - this.start.y) / dx;
  }

  toString(): string {
    return `Line(${this.start.toString()}, ${this.end.toString()})`;
  }
}
